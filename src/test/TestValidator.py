from typing import Callable, overload
import sys
from pathlib import Path
from person import Person


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())
from FluentValidation.InlineValidator import InlineValidator  # noqa: E402


class TestValidator(InlineValidator[Person]):
    @overload
    def __init__(self): ...

    @overload
    def __init__(self, *actions: Callable[["TestValidator"], None]): ...

    def __init__(self, *actions: Callable[["TestValidator"], None]):
        super().__init__()
        for action in actions:
            action(self)
