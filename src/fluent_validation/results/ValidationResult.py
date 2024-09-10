from __future__ import annotations
from typing import Iterable, Optional, overload
from collections import defaultdict

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ValidationFailure import ValidationFailure


class ValidationResult:
    @overload
    def __init__(self): ...

    @overload
    def __init__(self, failures: Iterable[ValidationFailure]): ...

    @overload
    def __init__(self, errors: list[ValidationFailure]): ...

    @overload
    def __init__(self, otherResults: Iterable["ValidationResult"]): ...

    def __init__(
        self,
        errors: Optional[ValidationFailure] = None,
        failures: Optional[Iterable[ValidationFailure]] = None,
        otherResults: Optional[Iterable["ValidationResult"]] = None,
    ) -> None:
        self._rule_sets_executed: Optional[list[str]] = None
        if errors is None and failures is None:
            self._errors: list[ValidationFailure] = []

        elif errors is None and isinstance(failures, list):
            self._errors: list[ValidationFailure] = []
            for x in failures:
                if x is not None:
                    self._errors.append(x)

        elif isinstance(errors, list) and failures is None:
            self._errors: list[ValidationFailure] = errors

        elif not errors and not failures and otherResults:
            self._errors = [err for result in otherResults for err in result.errors]
            self._rule_sets_executed = list(set(rule_set for result in otherResults if result.RuleSetsExecuted is not None for rule_set in result.RuleSetsExecuted))
        else:
            raise Exception(f"No se ha inicializado la clase {self.__class__.__name__}")

    @property
    def is_valid(self) -> bool:
        return len(self._errors) == 0

    @property
    def errors(self) -> list[ValidationFailure]:
        return self._errors

    @property
    def RuleSetsExecuted(self) -> Optional[list[str]]:
        return self._rule_sets_executed

    @RuleSetsExecuted.setter
    def RuleSetsExecuted(self, value: Optional[list[str]]) -> None:
        self._rule_sets_executed = value

    def to_string(self, separator: str = "\n") -> str:
        string: list[str] = [f"{separator} {failure.ErrorMessage}" for failure in self._errors]
        return "".join(string)

    def to_dictionary(self) -> dict[str, list[str]]:
        Errors = defaultdict(list)
        for err in self._errors:
            Errors[err.PropertyName].append(err.ErrorMessage)
        return dict(Errors)
