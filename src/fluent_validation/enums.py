from enum import Enum, auto


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


# COMMENT: Replicated StringComparer C# enum
class StringComparer(Enum):
    Ordinal = lambda x, y: x == y  # noqa: E731
    OrdinalIgnoreCase = lambda x, y: x.lower() == y.lower()  # noqa: E731
