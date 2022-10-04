
from nonebot.permission import Permission
from nonebot.adapters import Bot, Event

from .event.base import UserPermission
from .event.message import GroupMessage


async def _group_member(bot: "Bot", event: "Event") -> bool:
    return isinstance(event, GroupMessage) and \
        event.sender.permission == UserPermission.MEMBER


async def _group_admin(bot: "Bot", event: "Event") -> bool:
    return isinstance(event, GroupMessage) and \
        event.sender.permission == UserPermission.ADMINISTRATOR


async def _group_admins(bot: "Bot", event: "Event") -> bool:
    return isinstance(event, GroupMessage) and \
        event.sender.permission in \
        (UserPermission.ADMINISTRATOR, UserPermission.OWNER)


async def _group_owner(bot: "Bot", event: "Event") -> bool:
    return isinstance(event, GroupMessage) and \
        event.sender.permission == UserPermission.OWNER


async def _group_owner_superuser(bot: "Bot", event: "Event") -> bool:
    return isinstance(event, GroupMessage) and \
        (event.sender.permission == UserPermission.OWNER or
            event.get_user_id() in bot.config.superusers)


GROUP_MEMBER = Permission(_group_member)  # 仅成员
GROUP_ADMIN = Permission(_group_admin)  # 仅管理员
GROUP_ADMINS = Permission(_group_admins)  # 群主或管理员
GROUP_OWNER = Permission(_group_owner)  # 仅群主
GROUP_OWNER_SUPERUSER = Permission(_group_owner_superuser)  # 仅群主或超管
from nonebot.permission import SUPERUSER  # 仅超管  # noqa
