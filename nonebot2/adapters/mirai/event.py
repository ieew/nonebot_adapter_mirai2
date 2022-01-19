from pydantic import BaseModel
from nonebot.adapters import Event as BaseEvent

from .message import MessageChain


class Event(BaseEvent):

    def get_type(self) -> str:
        raise NotImplementedError

    def get_event_name(self) -> str:
        raise NotImplementedError

    def get_event_description(self) -> str:
        return str(self.dict())

    def get_message(self) -> MessageChain:
        raise NotImplementedError

    def get_plaintext(self) -> str:
        raise NotImplementedError

    def get_user_id(self) -> str:
        raise NotImplementedError

    def get_session_id(self) -> str:
        raise NotImplementedError

    def is_tome(self) -> bool:
        return False
