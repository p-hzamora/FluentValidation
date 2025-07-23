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


class SerbianCyrillicLanguage:
    Culture: str = "sr"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' није валидна email адреса.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' мора бити веће или једнако од '{ComparisonValue}'.",
            "GreaterThanValidator": "'{PropertyName}' мора бити веће од '{ComparisonValue}'.",
            "LengthValidator": "'{PropertyName}' мора имати између {min_length} и {max_length} карактера. Унесено је {total_length} карактера.",
            "MinimumLengthValidator": "'{PropertyName}' мора имати најмање {min_length} карактера. Унесено је {total_length} карактера.",
            "MaximumLengthValidator": "'{PropertyName}' не сме имати више од {max_length} карактера. Унесено је {total_length} карактера.",
            "LessThanOrEqualValidator": "'{PropertyName}' мора бити мање или једнако од '{ComparisonValue}'.",
            "LessThanValidator": "'{PropertyName}' мора бити мање од '{ComparisonValue}'.",
            "NotEmptyValidator": "'{PropertyName}' не сме бити празно.",
            "NotEqualValidator": "'{PropertyName}' не сме бити једнако '{ComparisonValue}'.",
            "NotNullValidator": "'{PropertyName}' не сме бити празно.",
            "PredicateValidator": "Задати услов није испуњен за '{PropertyName}'.",
            "AsyncPredicateValidator": "Задати услов није испуњен за '{PropertyName}'.",
            "RegularExpressionValidator": "'{PropertyName}' није у одговарајућем формату.",
            "EqualValidator": "'{PropertyName}' мора бити једнако '{ComparisonValue}'.",
            "ExactLengthValidator": "'{PropertyName}' мора имати тачно {max_length} карактера. Унесено је {total_length} карактера.",
            "InclusiveBetweenValidator": "'{PropertyName}' мора бити између {From} и {To}. Унесено је {PropertyValue}.",
            "ExclusiveBetweenValidator": "'{PropertyName}' мора бити између {From} и {To} (ексклузивно). Унесено је {PropertyValue}.",
            "CreditCardValidator": "'{PropertyName}' није валидан број кредитне картице.",
            "ScalePrecisionValidator": "'{PropertyName}' не сме имати више од {ExpectedPrecision} цифара, са дозвољених {ExpectedScale} децималних места. Унесено је {Digits} цифара и {ActualScale} децималних места.",
            "EmptyValidator": "'{PropertyName}' мора бити празно.",
            "NullValidator": "'{PropertyName}' мора бити празно.",
            "EnumValidator": "'{PropertyName}' има распон вредности који не укључује '{PropertyValue}'.",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' мора имати између {min_length} и {max_length} карактера.",
            "MinimumLength_Simple": "'{PropertyName}' мора имати најмање {min_length} карактера.",
            "MaximumLength_Simple": "'{PropertyName}' не сме имати више од {max_length} карактера.",
            "ExactLength_Simple": "'{PropertyName}' мора имати тачно {max_length} карактера.",
            "InclusiveBetween_Simple": "'{PropertyName}' мора бити између {From} и {To}.",
        }
        return dicc.get(key, None)
