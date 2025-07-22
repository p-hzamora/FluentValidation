class DutchLanguage:
    Culture: str = "nl"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' is geen geldig email adres.",
            "EqualValidator": "'{PropertyName}' moet gelijk zijn aan '{ComparisonValue}'.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' moet groter zijn dan of gelijk zijn aan '{ComparisonValue}'.",
            "GreaterThanValidator": "'{PropertyName}' moet groter zijn dan '{ComparisonValue}'.",
            "LengthValidator": "De lengte van '{PropertyName}' moet tussen {min_length} en {max_length} karakters zijn. U heeft {total_length} karakters ingevoerd.",
            "MinimumLengthValidator": "De lengte van '{PropertyName}' moet groter zijn dan of gelijk aan {min_length} karakters. U heeft {total_length} karakters ingevoerd.",
            "MaximumLengthValidator": "De lengte van '{PropertyName}' moet kleiner zijn dan of gelijk aan {max_length} karakters. U heeft {total_length} karakters ingevoerd.",
            "LessThanOrEqualValidator": "'{PropertyName}' moet kleiner zijn dan of gelijk zijn aan '{ComparisonValue}'.",
            "LessThanValidator": "'{PropertyName}' moet kleiner zijn dan '{ComparisonValue}'.",
            "NotEmptyValidator": "'{PropertyName}' mag niet leeg zijn.",
            "NotEqualValidator": "'{PropertyName}' moet anders zijn dan '{ComparisonValue}'.",
            "NotNullValidator": "'{PropertyName}' mag niet leeg zijn.",
            "PredicateValidator": "'{PropertyName}' voldoet niet aan de vereisten.",
            "AsyncPredicateValidator": "'{PropertyName}' voldoet niet aan de vereisten.",
            "RegularExpressionValidator": "'{PropertyName}' voldoet niet aan het verwachte formaat.",
            "ExactLengthValidator": "De lengte van '{PropertyName}' moet {max_length} karakters zijn. U heeft {total_length} karakters ingevoerd.",
            "EnumValidator": "'{PropertyValue}' komt niet voor in het bereik van '{PropertyName}'.",
            "CreditCardValidator": "'{PropertyName}' is geen geldig credit card nummer.",
            "EmptyValidator": "'{PropertyName}' hoort leeg te zijn.",
            "ExclusiveBetweenValidator": "'{PropertyName}' moet na {From} komen en voor {To} liggen. U heeft '{PropertyValue}' ingevuld.",
            "InclusiveBetweenValidator": "'{PropertyName}' moet tussen {From} en {To} liggen. U heeft '{PropertyValue}' ingevuld.",
            "ScalePrecisionValidator": "'{PropertyName}' mag in totaal niet meer dan {ExpectedPrecision} decimalen nauwkeurig zijn, met een grootte van {ExpectedScale} gehele getallen. Er zijn {Digits} decimalen en een grootte van {ActualScale} gehele getallen gevonden.",
            "NullValidator": "'{PropertyName}' moet leeg zijn.",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "De lengte van '{PropertyName}' moet tussen {min_length} en {max_length} karakters zijn.",
            "MinimumLength_Simple": "De lengte van '{PropertyName}' moet groter zijn dan of gelijk zijn aan {min_length} karakters.",
            "MaximumLength_Simple": "De lengte van '{PropertyName}' moet kleiner zijn dan of gelijk zijn aan {max_length} karakters.",
            "ExactLength_Simple": "De lengte van '{PropertyName}' moet {max_length} karakters zijn.",
            "InclusiveBetween_Simple": "'{PropertyName}' moet tussen {From} en {To} liggen.",
        }
        return dicc.get(key, None)