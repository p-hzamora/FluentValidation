from typing import Callable, overload, override
from abc import ABC, abstractmethod
from fluent_validation.IValidationContext import ValidationContext
from fluent_validation.validators.PropertyValidator import PropertyValidator


class ILengthValidator(ABC):
    @property
    @abstractmethod
    def Min(self) -> int: ...

    @property
    @abstractmethod
    def Max(self) -> int: ...


class LengthValidator[T](PropertyValidator[T, str], ILengthValidator):
    @overload
    def __init__(min: int, max: int): ...

    @overload
    def __init__(min: Callable[[T], int], max: Callable[[T], int]): ...

    def __init__(self, min: int | Callable[[T], int], max: int | Callable[[T], int]):
        def _init_int(min: int, max: int):
            self._min: int = min
            self._max: int = max

            if max != -1 and max < min:
                raise Exception(f"({max}) Max should be larger than min ({min})")

        def _init_functions(min: Callable[[T], int], max: Callable[[T], int]):
            self._min_func = min
            self._max_func = max

        self._min: int = None
        self._max: int = None
        self._min_func: Callable[[T], int] = None
        self._max_func: Callable[[T], int] = None

        if isinstance(min, int) and (isinstance(max, int)):
            _init_int(min, max)
        else:
            _init_functions(min, max)

    @property
    def Min(self):
        return self._min

    @property
    def Max(self):
        return self._max

    @override
    def is_valid(self, context: ValidationContext[T], value: str) -> bool:
        if value is None:
            return True

        min = self.Min
        max = self.Max

        if self._max_func is not None and self._min_func is not None:
            max = self._max_func(context.instance_to_validate)
            min = self._min_func(context.instance_to_validate)

        length = len(value)

        if length < min or (length > max and max != -1):
            context.MessageFormatter.AppendArgument("min_length", min)
            context.MessageFormatter.AppendArgument("max_length", max)
            context.MessageFormatter.AppendArgument("total_length", length)
            return False
        return True

    @override
    def get_default_message_template(self, error_code: str) -> str:
        return self.Localized(error_code, self.Name)


class ExactLengthValidator[T](LengthValidator[T]):
    def __init__(self, length: int | Callable[[T], int]):
        super().__init__(length, length)


class MaximumLengthValidator[T](LengthValidator[T]):
    def __init__(self, length: int | Callable[[T], int]):
        super().__init__(0, length)


class MinimumLengthValidator[T](LengthValidator[T]):
    def __init__(self, length: int | Callable[[T], int]):
        super().__init__(length, -1)
