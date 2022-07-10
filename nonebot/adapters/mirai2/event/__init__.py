r"""
\:\:\: warning
事件中为了使代码更加整洁, 我们采用了与PEP8相符的命名规则取代Mirai原有的驼峰命名

部分字段可能与文档在符号上不一致
\:\:\:
"""
from .base import (Event, GroupChatInfo, GroupInfo, PrivateChatInfo,
                   UserPermission)
from .message import *  # noqa
from .notice import *  # noqa
from .request import *  # noqa
from .meta import *  # noqa

__all__ = [  # noqa
    'Event', 'GroupChatInfo', 'GroupInfo', 'PrivateChatInfo', 'UserPermission',
    'MessageSource', 'MessageEvent', 'GroupMessage', 'FriendMessage',
    'TempMessage', 'NoticeEvent', 'MuteEvent', 'BotMuteEvent', 'BotUnmuteEvent',
    'MemberMuteEvent', 'MemberUnmuteEvent', 'BotJoinGroupEvent',
    'BotLeaveEventActive', 'BotLeaveEventKick', 'MemberJoinEvent',
    'MemberLeaveEventKick', 'MemberLeaveEventQuit', 'FriendRecallEvent',
    'GroupRecallEvent', 'GroupStateChangeEvent', 'GroupNameChangeEvent',
    'GroupEntranceAnnouncementChangeEvent', 'GroupMuteAllEvent',
    'GroupAllowAnonymousChatEvent', 'GroupAllowConfessTalkEvent',
    'GroupAllowMemberInviteEvent', 'MemberStateChangeEvent',
    'MemberCardChangeEvent', 'MemberSpecialTitleChangeEvent',
    'BotGroupPermissionChangeEvent', 'MemberPermissionChangeEvent',
    'RequestEvent', 'NewFriendRequestEvent', 'MemberJoinRequestEvent',
    'BotInvitedJoinGroupRequestEvent', 'MetaEvent', 'BotOnlineEvent',
    'BotOfflineEventActive', 'BotOfflineEventForce', 'BotOfflineEventDropped'
    'BotReloginEvent'
]
