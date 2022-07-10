from typing import Optional
from nonebot.utils import logger_wrapper

log = logger_wrapper("mirai2")


def info(message: str, exception: Optional[Exception] = None):
    log("INFO", message=message, exception=exception)


def warning(message: str, exception: Optional[Exception] = None):
    log("WARNING", message=message, exception=exception)


def warn(message: str, exception: Optional[Exception] = None):
    log("WARNING", message=message, exception=exception)


def debug(message: str, exception: Optional[Exception] = None):
    log("DEBUG", message=message, exception=exception)


def error(message: str, exception: Optional[Exception] = None):
    log("ERROR", message=message, exception=exception)
