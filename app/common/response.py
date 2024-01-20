import dataclasses


@dataclasses.dataclass
class SuccessLogin:
    data: str
    loggedIn: str = True


@dataclasses.dataclass
class ErrorLogin:
    data: str
    loggedIn: str = False


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
