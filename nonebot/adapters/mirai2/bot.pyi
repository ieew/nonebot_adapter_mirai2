from typing import Literal, Union, Optional, overload

from nonebot.adapters import Bot as BaseBot

from .event import Event
from .message import MessageChain, MessageSegment


class Bot(BaseBot):
    r"""
    mirai-api-http 协议 Bot 适配。

    \:\:\: warning
    API中为了使代码更加整洁, 我们采用了与PEP8相符的命名规则取代Mirai原有的驼峰命名

    部分字段可能与文档在符号上不一致
    \:\:\:

    """

    _type = 'mirai'

    async def send(
        self, *,
        event: Event,
        message: Union[MessageChain, MessageSegment, str],
        at_sender: Optional[bool] = False,
        quote: Optional[int] = None
    ):
        """
        :说明:

            根据 ``event`` 向触发事件的主体发送信息

        :参数:

            * ``event: Event``: Event对象
            * ``message: Union[MessageChain, MessageSegment, str]``: 要发送的消息
            * ``at_sender: bool``: 是否 @ 事件主体
        """
        ...

    async def about(self):
        """
        :说明:

            获取插件信息

        :参数:

            * 无
        """
        ...

    async def message_from_id(self, *, id: int):
        """
        :说明:

            获取消息 id 的内容

        :参数:

            * ``id: int`` 消息 id
        """
        ...

    async def friend_list(self):
        """
        :说明:

            获取好友列表

        :参数:

            * 无
        """
        ...

    async def group_list(self):
        """
        :说明:

            获取群列表

        :参数:

            * 无
        """
        ...

    async def member_list(self, *, target: int):
        """
        :说明:

            获取群 target 的成员列表

        :参数:

            * ``target: int`` 群 id
        """
        ...

    async def bot_pro_file(self):
        """
        :说明:

            获取Bot资料

        :参数:

            * 无
        """
        ...

    async def friend_pro_file(self, *, target: int):
        """
        :说明:

            获取好友 target 的资料

        :参数:

            * ``target: int`` 好友 id
        """
        ...

    async def member_profile(self, *, target: int, member_id: int):
        """
        :说明:

            获取群 target 中的成员 member_id 的资料

        :参数:

            * ``target: int`` 群 id
            * ``member_id`` 成员 id
        """
        ...

    async def send_friend_message(
        self, *,
        target: int,
        message_chain: MessageChain,
        quote: Optional[int]
    ):
        """
        :说明:

            发送好友消息

        :必填:

            * ``target: int`` 好友 id
            * ``message_chain: MessageChain`` 消息内容: (MessageChain("xxxx"))

        :选填:

            * ``quote: int`` 需引用消息的 id
        """
        ...

    async def send_group_message(
        self, *,
        target: int,
        message_chain: MessageChain,
        quote: Optional[int]
    ):
        """
        :说明:

            发送消息 message_chain 到 target 群

        :必填:

            * ``target: int`` 群 id
            * ``message_chain: MessageChain`` 消息内容: (MessageChain("xxxx"))

        :选填:

            * ``quote: int`` 需引用消息的 id
        """
        ...

    async def send_temp_message(
        self, *,
        qq: int,
        group: int,
        message_chain: MessageChain,
        quote: Optional[int]
    ):
        """
        :说明:

            发送消息 message_chain 到 target 群

        :必填:

            * ``qq: int`` qq id
            * ``group: int`` 群 id
            * ``message_chain: MessageChain`` 消息内容: (MessageChain("xxxx"))

        :选填:

            * ``quote: int`` 需引用消息的 id
        """
        ...

    async def send_nudge(
        self, *,
        target: int,
        subject: int,
        kind: str
    ):
        """
        :说明:

            发送头像戳一戳消息

        :参数:

            * ``target: int`` 戳一戳目标
            * ``subject: int`` 戳一戳接受主体(戳一戳信息会发送到该主体，为 群号/qq号)
            * ``kind: str`` 上下文类型，可选值: (Friend, Group, Stranger)
        """
        ...

    async def recall(self, *, target: int):
        """
        :说明:

            撤回消息

        :参数:

            * ``target: int`` 需要撤回的消息的 id
        """
        ...

    async def file_list(
        self, *,
        id: str,
        path: Optional[str],
        target: Optional[int],
        group: Optional[int],
        qq: Optional[int],
        with_download_info: Optional[bool],
        offset: Optional[int],
        size: Optional[int]
    ):
        """
        :说明:

            查看文件列表

        :必填:

            * ``id: int`` 文件夹id，空串为根目录

        :可选:

            * ``path: str`` 文件夹路径，文件夹允许重名，不保证准确，准确定位使用 id
            * ``target: int`` 群号或好友 qq 号
            * ``group: int`` 群号
            * ``qq: int`` 好友 qq 号
            * ``with_download_info: bool`` 是否携带下载信息，额外请求，无必要不要携带
            * ``offset: int`` 分页偏移
            * ``size: int`` 分页大小
        """
        ...

    async def file_info(
        self, *,
        id: str,
        path: Optional[str],
        target: Optional[int],
        group: Optional[int],
        qq: Optional[int],
        with_download_info: Optional[bool]
    ):
        """
        :说明:

            获取文件信息

        :必填:

            * ``id: int`` 文件夹id，空串为根目录

        :可选:

            * ``path: str`` 文件夹路径，文件夹允许重名，不保证准确，准确定位使用 id
            * ``target: int`` 群号或好友 qq 号
            * ``group: int`` 群号
            * ``qq: int`` 好友 qq 号
            * ``with_download_info: bool`` 是否携带下载信息，额外请求，无必要不要携带
        """
        ...

    async def file_mkdir(
        self, *,
        id: str,
        directory_name: str,
        path: Optional[str],
        target: Optional[int],
        group: Optional[int],
        qq: Optional[int]
    ):
        """
        :说明:

            创建文件夹

        :必填:

            * ``id: int`` 文件夹id，空串为根目录
            * ``directory_name: str`` 是否携带下载信息，额外请求，无必要不要携带

        :可选:

            * ``path: str`` 文件夹路径，文件夹允许重名，不保证准确，准确定位使用 id
            * ``target: int`` 群号或好友 qq 号
            * ``group: int`` 群号
            * ``qq: int`` 好友 qq 号
        """
        ...

    async def file_delete(
        self, *,
        id: str,
        path: Optional[str],
        target: Optional[int],
        group: Optional[int],
        qq: Optional[int]
    ):
        """
        :说明:

            删除文件

        :必填:

            * ``id: int`` 文件夹id，空串为根目录

        :可选:

            * ``path: str`` 文件夹路径，文件夹允许重名，不保证准确，准确定位使用 id
            * ``target: int`` 群号或好友 qq 号
            * ``group: int`` 群号
            * ``qq: int`` 好友 qq 号
        """
        ...

    async def file_move(
        self, *,
        id: str,
        path: Optional[str],
        target: Optional[int],
        group: Optional[int],
        qq: Optional[int],
        move_to: Optional[str],
        move_to_path: Optional[str]
    ):
        """
        :说明:

            移动文件

        :必填:

            * ``id: int`` 文件夹id，空串为根目录

        :可选:

            * ``path: str`` 文件夹路径，文件夹允许重名，不保证准确，准确定位使用 id
            * ``target: int`` 群号或好友 qq 号
            * ``group: int`` 群号
            * ``qq: int`` 好友 qq 号
            * ``move_to: str`` 移动目标文件夹 id
            * ``move_to_path: str`` 移动目标文件夹路径,文件夹允许重名,不保证准确,准确定位使用 move_to 参数
        """
        ...

    async def file_rename(
        self, *,
        id: str,
        path: Optional[str],
        target: Optional[int],
        group: Optional[int],
        qq: Optional[int],
        rename_to: Optional[int]
    ):
        """
        :说明:

            重命名文件

        :必填:

            * ``id: int`` 文件夹id，空串为根目录

        :可选:

            * ``path: str`` 文件夹路径，文件夹允许重名，不保证准确，准确定位使用 id
            * ``target: int`` 群号或好友 qq 号
            * ``group: int`` 群号
            * ``qq: int`` 好友 qq 号
            * ``rename_to: int`` 新文件名
        """
        ...

    async def delete_friend(self, *, target: int):
        """
        :说明:

            删除好友

        :参数:

            * ``target: int`` 好友 id
        """
        ...

    async def mute(
        self, *,
        target: int,
        member_id: int,
        time: int
    ):
        """
        :说明:

            禁言群 target 的 member_id 成员 time 秒

        :参数:

            * ``target: int`` 群 id
            * ``member_id: int`` 成员 id
            * ``time: int`` 时长(单位秒)
        """
        ...

    async def unmute(self, *, target: int, member_id: int):
        """
        :说明:

            解除群成员禁言

        :参数:

            * ``target: int`` 群 id
            * ``member_id: int`` 成员 id
        """
        ...

    async def kick(
        self, *,
        target: int,
        member_id: int,
        msg: Optional[str]
    ):
        """
        :说明:

            移除群成员

        :必填:

            * ``target: int`` 群 id
            * ``member_id: int`` 成员 id

        :可选:

            * ``msg: str`` 信息
        """
        ...

    async def quit(self, *, target: int):
        """
        :说明:

            退出群聊

        :参数:

            * ``target: int`` 群 id
        """
        ...

    async def mute_all(self, *, target: int):
        """
        :说明:

            全体禁言

        :参数:

            * ``target: int`` 群 id
        """
        ...

    async def unmute_all(self, *, target: int):
        """
        :说明:

            解除全体禁言

        :参数:

            * ``target: int`` 群 id
        """
        ...

    async def set_essence(self, *, target: int, message_id: int):
        """
        :说明:

            设置**群消息** id 为精华消息

        :参数:

            * ``target: int`` 群号
            * ``message_id: int`` 消息号
        """
        ...

    @overload
    async def group_config(
        self, *,
        subcommand: Literal["get", "update"],
        target: int,
    ):
        """
        :说明:

            获取群设置(当 subcommand="get" 时)

        :参数:

            * ``subcommand: str`` 只可以使用 "get"
            * ``target: int`` 群 id
        """
        ...

    @overload
    async def group_config(
        self, *,
        subcommand: Literal["get", "update"],
        target: int,
        config: dict,
    ):
        """
        :说明:

            修改群设置(当 subcommand="update" 时)

        :参数:

            * ``subcommand: str`` 只可以使用 "update"
            * ``target: int`` 群 id
            * ``config: dict`` 群设置 dict
        :config 例子:
            {
                "name": "群名称",
                "announcement": "群公告",
                "confessTalk": True, # 是否开启坦白说
                "allowMemberInvite": True # 是否允许群员邀请
                "autoApprove": True # 是否开启自动审批入群
                "anonymousChat": True # 是否允许匿名聊天
            }
        """
        ...

    async def member_info(self, *, target: int):
        """
        :说明:

            群员设置相关(暂不支持)

        :参数:

            * ``target: int`` 群 id
        """
        ...

    async def member_admin(
        self, *,
        target: int,
        member_id: int,
        assign: bool
    ):
        """
        :说明:

            修改群员管理员权限

        :参数:

            * ``target: int`` 群 id
            * ``member_id: int`` 群成员 id
            * ``assign: bool`` 是否设置为管理员
        """
        ...

    async def anno_list(
        self, *,
        id: int,
        offset: Optional[int],
        size: Optional[int]
    ):
        """
        :说明:

            获取群公告

        :参数:

            * ``id: int`` 群 id
            * ``offset: int`` 分页参数
            * ``size: int`` 分页参数 默认10
        """
        ...

    async def anno_publish(
        self, *,
        target: int,
        content: str,
        send_to_new_member: Optional[bool],
        pinned: Optional[bool],
        show_edit_card: Optional[bool],
        show_popup: Optional[bool],
        require_confirmation: Optional[bool],
        image_url: Optional[str],
        image_path: Optional[str],
        image_base64: Optional[str]
    ):
        """
        :说明:

            发送群公告

        :参数:

            * ``target: int`` 群号
            * ``content: str`` 公告内容
            * ``send_to_new_member`` 是否发送给新成员
            * ``pinned: bool`` 是否置顶
            * ``showEditCard: bool`` 是否显示群成员修改群名片的引导
            * ``showPopup: bool`` 是否自动弹出
            * ``requireConfirmation: bool`` 是否需要群成员确认
            * ``imageUrl: str`` 公告图片 url
            * ``imagePath: str`` 公告图片本地路径
            * ``imageBase64: str`` 公告图片 base64 编码
        """
        ...

    async def anno_delete(
        self, *, id: int, fid: str
    ):
        """
        :说明:

            删除群公告

        :参数:

            * ``id: int`` 群号
            * ``fid: str`` 群公告唯一 id
        """
        ...

    async def resp_newFriendRequestEvent(
        self, *,
        event_id: int,
        group_id: int,
        from_id: int,
        operate: int,
        message: str
    ):
        """
        :说明:

            处理添加好友事件

        :参数:

            * ``event_id: int`` 事件 id
            * ``group_id: int`` 群 id
            * ``from_id: int`` 事件对应申请人 qq id
            * ``operate: int`` 响应操作类型： 0 同意  1 拒绝  2 拒绝并加入黑名单
            * ``message: str`` 回复的消息内容
        """
        ...

    async def resp_memberJoinRequestEvent(
        self, *,
        event_id: int,
        group_id: int,
        from_id: int,
        operate: int,
        message: str
    ):
        """
        :说明:

            处理用户入群申请事件

        :参数:

            * ``event_id: int`` 事件 id
            * ``group_id: int`` 群 id
            * ``from_id: int`` 事件对应申请人 qq id
            * ``operate: int`` 响应操作类型： 0 同意入群  1 拒绝入群  2 忽略请求  3 拒绝入群并加入黑名单  4 忽略请求并加入黑名单  # noqa
            * ``message: str`` 回复的消息内容
        """
        ...

    async def resp_botInvitedJoinGroupRequestEvent(
        self, *,
        event_id: int,
        group_id: int,
        from_id: int,
        operate: int,
        message: str
    ):
        """
        :说明:

            处理 bot 被邀请入群事件

        :参数:

            * ``event_id: int`` 事件 id
            * ``group_id: int`` 群 id
            * ``from_id: int`` 事件对应申请人 qq id
            * ``operate: int`` 响应操作类型： 0 同意邀请  1 拒绝邀请
            * ``message: str`` 回复的消息内容
        """
        ...
