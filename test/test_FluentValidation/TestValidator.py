from typing import Callable, overload

from stc.common.scripts.FluentValidation.InlineValidator import InlineValidator
from person import Person 



class TestValidator(InlineValidator[Person]):
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, *actions:Callable[["TestValidator"],None]): ...
    
    def __init__(self, *actions:Callable[["TestValidator"],None]):
        super().__init__()
        for action in actions:
            action(self)