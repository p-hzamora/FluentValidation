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


class UkrainianLanguage:
    Culture: str = "uk"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' не є email-адресою.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' має бути більшим, або дорівнювати '{ComparisonValue}'.",
            "GreaterThanValidator": "'{PropertyName}' має бути більшим за '{ComparisonValue}'.",
            "LengthValidator": "'{PropertyName}' має бути довжиною від {min_length} до {max_length} символів. Ви ввели {total_length} символів.",
            "MinimumLengthValidator": "Довжина '{PropertyName}' має бути не меншою ніж {min_length} символів. Ви ввели {total_length} символів.",
            "MaximumLengthValidator": "Довжина '{PropertyName}' має бути {max_length} символів, або менше. Ви ввели {total_length} символів.",
            "LessThanOrEqualValidator": "'{PropertyName}' має бути меншим, або дорівнювати '{ComparisonValue}'.",
            "LessThanValidator": "'{PropertyName}' має бути меншим за '{ComparisonValue}'.",
            "NotEmptyValidator": "'{PropertyName}' не може бути порожнім.",
            "NotEqualValidator": "'{PropertyName}' не може дорівнювати '{ComparisonValue}'.",
            "NotNullValidator": "'{PropertyName}' не може бути порожнім.",
            "PredicateValidator": "Вказана умова не є задовільною для '{PropertyName}'.",
            "AsyncPredicateValidator": "Вказана умова не є задовільною для '{PropertyName}'.",
            "RegularExpressionValidator": "'{PropertyName}' має неправильний формат.",
            "EqualValidator": "'{PropertyName}' має дорівнювати '{ComparisonValue}'.",
            "ExactLengthValidator": "'{PropertyName}' має бути довжиною {max_length} символів. Ви ввели {total_length} символів.",
            "InclusiveBetweenValidator": "'{PropertyName}' має бути між {From} та {To} (включно). Ви ввели {PropertyValue}.",
            "ExclusiveBetweenValidator": "'{PropertyName}' має бути між {From} та {To}. Ви ввели {PropertyValue}.",
            "CreditCardValidator": "'{PropertyName}' не є номером кредитної картки.",
            "ScalePrecisionValidator": "'{PropertyName}' не може мати більше за {ExpectedPrecision} цифр всього, з {ExpectedScale} десятковими знаками. {Digits} цифр та {ActualScale} десяткових знаків знайдено.",
            "EmptyValidator": "'{PropertyName}' має бути порожнім.",
            "NullValidator": "'{PropertyName}' має бути порожнім.",
            "EnumValidator": "'{PropertyName}' має діапазон значень, який не включає '{PropertyValue}'.",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' має бути довжиною від {min_length} до {max_length} символів.",
            "MinimumLength_Simple": "Довжина '{PropertyName}' має бути не меншою ніж {min_length} символів.",
            "MaximumLength_Simple": "Довжина '{PropertyName}' має бути {max_length} символів, або менше.",
            "ExactLength_Simple": "'{PropertyName}' має бути довжиною {max_length} символів.",
            "InclusiveBetween_Simple": "'{PropertyName}' має бути між {From} та {To} (включно).",
        }
        return dicc.get(key, None)
