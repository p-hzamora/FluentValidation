class SwedishLanguage:
    Culture: str = "sv"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "\"{PropertyName}\" är inte en giltig e-postadress.",
            "GreaterThanOrEqualValidator": "\"{PropertyName}\" måste vara större än eller lika med {ComparisonValue}.",
            "GreaterThanValidator": "\"{PropertyName}\" måste vara större än {ComparisonValue}.",
            "LengthValidator": "\"{PropertyName}\" måste vara mellan {min_length} och {max_length} tecken långt. Du angav {total_length} tecken.",
            "MinimumLengthValidator": "\"{PropertyName}\" måste vara större än eller lika med {min_length} tecken. Du har skrivit in {total_length} tecken.",
            "MaximumLengthValidator": "\"{PropertyName}\" måste vara mindre än eller lika med {max_length} tecken. Du har skrivit in {total_length} tecken.",
            "LessThanOrEqualValidator": "\"{PropertyName}\" måste vara mindre än eller lika med {ComparisonValue}.",
            "LessThanValidator": "\"{PropertyName}\" måste vara mindre än {ComparisonValue}.",
            "NotEmptyValidator": "\"{PropertyName}\" måste anges.",
            "NotEqualValidator": "\"{PropertyName}\" får inte vara lika med \"{ComparisonValue}\".",
            "NotNullValidator": "\"{PropertyName}\" måste anges.",
            "PredicateValidator": "Det angivna villkoret uppfylldes inte för \"{PropertyName}\".",
            "AsyncPredicateValidator": "Det angivna villkoret uppfylldes inte för \"{PropertyName}\".",
            "RegularExpressionValidator": "\"{PropertyName}\" har inte ett korrekt format.",
            "EqualValidator": "\"{PropertyName}\" måste vara lika med \"{ComparisonValue}\".",
            "ExactLengthValidator": "\"{PropertyName}\" måste vara {max_length} tecken långt. Du angav {total_length} tecken.",
            "InclusiveBetweenValidator": "\"{PropertyName}\" måste vara mellan {From} och {To}. Du angav {PropertyValue}.",
            "ExclusiveBetweenValidator": "\"{PropertyName}\" måste vara mellan {From} och {To} (gränsvärdena exkluderade). Du angav {PropertyValue}.",
            "CreditCardValidator": "\"{PropertyName}\" är inte ett giltigt kreditkortsnummer.",
            "ScalePrecisionValidator": "\"{PropertyName}\" får inte vara mer än {ExpectedPrecision} siffror totalt, med förbehåll för {ExpectedScale} decimaler. {Digits} siffror och {ActualScale} decimaler hittades.",
            "EmptyValidator": "\"{PropertyName}\" ska vara tomt.",
            "NullValidator": "\"{PropertyName}\" ska vara tomt.",
            "EnumValidator": "\"{PropertyName}\" har ett antal värden som inte inkluderar \"{PropertyValue}\".",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "\"{PropertyName}\" måste vara mellan {min_length} och {max_length} tecken långt.",
            "MinimumLength_Simple": "\"{PropertyName}\" måste vara större än eller lika med {min_length} tecken.",
            "MaximumLength_Simple": "\"{PropertyName}\" måste vara mindre än eller lika med {max_length} tecken.",
            "ExactLength_Simple": "\"{PropertyName}\" måste vara {max_length} tecken långt.",
            "InclusiveBetween_Simple": "\"{PropertyName}\" måste vara mellan {From} och {To}.",
        }
        return dicc.get(key, None)