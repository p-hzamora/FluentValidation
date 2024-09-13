from enum import Enum, auto
from typing import Callable


class CascadeMode(Enum):
    Continue = auto()
    Stop = auto()


class ApplyConditionTo(Enum):
    AllValidators = auto()
    CurrentValidator = auto()


class Severity(Enum):
    Error = auto()
    Warning = auto()
    Info = auto()


def ordinal(x: str, y: str):
    return x == y


def ordinal_ignore_case(x: str, y: str):
    return x.lower() == y.lower()


# COMMENT: Replicated StringComparer C# enum
class StringComparer(Enum):
    Ordinal: Callable[[str, str], bool] = ordinal
    OrdinalIgnoreCase: Callable[[str, str], bool] = ordinal_ignore_case
