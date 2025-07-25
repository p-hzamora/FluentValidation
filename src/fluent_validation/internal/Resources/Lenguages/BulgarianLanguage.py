class BulgarianLanguage:
    Culture: str = "bg"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' не е валиден е-мейл адрес.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' трябва да бъде по-голямо или равно на  '{ComparisonValue}'.",
            "GreaterThanValidator": "'{PropertyName}' трябва да бъде по-голямо от '{ComparisonValue}'.",
            "LengthValidator": "'{PropertyName}' символите трябва да бъдат между {min_length} и {max_length}. Въведохте {total_length} знака.",
            "MinimumLengthValidator": "Дължината на '{PropertyName}' трябва да бъде най-малко {min_length} брой символи. Въведохте {total_length} знака.",
            "MaximumLengthValidator": "Дължината на '{PropertyName}' трябва да бъде  {max_length} брой символи. Въведохте {total_length} знака.",
            "LessThanOrEqualValidator": "'{PropertyName}' трябва да бъде по-малко или равно на '{ComparisonValue}'.",
            "LessThanValidator": "'{PropertyName}' трябва да бъде по-малко от '{ComparisonValue}'.",
            "NotEmptyValidator": "'{PropertyName}' не трябва да бъде празно.",
            "NotEqualValidator": "'{PropertyName}' не трябва да бъде равно на '{ComparisonValue}'.",
            "NotNullValidator": "'{PropertyName}' не трябва да бъде празно.",
            "PredicateValidator": "Специалните изисквания за '{PropertyName}' не са спазени.",
            "AsyncPredicateValidator": "Специалните изисквания за '{PropertyName}' не са спазени.",
            "RegularExpressionValidator": "'{PropertyName}' не е в правилния формат.",
            "EqualValidator": "'{PropertyName}' трябва да бъде равно на '{ComparisonValue}'.",
            "ExactLengthValidator": "'{PropertyName}' трябва да бъде {max_length} брой на символите. Въведохте {total_length} знака.",
            "InclusiveBetweenValidator": "'{PropertyName}' трябва да бъде между {From} и {To}. Вие въведохте {PropertyValue}.",
            "ExclusiveBetweenValidator": "'{PropertyName}' трябва да бъде между {From} и {To} (изключително). Вие въведохте {PropertyValue}.",
            "CreditCardValidator": "'{PropertyName}' не е валиден номер на кредитна карта.",
            "ScalePrecisionValidator": "'{PropertyName}' не трябва да е повече от {ExpectedPrecision} цифри и трябва да бъде до {ExpectedScale} знака след запетаята. В момента има {Digits} цифри и {ActualScale} знака след запетаята.",
            "EmptyValidator": "'{PropertyName}' трябва да бъде празно.",
            "NullValidator": "'{PropertyName}' трябва да бъде празно.",
            "EnumValidator": "'{PropertyName}' има диапазон, които не обхващат '{PropertyValue}'.",
            #  Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' трябва да бъде межди {min_length} и {max_length} брой символи.",
            "MinimumLength_Simple": "Дължината на '{PropertyName}' трябва да бъде поне {min_length} символи.",
            "MaximumLength_Simple": "Дължината на '{PropertyName}' трябва да бъде {max_length} или по-малко брой символи.",
            "ExactLength_Simple": "'{PropertyName}' трябва да бъде {max_length} дължина на символите.",
            "InclusiveBetween_Simple": "'{PropertyName}' трябва да бъде между {From} и {To}.",
        }
        return dicc.get(key, None)
