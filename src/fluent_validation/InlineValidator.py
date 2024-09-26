from __future__ import annotations
from typing import Callable, Type

from .abstract_validator import AbstractValidator
from .syntax import IRuleBuilderOptions


class InlineValidator[T](AbstractValidator[T]):
    """
     Validator implementation that allows rules to be defined without inheriting from AbstractValidator.

     EXAMPLE
     -

    @dataclass
     public class Customer:
       Id: int
       Name: str

       public static readonly InlineValidator&lt;Customer&gt; Validator = new InlineValidator&lt;Customer&gt; {
         v =&gt; v.RuleFor(x =&gt; x.Name).NotNull(),
         v =&gt; v.RuleFor(x =&gt; x.Id).NotEqual(0),
       }
     }
    """

    def __init__[TProperty](self, model: Type[T], *ruleCreator: Callable[[InlineValidator[T]], IRuleBuilderOptions[T, TProperty]]) -> None:
        super().__init__(model)
        for rule in ruleCreator:
            rule(self)
