import json
from typing import Any, Dict, Union
from nonebot.typing import overrides

from nonebot.message import handle_event
from nonebot.adapters import Bot as BaseBot

from .event.message import FriendMessage, GroupMessage, MessageEvent, TempMessage

from .event import Event
from .message import MessageChain, MessageSegment
from .utils import SyncIDStore, process_event, Log as log


class Bot(BaseBot):

    @overrides(BaseBot)
    async def send(
        self,
        event: Event,
        message: Union[str, MessageChain, MessageSegment],
        at_sender: bool = False,
        **kwargs,
    ) -> Any:
        """
        :说明:

          根据 ``event`` 向触发事件的主体发送信息

        :参数:

          * ``event: Event``: Event对象
          * ``message: Union[MessageChain, MessageSegment, str]``: 要发送的消息
          * ``at_sender: bool``: 是否 @ 事件主体
        """
        if not isinstance(message, MessageChain):
            message = MessageChain(message)
        if isinstance(event, FriendMessage):
            return await self.send_friend_message(target=event.sender.id,
                                                  message_chain=message)
        elif isinstance(event, GroupMessage):
            if at_sender:
                message = MessageSegment.at(event.sender.id) + message
            return await self.send_group_message(group=event.sender.group.id,
                                                 message_chain=message)
        elif isinstance(event, TempMessage):
            return await self.send_temp_message(qq=event.sender.id,
                                                group=event.sender.group.id,
                                                message_chain=message)
        else:
            raise ValueError(f'Unsupported event type {event!r}.')
