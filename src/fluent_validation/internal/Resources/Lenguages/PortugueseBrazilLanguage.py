# region License

# Copyright (c) .NET Foundation and contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# The latest version of this file can be found at https://github.com/p-hzamora/FluentValidation

# endregion


class PortugueseBrazilLanguage:
    Culture: str = "pt-BR"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' é um endereço de email inválido.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' deve ser superior ou igual a '{ComparisonValue}'.",
            "GreaterThanValidator": "'{PropertyName}' deve ser superior a '{ComparisonValue}'.",
            "LengthValidator": "'{PropertyName}' deve ter entre {min_length} e {max_length} caracteres. Você digitou {total_length} caracteres.",
            "MinimumLengthValidator": "'{PropertyName}' deve ser maior ou igual a {min_length} caracteres. Você digitou {total_length} caracteres.",
            "MaximumLengthValidator": "'{PropertyName}' deve ser menor ou igual a {max_length} caracteres. Você digitou {total_length} caracteres.",
            "LessThanOrEqualValidator": "'{PropertyName}' deve ser inferior ou igual a '{ComparisonValue}'.",
            "LessThanValidator": "'{PropertyName}' deve ser inferior a '{ComparisonValue}'.",
            "NotEmptyValidator": "'{PropertyName}' deve ser informado.",
            "NotEqualValidator": "'{PropertyName}' deve ser diferente de '{ComparisonValue}'.",
            "NotNullValidator": "'{PropertyName}' não pode ser nulo.",
            "PredicateValidator": "'{PropertyName}' não atende a condição definida.",
            "AsyncPredicateValidator": "'{PropertyName}' não atende a condição definida.",
            "RegularExpressionValidator": "'{PropertyName}' não está no formato correto.",
            "EqualValidator": "'{PropertyName}' deve ser igual a '{ComparisonValue}'.",
            "ExactLengthValidator": "'{PropertyName}' deve ter exatamente {max_length} caracteres. Você digitou {total_length} caracteres.",
            "ExclusiveBetweenValidator": "'{PropertyName}' deve, exclusivamente, estar entre {From} e {To}. Você digitou {PropertyValue}.",
            "InclusiveBetweenValidator": "'{PropertyName}' deve estar entre {From} e {To}. Você digitou {PropertyValue}.",
            "CreditCardValidator": "'{PropertyName}' não é um número válido de cartão de crédito.",
            "ScalePrecisionValidator": "'{PropertyName}' não pode ter mais do que {ExpectedPrecision} dígitos no total, com {ExpectedScale} dígitos decimais. {Digits} dígitos e {ActualScale} decimais foram informados.",
            "EmptyValidator": "'{PropertyName}' deve estar vazio.",
            "NullValidator": "'{PropertyName}' deve estar null.",
            "EnumValidator": "'{PropertyName}' possui um intervalo de valores que não inclui '{PropertyValue}'.",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' deve ter entre {min_length} e {max_length} caracteres.",
            "MinimumLength_Simple": "'{PropertyName}' deve ser maior ou igual a {min_length} caracteres.",
            "MaximumLength_Simple": "'{PropertyName}' deve ser menor ou igual a {max_length} caracteres.",
            "ExactLength_Simple": "'{PropertyName}' deve ter {max_length} caracteres de comprimento.",
            "InclusiveBetween_Simple": "'{PropertyName}' deve estar entre {From} e {To}.",
        }
        return dicc.get(key, None)
