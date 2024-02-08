from typing import Iterable, overload

from .ValidationFailure import ValidationFailure


class ValidationResult[T]:
    @overload
    def __init__(self):
        ...

    @overload
    def __init__(self, failures: Iterable[ValidationFailure]):
        ...

    @overload
    def __init__(self, errors: list[ValidationFailure]):
        ...

    def __init__(
        self,
        errors: ValidationFailure = None,
        failures: Iterable[ValidationFailure] = None,
    ) -> None:
        if errors is None and failures is None:
            self._errors: list[ValidationFailure] = []

        elif errors is None and isinstance(failures, list):
            self._errors: list[ValidationFailure] = []
            for x in failures:
                if x is not None:
                    self._errors.append(x)

        elif isinstance(errors, list) and failures is None:
            self._errors: list[ValidationFailure] = errors
        else:
            raise Exception(f"No se ha inicializado la clase {self.__class__.__name__}")

    @property
    def is_valid(self) -> bool:
        return len(self._errors) == 0

    @property
    def errors(self) -> list[ValidationFailure]:
        return self._errors
