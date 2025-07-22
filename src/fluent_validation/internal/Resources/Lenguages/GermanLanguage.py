class GermanLanguage:
    Culture: str = "de"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' ist keine gültige E-Mail-Adresse.",
            "GreaterThanOrEqualValidator": "Der Wert von '{PropertyName}' muss grösser oder gleich '{ComparisonValue}' sein.",
            "GreaterThanValidator": "Der Wert von '{PropertyName}' muss grösser sein als '{ComparisonValue}'.",
            "LengthValidator": "Die Länge von '{PropertyName}' muss zwischen {min_length} und {max_length} Zeichen liegen. Es wurden {total_length} Zeichen eingetragen.",
            "MinimumLengthValidator": "Die Länge von '{PropertyName}' muss größer oder gleich {min_length} sein. Sie haben {total_length} Zeichen eingegeben.",
            "MaximumLengthValidator": "Die Länge von '{PropertyName}' muss kleiner oder gleich {max_length} sein. Sie haben {total_length} Zeichen eingegeben.",
            "LessThanOrEqualValidator": "Der Wert von '{PropertyName}' muss kleiner oder gleich '{ComparisonValue}' sein.",
            "LessThanValidator": "Der Wert von '{PropertyName}' muss kleiner sein als '{ComparisonValue}'.",
            "NotEmptyValidator": "'{PropertyName}' darf nicht leer sein.",
            "NotEqualValidator": "'{PropertyName}' darf nicht '{ComparisonValue}' sein.",
            "NotNullValidator": "'{PropertyName}' darf kein Nullwert sein.",
            "PredicateValidator": "Der Wert von '{PropertyName}' entspricht nicht der festgelegten Bedingung.",
            "AsyncPredicateValidator": "Der Wert von '{PropertyName}' entspricht nicht der festgelegten Bedingung.",
            "RegularExpressionValidator": "'{PropertyName}' weist ein ungültiges Format auf.",
            "EqualValidator": "'{PropertyName}' muss gleich '{ComparisonValue}' sein.",
            "ExactLengthValidator": "'{PropertyName}' muss genau {max_length} lang sein. Es wurden {total_length} eingegeben.",
            "ExclusiveBetweenValidator": "'{PropertyName}' muss zwischen {From} und {To} sein (exklusiv). Es wurde {PropertyValue} eingegeben.",
            "InclusiveBetweenValidator": "'{PropertyName}' muss zwischen {From} und {To} sein. Es wurde {PropertyValue} eingegeben.",
            "CreditCardValidator": "'{PropertyName}' ist keine gültige Kreditkartennummer.",
            "ScalePrecisionValidator": "'{PropertyName}' darf insgesamt nicht mehr als {ExpectedPrecision} Ziffern enthalten, mit Berücksichtigung von {ExpectedScale} Dezimalstellen. Es wurden {Digits} Ziffern und {ActualScale} Dezimalstellen gefunden.",
            "EmptyValidator": "'{PropertyName}' sollte leer sein.",
            "NullValidator": "'{PropertyName}' sollte leer sein.",
            "EnumValidator": "'{PropertyName}' hat einen Wertebereich, der '{PropertyValue}' nicht enthält.",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "Die Länge von '{PropertyName}' muss zwischen {min_length} und {max_length} Zeichen liegen.",
            "MinimumLength_Simple": "Die Länge von '{PropertyName}' muss größer oder gleich {min_length} sein.",
            "MaximumLength_Simple": "Die Länge von '{PropertyName}' muss kleiner oder gleich {max_length} sein.",
            "ExactLength_Simple": "'{PropertyName}' muss genau {max_length} lang sein.",
            "InclusiveBetween_Simple": "'{PropertyName}' muss zwischen {From} und {To} sein.",
        }
        return dicc.get(key, None)