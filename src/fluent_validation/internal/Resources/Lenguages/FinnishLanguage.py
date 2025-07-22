class FinnishLanguage:
    Culture: str = "fi"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' ei ole kelvollinen sähköpostiosoite.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' pitää olla suurempi tai yhtä suuri kuin '{ComparisonValue}'.",
            "GreaterThanValidator": "'{PropertyName}' pitää olla suurempi kuin '{ComparisonValue}'.",
            "LengthValidator": "'{PropertyName}' pitää olla {min_length}-{max_length} merkkiä. Syötit {total_length} merkkiä.",
            "MinimumLengthValidator": "'{PropertyName}' pitää olla vähintään {min_length} merkkiä. Syötit {total_length} merkkiä.",
            "MaximumLengthValidator": "'{PropertyName}' saa olla enintään {max_length} merkkiä. Syötit {total_length} merkkiä.",
            "LessThanOrEqualValidator": "'{PropertyName}' pitää olla pienempi tai yhtä suuri kuin '{ComparisonValue}'.",
            "LessThanValidator": "'{PropertyName}' pitää olla pienempi kuin '{ComparisonValue}'.",
            "NotEmptyValidator": "'{PropertyName}' ei voi olla tyhjä.",
            "NotEqualValidator": "'{PropertyName}' ei voi olla yhtä suuri kuin '{ComparisonValue}'.",
            "NotNullValidator": "'{PropertyName}' ei voi olla tyhjä.",
            "PredicateValidator": "'{PropertyName}' määritetty ehto ei toteutunut.",
            "AsyncPredicateValidator": "'{PropertyName}' määritetty ehto ei toteutunut.",
            "RegularExpressionValidator": "'{PropertyName}' ei ole oikeassa muodossa.",
            "EqualValidator": "'{PropertyName}' pitäisi olla yhtä suuri kuin '{ComparisonValue}'.",
            "ExactLengthValidator": "'{PropertyName}' pitää olla {max_length} merkkiä. Syötit {total_length} merkkiä.",
            "ExclusiveBetweenValidator": "'{PropertyName}' pitää olla suljetulla välillä {From}-{To}. Syötit {PropertyValue}.",
            "InclusiveBetweenValidator": "'{PropertyName}' pitää olla välillä {From}-{To}. Syötit {PropertyValue}.",
            "CreditCardValidator": "'{PropertyName}' ei ole kelvollinen luottokortin numero.",
            "ScalePrecisionValidator": "'{PropertyName}' ei saa sisältää enempää kuin {ExpectedPrecision} numeroa, sallien {ExpectedScale} desimaalia. {Digits} numeroa ja {ActualScale} desimaalia löytyi.",
            "EmptyValidator": "'{PropertyName}' pitäisi olla tyhjä.",
            "NullValidator": "'{PropertyName}' pitäisi olla tyhjä.",
            "EnumValidator": "'{PropertyName}' arvoista ei löydy '{PropertyValue}'.",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' pitää olla {min_length}-{max_length} merkkiä.",
            "MinimumLength_Simple": "'{PropertyName}' saa olla vähintään {min_length} merkkiä.",
            "MaximumLength_Simple": "'{PropertyName}' pitää olla enintään {max_length} merkkiä.",
            "ExactLength_Simple": "'{PropertyName}' pitää olla {max_length} merkkiä pitkä.",
            "InclusiveBetween_Simple": "'{PropertyName}' pitää olla välillä {From}-{To}.",
        }
        return dicc.get(key, None)