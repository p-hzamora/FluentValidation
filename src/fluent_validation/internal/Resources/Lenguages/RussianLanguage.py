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


class RussianLanguage:
    Culture: str = "ru"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' неверный email адрес.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' должно быть больше или равно '{ComparisonValue}'.",
            "GreaterThanValidator": "'{PropertyName}' должно быть больше '{ComparisonValue}'.",
            "LengthValidator": "'{PropertyName}' должно быть длиной от {min_length} до {max_length} символов. Количество введенных символов: {total_length}.",
            "MinimumLengthValidator": "'{PropertyName}' должно быть длиной не менее {min_length} символов. Количество введенных символов: {total_length}.",
            "MaximumLengthValidator": "'{PropertyName}' должно быть длиной не более {max_length} символов. Количество введенных символов: {total_length}.",
            "LessThanOrEqualValidator": "'{PropertyName}' должно быть меньше или равно '{ComparisonValue}'.",
            "LessThanValidator": "'{PropertyName}' должно быть меньше '{ComparisonValue}'.",
            "NotEmptyValidator": "'{PropertyName}' должно быть заполнено.",
            "NotEqualValidator": "'{PropertyName}' не должно быть равно '{ComparisonValue}'.",
            "NotNullValidator": "'{PropertyName}' должно быть заполнено.",
            "PredicateValidator": "Не выполнено указанное условие для '{PropertyName}'.",
            "AsyncPredicateValidator": "Не выполнено указанное условие для '{PropertyName}'.",
            "RegularExpressionValidator": "'{PropertyName}' имеет неверный формат.",
            "EqualValidator": "'{PropertyName}' должно быть равно '{ComparisonValue}'.",
            "ExactLengthValidator": "'{PropertyName}' должно быть длиной {max_length} символа(ов). Количество введенных символов: {total_length}.",
            "InclusiveBetweenValidator": "'{PropertyName}' должно быть в диапазоне от {From} до {To}. Введенное значение: {PropertyValue}.",
            "ExclusiveBetweenValidator": "'{PropertyName}' должно быть в диапазоне от {From} до {To} (не включая эти значения). Введенное значение: {PropertyValue}.",
            "CreditCardValidator": "'{PropertyName}' неверный номер карты.",
            "ScalePrecisionValidator": "'{PropertyName}' должно содержать не более {ExpectedPrecision} цифр всего, в том числе {ExpectedScale} десятичных знака(ов). Введенное значение содержит {Digits} цифр(ы) и {ActualScale} десятичных знака(ов).",
            "EmptyValidator": "'{PropertyName}' должно быть пустым.",
            "NullValidator": "'{PropertyName}' должно быть пустым.",
            "EnumValidator": "'{PropertyName}' содержит недопустимое значение '{PropertyValue}'.",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' должно быть длиной от {min_length} до {max_length} символов.",
            "MinimumLength_Simple": "'{PropertyName}' должно быть длиной не менее {min_length} символов.",
            "MaximumLength_Simple": "'{PropertyName}' должно быть длиной не более {max_length} символов.",
            "ExactLength_Simple": "'{PropertyName}' должно быть длиной {max_length} символа(ов).",
            "InclusiveBetween_Simple": "'{PropertyName}' должно быть в диапазоне от {From} до {To}.",
        }
        return dicc.get(key, None)
