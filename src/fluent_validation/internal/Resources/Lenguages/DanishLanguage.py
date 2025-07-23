class DanishLanguage:
    Culture: str = "da"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' er ikke en gyldig e-mail-adresse.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' skal være større end eller lig med '{ComparisonValue}'.",
            "GreaterThanValidator": "'{PropertyName}' skal være større end '{ComparisonValue}'.",
            "LengthValidator": "'{PropertyName}' skal være mellem {min_length} og {max_length} tegn. Du har indtastet {total_length} tegn.",
            "MinimumLengthValidator": "'{PropertyName}' skal være større end eller lig med {min_length} tegn. Du indtastede {total_length} tegn.",
            "MaximumLengthValidator": "'{PropertyName}' skal være mindre end eller lig med {max_length} tegn. Du indtastede {total_length} tegn.",
            "LessThanOrEqualValidator": "'{PropertyName}' skal være mindre end eller lig med '{ComparisonValue}'.",
            "LessThanValidator": "'{PropertyName}' skal være mindre end '{ComparisonValue}'.",
            "NotEmptyValidator": "'{PropertyName}' må ikke være tom.",
            "NotEqualValidator": "'{PropertyName}' må ikke være lig med '{ComparisonValue}'.",
            "NotNullValidator": "'{PropertyName}' må ikke være tom.",
            "PredicateValidator": "Den angivne betingelse var ikke opfyldt for '{PropertyName}'.",
            "AsyncPredicateValidator": "Den angivne betingelse var ikke opfyldt for '{PropertyName}'.",
            "RegularExpressionValidator": "'{PropertyName}' er ikke i det rigtige format.",
            "EqualValidator": "'{PropertyName}' skal være lig med '{ComparisonValue}'.",
            "ExactLengthValidator": "'{PropertyName}' skal være {max_length} tegn langt. Du har indtastet {total_length} tegn.",
            "InclusiveBetweenValidator": "'{PropertyName}' skal være mellem {From} og {To}. Du har indtastet {PropertyValue}.",
            "ExclusiveBetweenValidator": "'{PropertyName}' skal være mellem {From} og {To} (eksklusiv). Du har indtastet {PropertyValue}.",
            "CreditCardValidator": "'{PropertyName}' er ikke et gyldigt kreditkortnummer.",
            "ScalePrecisionValidator": "'{PropertyName}' må ikke være mere end {ExpectedPrecision} cifre i alt, med hensyn til {ExpectedScale} decimaler. {Digits} cifre og {ActualScale} decimaler blev fundet.",
            "EmptyValidator": "'{PropertyName}' skal være tomt.",
            "NullValidator": "'{PropertyName}' skal være tomt.",
            "EnumValidator": "'{PropertyName}' har en række værdier, der ikke indeholder '{PropertyValue}'.",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' skal være mellem {min_length} og {max_length} tegn.",
            "MinimumLength_Simple": "'{PropertyName}' skal være større end eller lig med {min_length} tegn.",
            "MaximumLength_Simple": "'{PropertyName}' skal være mindre end eller lig med {max_length} tegn.",
            "ExactLength_Simple": "'{PropertyName}' skal være {max_length} tegn langt.",
            "InclusiveBetween_Simple": "'{PropertyName}' skal være mellem {From} og {To}.",
        }
        return dicc.get(key, None)
