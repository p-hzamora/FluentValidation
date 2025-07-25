class PolishLanguage:
    Culture: str = "pl"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "Pole '{PropertyName}' nie zawiera poprawnego adresu email.",
            "GreaterThanOrEqualValidator": "Wartość pola '{PropertyName}' musi być równa lub większa niż '{ComparisonValue}'.",
            "GreaterThanValidator": "Wartość pola '{PropertyName}' musi być większa niż '{ComparisonValue}'.",
            "LengthValidator": "Długość pola '{PropertyName}' musi zawierać się pomiędzy {min_length} i {max_length} znaki(ów). Wprowadzono {total_length} znaki(ów).",
            "MinimumLengthValidator": "Długość pola '{PropertyName}' musi być większa lub równa {min_length} znaki(ów). Wprowadzono {total_length} znaki(ów).",
            "MaximumLengthValidator": "Długość pola '{PropertyName}' musi być mniejsza lub równa {max_length} znaki(ów). Wprowadzono {total_length} znaki(ów).",
            "LessThanOrEqualValidator": "Wartość pola '{PropertyName}' musi być równa lub mniejsza niż '{ComparisonValue}'.",
            "LessThanValidator": "Wartość pola '{PropertyName}' musi być mniejsza niż '{ComparisonValue}'.",
            "NotEmptyValidator": "Pole '{PropertyName}' nie może być puste.",
            "NotEqualValidator": "Pole '{PropertyName}' nie może być równe '{ComparisonValue}'.",
            "NotNullValidator": "Pole '{PropertyName}' nie może być puste.",
            "PredicateValidator": "Określony warunek nie został spełniony dla pola '{PropertyName}'.",
            "AsyncPredicateValidator": "Określony warunek nie został spełniony dla pola '{PropertyName}'.",
            "RegularExpressionValidator": "'{PropertyName}' wprowadzono w niepoprawnym formacie.",
            "EqualValidator": "Wartość pola '{PropertyName}' musi być równa '{ComparisonValue}'.",
            "ExactLengthValidator": "Pole '{PropertyName}' musi posiadać długość {max_length} znaki(ów). Wprowadzono {total_length} znaki(ów).",
            "InclusiveBetweenValidator": "Wartość pola '{PropertyName}' musi zawierać się pomiędzy {From} i {To}. Wprowadzono {PropertyValue}.",
            "ExclusiveBetweenValidator": "Wartość pola '{PropertyName}' musi zawierać się pomiędzy {From} i {To} (wyłącznie). Wprowadzono {PropertyValue}.",
            "CreditCardValidator": "Pole '{PropertyName}' nie zawiera poprawnego numeru karty kredytowej.",
            "ScalePrecisionValidator": "Wartość pola '{PropertyName}' nie może mieć więcej niż {ExpectedPrecision} cyfr z dopuszczalną dokładnością {ExpectedScale} cyfr po przecinku. Znaleziono {Digits} cyfr i {ActualScale} cyfr po przecinku.",
            "EmptyValidator": "Pole '{PropertyName}' musi być puste.",
            "NullValidator": "Pole '{PropertyName}' musi być puste.",
            "EnumValidator": "Pole '{PropertyName}' ma zakres wartości, który nie obejmuje {PropertyValue}.",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "Długość pola '{PropertyName}' musi zawierać się pomiędzy {min_length} i {max_length} znaki(ów).",
            "MinimumLength_Simple": "Długość pola '{PropertyName}' musi być większa lub równa {min_length} znaki(ów).",
            "MaximumLength_Simple": "Długość pola '{PropertyName}' musi być mniejsza lub równa {max_length} znaki(ów).",
            "ExactLength_Simple": "Pole '{PropertyName}' musi posiadać długość {max_length} znaki(ów).",
            "InclusiveBetween_Simple": "Wartość pola '{PropertyName}' musi zawierać się pomiędzy {From} i {To}.",
        }
        return dicc.get(key, None)
