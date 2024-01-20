import dataclasses
from typing import Any


@dataclasses.dataclass
class SuccessLogin:
    data: Any
    loggedIn: str = True


@dataclasses.dataclass
class ErrorLogin:
    data: str
    loggedIn: str = False

@dataclasses.dataclass
class ErrorRegister:
    data: str
    registered: str = False

@dataclasses.dataclass
class SuccessRegister:
    data: str
    registered: str = True

def success(data):
    return {
        "success": True,
        "data": data
    }


def failed(data):
    return {
        "success": False,
        "data": data
    }
