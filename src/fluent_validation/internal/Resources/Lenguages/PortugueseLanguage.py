class PortugueseLanguage:
    Culture: str = "pt"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' é um endereço de email inválido.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' deve ser superior ou igual a '{ComparisonValue}'.",
            "GreaterThanValidator": "'{PropertyName}' deve ser superior a '{ComparisonValue}'.",
            "LengthValidator": "'{PropertyName}' deve ter {min_length} a {max_length} caracteres. Introduziu {total_length} caracteres.",
            "MinimumLengthValidator": "'{PropertyName}' deve ser maior ou igual a caracteres {min_length}. Você digitou caracteres {total_length}.",
            "MaximumLengthValidator": "'{PropertyName}' deve ser menor ou igual a caracteres {max_length}. Você digitou caracteres {total_length}.",
            "LessThanOrEqualValidator": "'{PropertyName}' deve ser inferior ou igual a '{ComparisonValue}'.",
            "LessThanValidator": "'{PropertyName}' deve ser inferior a '{ComparisonValue}'.",
            "NotEmptyValidator": "'{PropertyName}' deve ser definido.",
            "NotEqualValidator": "'{PropertyName}' deve ser diferente de '{ComparisonValue}'.",
            "NotNullValidator": "'{PropertyName}' não pode ser nulo.",
            "PredicateValidator": "'{PropertyName}' não verifica a condição definida.",
            "AsyncPredicateValidator": "'{PropertyName}' não verifica a condição definida.",
            "RegularExpressionValidator": "'{PropertyName}' não se encontra no formato correcto.",
            "EqualValidator": "'{PropertyName}' deve ser igual a '{ComparisonValue}'.",
            "ExactLengthValidator": "'{PropertyName}' deve ter o comprimento de {max_length} caracteres. Introduziu {total_length} caracteres.",
            "ExclusiveBetweenValidator": "'{PropertyName}' deve estar entre {From} e {To} (exclusivo). Introduziu {PropertyValue}.",
            "InclusiveBetweenValidator": "'{PropertyName}' deve estar entre {From} e {To}. Introduziu {PropertyValue}.",
            "CreditCardValidator": "'{PropertyName}' não é um número de cartão de crédito válido.",
            "ScalePrecisionValidator": "'{PropertyName}' pode não ser mais do que dígitos {ExpectedPrecision} no total, com permissão para decimais de {ExpectedScale}. {Digits} dígitos e {ActualScale} decimais foram encontrados.",
            "EmptyValidator": "'{PropertyName}' deve estar vazio.",
            "NullValidator": "'{PropertyName}' deve estar vazio.",
            "EnumValidator": "'{PropertyName}' possui um intervalo de valores que não inclui '{PropertyValue}'.",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' deve ter {min_length} a {max_length} caracteres.",
            "MinimumLength_Simple": "'{PropertyName}' deve ser maior ou igual a caracteres {min_length}.",
            "MaximumLength_Simple": "'{PropertyName}' deve ser menor ou igual a caracteres {max_length}.",
            "ExactLength_Simple": "'{PropertyName}' deve ter o comprimento de {max_length} caracteres.",
            "InclusiveBetween_Simple": "'{PropertyName}' deve estar entre {From} e {To}.",
        }
        return dicc.get(key, None)
