from typing import Callable, overload

from stc.common.scripts.FluentValidation.abstract_validator import AbstractValidator
from stc.common.scripts.FluentValidation.syntax import IRuleBuilderOptions

class InlineValidator[T](AbstractValidator[T]):
    def __init__(self)->None:
        super().__init__()

    def Add[TProperty](self, ruleCreator:Callable[["InlineValidator"], IRuleBuilderOptions[T, TProperty]]):
        ruleCreator(self)
