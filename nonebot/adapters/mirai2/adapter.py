import json
import asyncio
import contextlib
from typing import Any, Dict, List, Optional, Literal, cast

from nonebot.utils import escape_tag
from nonebot.adapters import Adapter as BaseAdapter
from nonebot.exception import ActionFailed, WebSocketClosed
from nonebot.drivers import (
    URL,
    Driver,
    Request,
    WebSocket,
    ReverseDriver,
    ForwardDriver,
    WebSocketServerSetup
)

from . import log
from .bot import Bot
from .config import Config
from .event import Event
from .utils import (
    SyncIDStore,
    process_event,
    snake_to_camel,
    MiraiDataclassEncoder
)

class Adapter(BaseAdapter):

    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        self.mirai_config: Config = Config(**self.config.dict())
        self.connections: Dict[str, WebSocket] = {}
        self.tasks: List["asyncio.Task"] = []
        self.setup()

    @classmethod
    def get_name(cls):
        return "mirai2"
    
    def setup(self) -> None:
        if isinstance(self.driver, ReverseDriver):
            self.setup_websocket_server(
                WebSocketServerSetup(
                    URL("/mirai2/ws"), self.get_name(), self._handle_ws_server
                )
            )

        if isinstance(self.driver, ForwardDriver) and self.mirai_config.mirai_Forward:
            if not all([
                isinstance(self.mirai_config.verify_key, str),
                isinstance(self.mirai_config.mirai_host, str),
                isinstance(self.mirai_config.mirai_port, int),
                isinstance(self.mirai_config.mirai_qq, list),
            ]):
                raise ValueError("请检查环境变量中的 Verify_key, Mirai_host, Mirai_port, Mirai_qq 是否异常")
            self.driver.on_startup(self._start_ws_client)
            self.driver.on_shutdown(self._stop_ws_client)

    async def _handle_ws_server(self, websocket: WebSocket):
        access_token = self.mirai_config.mirai_access_token
        if access_token is not None:
            if access_token != websocket.request.headers.get("access_token", ""):
                await websocket.close(code=1000, reason="access_token error")
                return

        await websocket.accept()

        await websocket.send(json.dumps({"syncId": "-1", "command": "botList", "content": {}}))
        bot_list = json.loads(await websocket.receive()).get("data", {}).get("data", [])

        qqid = websocket.request.headers.get("qq")
        if int(qqid) not in bot_list:
            await websocket.close(code=1000, reason=f"账号 {qqid} 未在客户端登录")
            return
        
        await websocket.send(json.dumps({
            "syncId": "-1", "command": "verify", "content": {
                "verifyKey": self.mirai_config.verify_key,
                "sessionKey": None,
                "qq": qqid
            }
        }))
        code = json.loads(await websocket.receive()).get("data", {})
        if code.get("code"):
            log.error(f"{qqid}, {code}")
            return
        
        bot = Bot(self, qqid)
        self.bot_connect(bot)
        self.connections[qqid] = websocket
        log.info(f"({bot.self_id}) connection ...")

        try:
            while True:
                data = await websocket.receive()
                json_data = json.loads(data)
                if json_data.get("data"):
                    self._event_handle(bot, json_data)
        except WebSocketClosed as e:
            qqid = ", ".join(self.connections)
            log.warning(f"WebSocket for Bot {escape_tag(qqid)} closed by peer")
        except Exception as e:
            log.error(f"<r><bg #f8bbd0>Error while process data from websocket "
                f"for bot {escape_tag(bot.self_id)}.</bg #f8bbd0></r>", e)
        finally:
            with contextlib.suppress(Exception):
                await websocket.close()
            self.connections.pop(qqid, None)
            self.bot_disconnect(bot=bot)

    async def _start_ws_client(self):
        for qq in self.mirai_config.mirai_qq:
            try:
                ws_url = URL(f"ws://{self.mirai_config.mirai_host}:{self.mirai_config.mirai_port}/all")
                self.tasks.append(asyncio.create_task(self._ws_client(qq, ws_url)))
            except Exception as e:
                log.error(f"<r><bg #f8bbd0>Bad url {escape_tag(str(ws_url))} "
                    "in mirai2 forward websocket config</bg #f8bbd0></r>",
                    e)

    async def _stop_ws_client(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()

    async def _ws_client(self, qq: str, url: URL):
        headers = {
            "verifyKey": self.mirai_config.verify_key,
            "qq": qq
        }
        request = Request(
            "GET",
            url=url,
            headers=headers,
            timeout=3
        )

        while True:
            try:
                async with self.websocket(request) as ws:
                    log.debug(f"WebSocket Connection to {escape_tag(str(url))} established")
                    try:
                        bot = Bot(self, qq)
                        self.connections[qq] = ws
                        self.bot_connect(bot)
                        log.info(f"<y>Bot {escape_tag(qq)}</y> connected")

                        data = json.loads(await ws.receive()).get("data", {})
                        if data.get("code") > 0:
                            log.warning(f'{json_data["data"]["msg"]}: {qq}')
                            return

                        while True:
                            data = await ws.receive()
                            json_data = json.loads(data)
                            self._event_handle(bot, json_data)
                    except WebSocketClosed as e:
                        log.error("<r><bg #f8bbd0>WebSocket Closed</bg #f8bbd0></r>", e)
                    except Exception as e:
                        log.error("<r><bg #f8bbd0>Error while process data from websocket"
                            f"{escape_tag(str(url))}. Trying to reconnect...</bg #f8bbd0></r>",
                            e
                        )
                    finally:
                        self.connections.pop(qq, None)
                        self.bot_disconnect(bot)
            except Exception as e:
                log.error("<r><bg #f8bbd0>Error while setup websocket to "
                    f"{escape_tag(str(url))}. Trying to reconnect...</bg #f8bbd0></r>",
                    e
                )
            await asyncio.sleep(3)

    def _event_handle(self, bot: Bot, event: Dict):
        if int(event.get("syncId") or "0") >= 0:
            SyncIDStore.add_response(event)
            return
        asyncio.create_task(process_event(
            bot,
            event=Event.new({
                **event["data"],
                "self_id": bot.self_id
            })
        ))

    async def _call_api(self, bot: Bot, api: str,
        subcommand: Optional[Literal['get', 'update']] = None, **data: Any) -> Any:
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