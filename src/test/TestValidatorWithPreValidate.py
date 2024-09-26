from typing import Callable, override
import sys
from pathlib import Path
from person import Person


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())
from fluent_validation.InlineValidator import InlineValidator  # noqa: E402
from fluent_validation.syntax import IRuleBuilderOptions  # noqa: E402
from fluent_validation import ValidationContext, ValidationResult


class TestValidatorWithPreValidate(InlineValidator[Person]):
    def __init__[TProperty](
        self,
        PreValidateMethod: Callable[[ValidationContext[Person], ValidationResult], bool] = None,
        *ruleCreator: Callable[[InlineValidator[Person]], IRuleBuilderOptions[Person, TProperty]],
    ) -> None:
        super().__init__(Person, *ruleCreator)

        self.PreValidateMethod: None| Callable[[ValidationContext[Person], ValidationResult], bool] = PreValidateMethod

    @override
    def PreValidate(self, context: ValidationContext[Person], result: ValidationResult) -> bool:
        if self.PreValidateMethod is not None:
            return self.PreValidateMethod(context, result)
        return super().PreValidate(context, result)
