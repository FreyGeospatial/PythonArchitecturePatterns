from collections import namedtuple
from dataclasses import dataclass
from typing import NamedTuple


class Money(NamedTuple):
    """Inherits from named tuple class"""
    currency: str
    value: int

@dataclass(frozen=True) 
class Name:
    """Name is a value object, as it is identified by, well, its name! if you change the name, the name is no longer the same"""
    first_name: str
    surname: str

class Person:
    """person is an entity. If you change the name, the person remains the same"""
    def __init__(self, name: Name):
        self.name = name