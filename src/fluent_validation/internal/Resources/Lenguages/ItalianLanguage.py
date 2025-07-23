class ItalianLanguage:
    Culture: str = "it"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' non è un indirizzo email valido.",
            "EqualValidator": "'{PropertyName}' dovrebbe essere uguale a '{ComparisonValue}'.",
            "ExactLengthValidator": "'{PropertyName}' deve essere lungo {max_length} caratteri. Hai inserito {total_length} caratteri.",
            "ExclusiveBetweenValidator": "'{PropertyName}' deve essere compreso tra {From} e {To} (esclusi). Hai inserito {PropertyValue}.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' deve essere maggiore o uguale a '{ComparisonValue}'.",
            "GreaterThanValidator": "'{PropertyName}' deve essere maggiore di '{ComparisonValue}'.",
            "InclusiveBetweenValidator": "'{PropertyName}' deve essere compreso tra {From} e {To}. Hai inserito {PropertyValue}.",
            "LengthValidator": "'{PropertyName}' deve essere lungo tra i {min_length} e {max_length} caratteri. Hai inserito {total_length} caratteri.",
            "MinimumLengthValidator": "'{PropertyName}' deve essere maggiore o uguale a {min_length} caratteri. Hai inserito {total_length} caratteri.",
            "MaximumLengthValidator": "'{PropertyName}' deve essere minore o uguale a {max_length} caratteri. Hai inserito {total_length} caratteri.",
            "LessThanOrEqualValidator": "'{PropertyName}' deve essere minore o uguale a '{ComparisonValue}'.",
            "LessThanValidator": "'{PropertyName}' deve essere minore di '{ComparisonValue}'.",
            "NotEmptyValidator": "'{PropertyName}' non può essere vuoto.",
            "NotEqualValidator": "'{PropertyName}' non può essere uguale a '{ComparisonValue}'.",
            "NotNullValidator": "'{PropertyName}' non può essere vuoto.",
            "PredicateValidator": "La condizione non è verificata per '{PropertyName}'.",
            "AsyncPredicateValidator": "La condizione non è verificata per '{PropertyName}'.",
            "RegularExpressionValidator": "'{PropertyName}' non è nel formato corretto.",
            "CreditCardValidator": "'{PropertyName}' non è un numero di carta di credito valido.",
            "ScalePrecisionValidator": "'{PropertyName}' non può avere più di {ExpectedPrecision} cifre in totale, con una tolleranza per {ExpectedScale} decimali. Sono state trovate {Digits} cifre e {ActualScale} decimali.",
            "EmptyValidator": "'{PropertyName}' dovrebbe essere vuoto.",
            "NullValidator": "'{PropertyName}' dovrebbe essere vuoto.",
            "EnumValidator": "'{PropertyName}' ha un intervallo di valori che non include '{PropertyValue}'.",
            # Additional fallback messages used by clientside validation integration.
            "ExactLength_Simple": "'{PropertyName}' deve essere lungo {max_length} caratteri.",
            "InclusiveBetween_Simple": "'{PropertyName}' deve essere compreso tra {From} e {To}.",
            "Length_Simple": "'{PropertyName}' deve essere lungo tra i {min_length} e {max_length} caratteri.",
            "MinimumLength_Simple": "'{PropertyName}' deve essere maggiore o uguale a {min_length} caratteri.",
            "MaximumLength_Simple": "'{PropertyName}' deve essere minore o uguale a {max_length} caratteri.",
        }
        return dicc.get(key, None)
