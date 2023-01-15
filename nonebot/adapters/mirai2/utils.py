import asyncio
import re
import sys
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from nonebot.message import handle_event
from nonebot.typing import overrides
from nonebot.utils import DataclassEncoder

from .exception import ApiNotAvailable

from .event import Event, GroupMessage, MessageEvent, MessageSource, MessageQuote
from .message import MessageSegment, MessageType
from . import log

if TYPE_CHECKING:
    from .bot import Bot


def snake_to_camel(name: str):
            for i in ['anno', 'resp']:
                if re.match(i, name):
                    return name
            first, *rest = name.split('_')
            return ''.join([first.lower(), *(r.title() for r in rest)])


def process_source(bot: "Bot", event: MessageEvent) -> MessageEvent:
    source = event.message_chain.extract_first(MessageType.SOURCE)
    if source is not None:
        event.source = MessageSource.parse_obj(source.data)
    return event


def process_quote(bot: "Bot", event: Union[MessageEvent, GroupMessage]) -> MessageEvent:
    quote = event.message_chain.extract_first(MessageType.QUOTE)
    if quote is not None:
        event.quote = MessageQuote.parse_obj(quote.data)
        if quote.data['senderId'] == event.self_id:
            event.to_me = True
    return event


def process_at(bot: "Bot", event: GroupMessage) -> GroupMessage:
    c = 0
    for msg in event.message_chain:
        if (msg.type == MessageType.AT) and (msg.data.get('target', '') == event.self_id):
            event.to_me = True
            event.message_chain.pop(c)
            break
        c += 1
    if not event.message_chain:
        event.message_chain.append(MessageSegment.plain(""))
    return event


def process_nick(bot: "Bot", event: GroupMessage) -> GroupMessage:
    plain = event.message_chain.extract_first(MessageType.PLAIN)
    if plain is not None:
        if len(bot.config.nickname):
            text = str(plain)
            nick_regex = '|'.join(filter(lambda x: x, bot.config.nickname))
            matched = re.search(rf"^({nick_regex})([\s,，]*|$)", text, re.IGNORECASE)
            if matched is not None:
                event.to_me = True
                nickname = matched.group(1)
                log.info(f'User is calling me {nickname}')
                plain.data['text'] = text[matched.end():]
        event.message_chain.insert(0, plain)
    return event


async def process_event(bot: "Bot", event: Event) -> None:
    if isinstance(event, MessageEvent):
        event = process_source(bot, event)
        event = process_quote(bot, event)
        if isinstance(event, GroupMessage):
            event = process_nick(bot, event)
            event = process_at(bot, event)
    await handle_event(bot, event)


class SyncIDStore:
    _sync_id = 0
    _futures: Dict[str, asyncio.Future] = {}

    @classmethod
    def get_id(cls) -> str:
        sync_id = cls._sync_id
        cls._sync_id = (cls._sync_id + 1) % sys.maxsize
        return str(sync_id)

    @classmethod
    def add_response(cls, response: Dict[str, Any]):
        if not isinstance(response.get('syncId'), str):
            return
        sync_id: str = response['syncId']
        if sync_id in cls._futures:
            cls._futures[sync_id].set_result(response)
        return sync_id

    @classmethod
    async def fetch_response(cls, sync_id: str,
                             timeout: Optional[float]) -> Dict[str, Any]:
        future = asyncio.get_running_loop().create_future()
        cls._futures[sync_id] = future
        try:
            return await asyncio.wait_for(future, timeout)
        except asyncio.TimeoutError:
            raise ApiNotAvailable('timeout') from None
        finally:
            del cls._futures[sync_id]


class MiraiDataclassEncoder(DataclassEncoder):

    @overrides(DataclassEncoder)
    def default(self, o):
        if isinstance(o, MessageSegment):
            return o.as_dict()
        return super().default(o)
