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


class FrenchLanguage:
    Culture: str = "fr"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' n'est pas une adresse email valide.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' doit être plus grand ou égal à '{ComparisonValue}'.",
            "GreaterThanValidator": "'{PropertyName}' doit être plus grand que '{ComparisonValue}'.",
            "LengthValidator": "'{PropertyName}' doit contenir entre {min_length} et {max_length} caractères. {total_length} caractères ont été saisis.",
            "MinimumLengthValidator": "'{PropertyName}' doit être supérieur ou égal à {min_length} caractères. Vous avez saisi {total_length} caractères.",
            "MaximumLengthValidator": "'{PropertyName}' doit être inférieur ou égal à {max_length} caractères. Vous avez saisi {total_length} caractères.",
            "LessThanOrEqualValidator": "'{PropertyName}' doit être plus petit ou égal à '{ComparisonValue}'.",
            "LessThanValidator": "'{PropertyName}' doit être plus petit que '{ComparisonValue}'.",
            "NotEmptyValidator": "'{PropertyName}' ne doit pas être vide.",
            "NotEqualValidator": "'{PropertyName}' ne doit pas être égal à '{ComparisonValue}'.",
            "NotNullValidator": "'{PropertyName}' ne doit pas avoir la valeur null.",
            "PredicateValidator": "'{PropertyName}' ne respecte pas la condition fixée.",
            "AsyncPredicateValidator": "'{PropertyName}' ne respecte pas la condition fixée.",
            "RegularExpressionValidator": "'{PropertyName}' n'a pas le bon format.",
            "EqualValidator": "'{PropertyName}' doit être égal à '{ComparisonValue}'.",
            "ExactLengthValidator": "'{PropertyName}' doit être d'une longueur de {max_length} caractères. {total_length} caractères ont été saisis.",
            "ExclusiveBetweenValidator": "'{PropertyName}' doit être entre {From} et {To} (exclusif). Vous avez saisi {PropertyValue}.",
            "InclusiveBetweenValidator": "'{PropertyName}' doit être entre {From} et {To}. Vous avez saisi {PropertyValue}.",
            "CreditCardValidator": "'{PropertyName}' n'est pas un numéro de carte de crédit valide.",
            "ScalePrecisionValidator": "'{PropertyName}' ne doit pas dépasser {ExpectedPrecision} chiffres au total, avec une tolérance de {ExpectedScale} décimales. {Digits} nombres entiers et {ActualScale} décimales ont été trouvés.",
            "EmptyValidator": "'{PropertyName}' devrait être vide.",
            "NullValidator": "'{PropertyName}' devrait être vide.",
            "EnumValidator": "'{PropertyName}' a une plage de valeurs qui n'inclut pas '{PropertyValue}'.",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' doit contenir entre {min_length} et {max_length} caractères.",
            "MinimumLength_Simple": "'{PropertyName}' doit être supérieur ou égal à {min_length} caractères.",
            "MaximumLength_Simple": "'{PropertyName}' doit être inférieur ou égal à {max_length} caractères.",
            "ExactLength_Simple": "'{PropertyName}' doit être d'une longueur de {max_length} caractères.",
            "InclusiveBetween_Simple": "'{PropertyName}' doit être entre {From} et {To}.",
        }
        return dicc.get(key, None)
