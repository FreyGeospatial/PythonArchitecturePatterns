from collections import namedtuple
from dataclasses import dataclass
from typing import NamedTuple


class Money(NamedTuple):
    """Inherits from named tuple class"""
    currency: str
    value: int