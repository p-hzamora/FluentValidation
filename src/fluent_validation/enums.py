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
