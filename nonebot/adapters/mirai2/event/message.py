from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

from nonebot.typing import overrides

from ..message import MessageChain
from .base import (
    Event,
    GroupChatInfo,
    OtherChatInfo,
    PrivateChatInfo,
    StrangerChatInfo
)


class MessageSource(BaseModel):
    id: int
    time: datetime


class MessageQuote(BaseModel):
    _type: str = Field(..., alias="type")
    id: int
    sender_id: int = Field(..., alias="senderId")
    target_id: int = Field(..., alias="targetId")
    group_id: int = Field(None, alias="groupId")
    origin: MessageChain


class MessageEvent(Event):
    """消息事件基类"""
    message_chain: MessageChain = Field(alias='messageChain')
    source: Optional[MessageSource] = None
    sender: Any
    to_quote: bool = False
    quote: Optional[MessageQuote] = None

    @overrides(Event)
    def get_type(self) -> Literal["message"]:  # noqa
        return 'message'

    @overrides(Event)
    def get_message(self) -> MessageChain:
        return self.message_chain

    @overrides(Event)
    def get_plaintext(self) -> str:
        return self.message_chain.extract_plain_text()

    @overrides(Event)
    def get_user_id(self) -> str:
        raise NotImplementedError

    @overrides(Event)
    def get_session_id(self) -> str:
        raise NotImplementedError


class GroupMessage(MessageEvent):
    """群消息事件"""
    sender: GroupChatInfo
    to_me: bool = False

    @overrides(MessageEvent)
    def get_session_id(self) -> str:
        return f'group_{self.sender.group.id}_' + self.get_user_id()

    @overrides(MessageEvent)
    def get_user_id(self) -> str:
        return str(self.sender.id)

    @overrides(MessageEvent)
    def is_tome(self) -> bool:
        return self.to_me


class FriendMessage(MessageEvent):
    """好友消息事件"""
    sender: PrivateChatInfo

    @overrides(MessageEvent)
    def get_user_id(self) -> str:
        return str(self.sender.id)

    @overrides(MessageEvent)
    def get_session_id(self) -> str:
        return 'friend_' + self.get_user_id()

    @overrides(MessageEvent)
    def is_tome(self) -> bool:
        return True


class TempMessage(MessageEvent):
    """临时会话消息事件"""
    sender: GroupChatInfo

    @overrides(MessageEvent)
    def get_user_id(self) -> str:
        return str(self.sender.id)

    @overrides(MessageEvent)
    def get_session_id(self) -> str:
        return f'temp_{self.sender.group.id}_' + self.get_user_id()

    @overrides(MessageEvent)
    def is_tome(self) -> bool:
        return True


class StrangerMessage(MessageEvent):
    """陌生人消息事件"""
    sender: StrangerChatInfo

    @overrides(MessageEvent)
    def get_user_id(self) -> str:
        return str(self.sender.id)

    @overrides(MessageEvent)
    def get_session_id(self) -> str:
        return 'stranger_' + self.get_user_id()


class OtherClientMessage(MessageEvent):
    """其他客户端消息事件"""
    sender: OtherChatInfo

    @overrides(MessageEvent)
    def get_user_id(self) -> str:
        return str(self.sender.id)

    @overrides(MessageEvent)
    def get_session_id(self) -> str:
        return 'other_' + self.get_user_id()
