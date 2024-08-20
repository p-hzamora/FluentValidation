class EnglishLanguage:
    Culture: str = "en"
    AmericanCulture: str = "en-US"
    BritishCulture: str = "en-GB"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' is not a valid email address.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' must be greater than or equal to '{ComparisonValue}'.",
            "GreaterThanValidator": "'{PropertyName}' must be greater than '{ComparisonValue}'.",
            "LengthValidator": "'{PropertyName}' must be between {min_length} and {max_length} characters. You entered {total_length} characters.",
            "MinimumLengthValidator": "The length of '{PropertyName}' must be at least {min_length} characters. You entered {total_length} characters.",
            "MaximumLengthValidator": "The length of '{PropertyName}' must be {max_length} characters or fewer. You entered {total_length} characters.",
            "LessThanOrEqualValidator": "'{PropertyName}' must be less than or equal to '{ComparisonValue}'.",
            "LessThanValidator": "'{PropertyName}' must be less than '{ComparisonValue}'.",
            "NotEmptyValidator": "'{PropertyName}' must not be empty.",
            "NotEqualValidator": "'{PropertyName}' must not be equal to '{ComparisonValue}'.",
            "NotNullValidator": "'{PropertyName}' must not be empty.",
            "PredicateValidator": "The specified condition was not met for '{PropertyName}'.",
            "AsyncPredicateValidator": "The specified condition was not met for '{PropertyName}'.",
            "RegularExpressionValidator": "'{PropertyName}' is not in the correct format.",
            "EqualValidator": "'{PropertyName}' must be equal to '{ComparisonValue}'.",
            "ExactLengthValidator": "'{PropertyName}' must be {max_length} characters in length. You entered {total_length} characters.",
            "InclusiveBetweenValidator": "'{PropertyName}' must be between {From} and {To}. You entered {PropertyValue}.",
            "ExclusiveBetweenValidator": "'{PropertyName}' must be between {From} and {To} (exclusive). You entered {PropertyValue}.",
            "CreditCardValidator": "'{PropertyName}' is not a valid credit card number.",
            "ScalePrecisionValidator": "'{PropertyName}' must not be more than {ExpectedPrecision} digits in total, with allowance for {ExpectedScale} decimals. {Digits} digits and {ActualScale} decimals were found.",
            "EmptyValidator": "'{PropertyName}' must be empty.",
            "NullValidator": "'{PropertyName}' must be empty.",
            "EnumValidator": "'{PropertyName}' has a range of values which does not include '{PropertyValue}'.",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' must be between {min_length} and {max_length} characters.",
            "MinimumLength_Simple": "The length of '{PropertyName}' must be at least {min_length} characters.",
            "MaximumLength_Simple": "The length of '{PropertyName}' must be {max_length} characters or fewer.",
            "ExactLength_Simple": "'{PropertyName}' must be {max_length} characters in length.",
            "InclusiveBetween_Simple": "'{PropertyName}' must be between {From} and {To}.",
        }
        return dicc.get(key, None)
