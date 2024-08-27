from typing import Type, Optional


class AsyncValidatorInvokedSynchronouslyException(RuntimeError):
    def __init__(self, validatorType: Optional[Type] = None, wasInvokedByAspNet: bool = False, message: Optional[str] = None):
        self.validatorType = validatorType if validatorType else type(None).__class__
        self.message = message if message else self.BuildMessage(validatorType, wasInvokedByAspNet)

    @staticmethod
    def BuildMessage(validatorType: Type, wasInvokedByAspNet: bool) -> str:
        if wasInvokedByAspNet:
            return f"Validator \"{validatorType.__name__}\" can't be used with ASP.NET automatic validation as it contains asynchronous rules. ASP.NET's validation pipeline is not asynchronous and can't invoke asynchronous rules. Remove the asynchronous rules in order for this validator to run."
        return f'Validator "{validatorType.__name__}" contains asynchronous rules but was invoked synchronously. Please call ValidateAsync rather than validate.'

    def __str__(self) -> str:
        return self.message
