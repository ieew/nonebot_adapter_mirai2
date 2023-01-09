import asyncio
import json
import re
from typing import Any, Dict, List, Literal, Optional, cast
from nonebot.typing import overrides
from nonebot.exception import ActionFailed, WebSocketClosed
from nonebot.drivers import (
    URL,
    Driver,
    ForwardDriver,
    ReverseDriver,
    Request,
    WebSocket,
    WebSocketServerSetup,
)
from nonebot.adapters import Adapter as BaseAdapter

from .bot import Bot
from .event import Event
from .config import Config
from .utils import (
    MiraiDataclassEncoder,
    SyncIDStore,
    process_event
)
from . import log

RECONNECT_INTERVAL = 3.0


class Adapter(BaseAdapter):

    @overrides(BaseAdapter)
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        self.mirai_config: Config = Config(**self.config.dict())
        self.connections: Dict[str, WebSocket] = {}
        self.tasks: List['asyncio.Task'] = []
        self.setup()

    @classmethod
    @overrides(BaseAdapter)
    def get_name(cls) -> str:
        return 'mirai2'

    def setup(self) -> None:

        if self.mirai_config.mirai_reverse:
            if not isinstance(self.driver, ReverseDriver):
                log.error("mirai_reverse=True? 启用反向 ws 需要启用 fastapi 驱动器！")
                return
            self.setup_websocket_server(
                WebSocketServerSetup(
                    URL("/mirai2/ws"), self.get_name(), self._handle_ws_server
                )
            )
        else:
            if isinstance(self.driver, ForwardDriver):
                self.driver.on_startup(self.start_ws_client)
                self.driver.on_shutdown(self.stop_ws_client)
            else:
                log.error(f"{self.get_name()} 请添加 websockets 驱动以使用本 adapter")

    async def _handle_ws_server(self, ws: WebSocket):
        await ws.accept()

        await ws.send(json.dumps({"syncId": "-1", "command": "about", "content": {}}))
        state = json.loads(await ws.receive())
        if (state := state.get("data")) and not state.get("code"):
            if state["data"].get("version") < "2.7.0":
                await ws.close(code=1000)
        
        await ws.send(json.dumps({"syncId": "-1", "command": "botList", "content": {}}))
        data = json.loads(await ws.receive())
    
        bot_list = data["data"].get("data")

        if (qqid := ws.request.headers.get("qq")) and int(qqid) in bot_list:
            await ws.send(json.dumps(
                {
                    "syncId": "-1", "command": "verify", "content": {
                        "verifyKey": "6THQWK46d84w96h889uA",
                        "sessionKey": None,
                        "qq": qqid
                    }
                }
            ))
            data = await ws.receive()
        else:
            await ws.close(code=1001, reason=f"账号 {qqid} 未在客户端登录")
        try:
            
            bot = Bot(self, str(qqid))
            self.bot_connect(bot)
            self.connections[str(qqid)] = ws
            log.info(f"({bot.self_id}) connection ...")

            while True:
                data = await ws.receive()
                json_data = json.loads(data)
                if "data" in json_data:
                    await self.ws_event(ws, bot, json_data["data"])
        except WebSocketClosed:
            log.info(f"({bot.self_id}) clone ...")
        finally:
            self.connections.pop(qqid)
            self.bot_disconnect(bot)

    async def start_ws_client(self):
        for qq in self.mirai_config.mirai_qq:
            self.tasks.append(asyncio.create_task(self._client(qq)))

    async def stop_ws_client(self):
        for i in self.tasks:
            i.cancel()
        for qq, ws in self.connections.items():
            await ws.close()

    async def _client(self, self_qq: int):
        request = Request(
            "GET",
            URL("ws://{host}:{port}/all".format(
                host=self.mirai_config.mirai_host,
                port=self.mirai_config.mirai_port
            )),
            headers={
                "verifyKey": self.mirai_config.verify_key,
                "qq": self_qq
            },
            timeout=3
        )

        while True:
            try:
                async with self.websocket(request) as ws:
                    log.debug(
                        "WebSocket Connection to "
                        f'ws://{self.mirai_config.mirai_host}:{self.mirai_config.mirai_port}/all?'  # noqa
                        f'qq={self_qq} established'
                    )
                    data = await ws.receive()
                    json_data = json.loads(data)
                    if "data" in json_data and json_data.get("data")["code"] > 0:
                        log.warn(f'{json_data["data"]["msg"]}: {self_qq}')
                        return

                    bot = Bot(self, str(self_qq))
                    self.bot_connect(bot)
                    self.connections[str(self_qq)] = ws

                    await self.ws_event(ws, bot, json_data)

            except ConnectionRefusedError as e:
                log.warn(f"connection error ({self_qq}):{e} ")
                break
            await asyncio.sleep(3)

    async def ws_event(self, ws: WebSocket, bot: Bot, data: dict):

        while True:
            data = await ws.receive()
            json_data = json.loads(data)
            if int(json_data.get("syncId") or "0") >= 0:
                SyncIDStore.add_response(json_data)
                continue
            asyncio.create_task(process_event(
                bot,
                event=Event.new({
                    **json_data["data"],
                    "self_id": int(bot.self_id)
                })
            ))

    @overrides(BaseAdapter)
    async def _call_api(
        self,
        bot: Bot,
        api: str,
        subcommand: Optional[Literal['get', 'update']] = None,
        **data
    ) -> Any:

        def snake_to_camel(name: str):
            for i in ['anno', 'resp']:
                if re.match(i, name):
                    return name
            first, *rest = name.split('_')
            return ''.join([first.lower(), *(r.title() for r in rest)])

        sync_id = SyncIDStore.get_id()
        api = snake_to_camel(api)
        data = {snake_to_camel(k): v for k, v in data.items()}
        body = {
            'syncId': sync_id,
            'command': api,
            'subcommand': subcommand,
            'content': {
                **data,
            }
        }

        await cast(WebSocket, self.connections[str(bot.self_id)]).send(
            json.dumps(
                body,
                cls=MiraiDataclassEncoder
            )
        )

        result: Dict[str, Any] = await SyncIDStore.fetch_response(
            sync_id, timeout=self.config.api_timeout)

        if ('data') not in result or (result['data']).get('code') not in (None, 0):
            raise ActionFailed(
                f'{self.get_name()} | {result.get("data") or result}'
            )

        return result['data']
