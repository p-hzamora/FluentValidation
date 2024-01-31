from typing import Callable

from .abstract_validator import AbstractValidator
from .syntax import IRuleBuilderOptions


class InlineValidator[T](AbstractValidator[T]):
    def __init__(self) -> None:
        super().__init__()

    def Add[TProperty](
        self,
        ruleCreator: Callable[["InlineValidator"], IRuleBuilderOptions[T, TProperty]],
    ):
        ruleCreator(self)
