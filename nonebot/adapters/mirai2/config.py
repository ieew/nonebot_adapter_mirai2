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
    """

    verify_key: str = Field(
        ..., alias="mirai_verify_key"
    )
    mirai_host: str
    mirai_port: str
    mirai_qq: List[int]

    class Config:
        extra = Extra.ignore
        allow_population_by_field_name = True
