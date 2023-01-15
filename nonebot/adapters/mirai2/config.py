from typing import List, Optional

from pydantic import Field, Extra, BaseModel


class Config(BaseModel):
    """
    mirai2 配置类

    :配置项:

      - ``verify_key`` / ``mirai_verify_key``: mirai-api-http 的 verify_key
      - ``mirai_host``: mirai-api-http 的地址
      - ``mirai_port``: mirai-api-http 的端口
      - ``mirai_qq``: mirai-api-http qq 列表
      - ``mirai_reverse``: 是否启用正向 ws
      - ``mirai_access_token``: 反向 ws 专用的对客户端鉴权 token
    """

    verify_key: str = Field(
        None, alias="mirai_verify_key"
    )
    mirai_host: Optional[str] = None
    mirai_port: Optional[int] = None
    mirai_qq: Optional[List[str]] = None
    mirai_Forward: Optional[bool] = True
    mirai_access_token: Optional[str] = None

    class Config:
        extra = Extra.ignore
        allow_population_by_field_name = True
