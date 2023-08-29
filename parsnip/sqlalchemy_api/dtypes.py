from typing import Any

from sqlalchemy.orm import DeclarativeBase


def is_sqlalchemy_class(obj: Any) -> bool:
    return issubclass(obj, DeclarativeBase) or isinstance(obj, DeclarativeBase)
