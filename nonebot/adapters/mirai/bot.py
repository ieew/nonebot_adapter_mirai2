from typing import Any, Optional, Union
from nonebot.typing import overrides

from nonebot.adapters import Bot as BaseBot

from .event.message import FriendMessage, GroupMessage, TempMessage

from .event import Event
from .message import MessageChain, MessageSegment


class Bot(BaseBot):

    @overrides(BaseBot)
    async def send(
        self,
        event: Event,
        message: Union[str, MessageChain, MessageSegment],
        at_sender: Optional[bool] = False,
        quote: Optional[int] = None,
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
                                                  message_chain=message,
                                                  quote=quote)
        elif isinstance(event, GroupMessage):
            if at_sender:
                message = MessageSegment.at(event.sender.id) + message
            return await self.send_group_message(group=event.sender.group.id,
                                                 message_chain=message,
                                                 quote=quote)
        elif isinstance(event, TempMessage):
            return await self.send_temp_message(qq=event.sender.id,
                                                group=event.sender.group.id,
                                                message_chain=message,
                                                quote=quote)
        else:
            raise ValueError(f'Unsupported event type {event!r}.')
