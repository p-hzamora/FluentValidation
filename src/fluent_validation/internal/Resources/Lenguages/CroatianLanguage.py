class CroatianLanguage:
    Culture: str = "hr"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' nije ispravna e-mail adresa.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' mora biti veći ili jednak '{ComparisonValue}'.",
            "GreaterThanValidator": "'{PropertyName}' mora biti veći od '{ComparisonValue}'.",
            "LengthValidator": "'{PropertyName}' mora biti između {min_length} i {max_length} znakova. Upisali ste {total_length} znakova.",
            "MinimumLengthValidator": "'{PropertyName}' mora imati duljinu veću ili jednaku {min_length}. Unijeli ste {total_length} znakova.",
            "MaximumLengthValidator": "'{PropertyName}' mora imati duljinu manju ili jednaku {max_length}. Unijeli ste {total_length} znakova.",
            "LessThanOrEqualValidator": "'{PropertyName}' mora biti manji ili jednak '{ComparisonValue}'.",
            "LessThanValidator": "'{PropertyName}' mora biti manji od '{ComparisonValue}'.",
            "NotEmptyValidator": "'{PropertyName}' ne smije biti prazan.",
            "NotEqualValidator": "'{PropertyName}' ne smije biti jednak '{ComparisonValue}'.",
            "NotNullValidator": "Niste upisali '{PropertyName}'",
            "PredicateValidator": "'{PropertyName}' nije ispravan.",
            "AsyncPredicateValidator": "'{PropertyName}' nije ispravan.",
            "RegularExpressionValidator": "'{PropertyName}' nije u odgovarajućem formatu.",
            "EqualValidator": "'{PropertyName}' mora biti jednak '{ComparisonValue}'.",
            "ExactLengthValidator": "'{PropertyName}' mora sadržavati {max_length} znakova. Upisali ste {total_length} znakova.",
            "InclusiveBetweenValidator": "'{PropertyName}' mora biti između {From} i {To}. Upisali ste {PropertyValue}.",
            "ExclusiveBetweenValidator": "'{PropertyName}' mora biti između {From} i {To} (ne uključujući granice). Upisali ste {PropertyValue}.",
            "CreditCardValidator": "'{PropertyName}' nije odgovarajuća kreditna kartica.",
            "ScalePrecisionValidator": "'{PropertyName}' ne smije imati više od {ExpectedPrecision} znamenki, sa {ExpectedScale} decimalna mjesta. Upisali ste {Digits} znamenki i {ActualScale} decimalna mjesta.",
            "EmptyValidator": "'{PropertyName}' mora biti prazan.",
            "NullValidator": "'{PropertyName}' mora biti prazan.",
            "EnumValidator": "'{PropertyName}' ima raspon vrijednosti koji ne uključuje '{PropertyValue}'.",
            #  Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' mora biti između {min_length} i {max_length} znakova.",
            "MinimumLength_Simple": "'{PropertyName}' mora imati duljinu veću ili jednaku {min_length}.",
            "MaximumLength_Simple": "'{PropertyName}' mora imati duljinu manju ili jednaku {max_length}.",
            "ExactLength_Simple": "'{PropertyName}' mora sadržavati {max_length} znakova.",
            "InclusiveBetween_Simple": "'{PropertyName}' mora biti između {From} i {To}.",
        }
        return dicc.get(key, None)
