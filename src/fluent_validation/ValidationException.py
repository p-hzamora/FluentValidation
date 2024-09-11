from fluent_validation.results.ValidationFailure import ValidationFailure


class ValidationException(Exception):
    # def __init__(self, message:str ):
    # 	this(message, Enumerable.Empty<ValidationFailure>())

    # def __init__(self, message:str , errors:list[ValidationFailure]) : base(message) {
    # 	Errors = errors
    # }

    # def __init__(self, message:str , errors:list[ValidationFailure], bool appendDefaultMessage)
    # 	: base(appendDefaultMessage ? $"{message} {BuildErrorMessage(errors)}" : message) {
    # 	Errors = errors
    # }

    # def __init__(self, errors:list[ValidationFailure]) : base(BuildErrorMessage(errors)) {
    # 	Errors = errors
    # }

    def __init__(self, *, message: str = None, errors: list[ValidationFailure] = [], appendDefaultMessage: bool = False):
        if not message:
            self.message = self.BuildErrorMessage(errors)
        else:
            self.message: str = message

        self.Errors: list[ValidationFailure] = errors
        self.appendDefaultMessage = appendDefaultMessage

    @staticmethod
    def BuildErrorMessage(errors: list[ValidationFailure]) -> str:
        arr = [f"\n -- {x.PropertyName}: {x.ErrorMessage} Severity: {x.Severity.name}" for x in errors]
        return "Validation failed: " + "".join(arr)

    # 	ValidationException(SerializationInfo info, StreamingContext context) : base(info, context) {
    # 		Errors = info.GetValue("errors", typeof(list[ValidationFailure])) as list[ValidationFailure]
    # 	}

    # 	override void GetObjectData(SerializationInfo info, StreamingContext context) {
    # 		if (info == null) throw new ArgumentNullException("info")

    # 		info.AddValue("errors", Errors)
    # 		base.GetObjectData(info, context)
    # 	}
    # }

    def __str__(self) -> str:
        return self.message
