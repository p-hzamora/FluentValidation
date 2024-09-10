from typing import Any, Callable


class MemberInfo:
    def __init__(self, func: Callable[..., Any]) -> None:
        self._func: Callable[..., Any] = func

    @property
    def Name(self):
        return self._func.__name__
