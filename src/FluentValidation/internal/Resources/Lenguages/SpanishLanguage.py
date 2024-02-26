class SpanishLanguage:
    Culture: str = "es_ES"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' no es una dirección de correo electrónico válida.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' debe ser mayor o igual que '{ComparisonValue}'.",
            "GreaterThanValidator": "'{PropertyName}' debe ser mayor que '{ComparisonValue}'.",
            "LengthValidator": "'{PropertyName}' debe tener entre {min_length} y {max_length} caracteres. Actualmente tiene {total_length} caracteres.",
            "MinimumLengthValidator": "'{PropertyName}' debe ser mayor o igual que {min_length} caracteres. Ingresó {total_length} caracteres.",
            "MaximumLengthValidator": "'{PropertyName}' debe ser menor o igual que {max_length} caracteres. Ingresó {total_length} caracteres.",
            "LessThanOrEqualValidator": "'{PropertyName}' debe ser menor o igual que '{ComparisonValue}'.",
            "LessThanValidator": "'{PropertyName}' debe ser menor que '{ComparisonValue}'.",
            "NotEmptyValidator": "'{PropertyName}' no debería estar vacío.",
            "NotEqualValidator": "'{PropertyName}' no debería ser igual a '{ComparisonValue}'.",
            "NotNullValidator": "'{PropertyName}' no debe estar vacío.",
            "PredicateValidator": "'{PropertyName}' no cumple con la condición especificada.",
            "AsyncPredicateValidator": "'{PropertyName}' no cumple con la condición especificada.",
            "RegularExpressionValidator": "'{PropertyName}' no tiene el formato correcto.",
            "EqualValidator": "'{PropertyName}' debería ser igual a '{ComparisonValue}'.",
            "ExactLengthValidator": "'{PropertyName}' debe tener una longitud de {max_length} caracteres. Actualmente tiene {total_length} caracteres.",
            "ExclusiveBetweenValidator": "'{PropertyName}' debe estar entre {From} y {To} (exclusivo). Actualmente tiene un valor de {PropertyValue}.",
            "InclusiveBetweenValidator": "'{PropertyName}' debe estar entre {From} y {To}. Actualmente tiene un valor de {PropertyValue}.",
            "CreditCardValidator": "'{PropertyName}' no es un número de tarjeta de crédito válido.",
            "ScalePrecisionValidator": "'{PropertyName}' no debe tener más de {ExpectedPrecision} dígitos en total, con margen para {ExpectedScale} decimales. Se encontraron {Digits} y {ActualScale} decimales.",
            "EmptyValidator": "'{PropertyName}' debe estar vacío.",
            "NullValidator": "'{PropertyName}' debe estar vacío.",
            "EnumValidator": "'{PropertyName}' tiene un rango de valores que no incluye '{PropertyValue}'.",
            #  Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' debe tener entre {min_length} y {max_length} caracteres.",
            "MinimumLength_Simple": "'{PropertyName}' debe ser mayor o igual que {min_length} caracteres.",
            "MaximumLength_Simple": "'{PropertyName}' debe ser menor o igual que {max_length} caracteres.",
            "ExactLength_Simple": "'{PropertyName}' debe tener una longitud de {max_length} caracteres.",
            "InclusiveBetween_Simple": "'{PropertyName}' debe estar entre {From} y {To}.",
        }
        return dicc.get(key, None)
