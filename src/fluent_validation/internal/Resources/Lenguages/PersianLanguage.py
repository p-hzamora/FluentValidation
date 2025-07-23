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


class PersianLanguage:
    Culture: str = "fa"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' وارد شده قالب صحیح یک ایمیل را ندارد.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' باید بیشتر یا مساوی '{ComparisonValue}' باشد.",
            "GreaterThanValidator": "'{PropertyName}' باید بیشتر از '{ComparisonValue}' باشد.",
            "LengthValidator": "'{PropertyName}' باید حداقل {min_length} و حداکثر {max_length} کاراکتر داشته باشد. اما مقدار وارد شده {total_length} کاراکتر دارد.",
            "MinimumLengthValidator": "'{PropertyName}' باید بزرگتر یا برابر با {min_length} کاراکتر باشد. شما تعداد {total_length} کاراکتر را وارد کردید",
            "MaximumLengthValidator": "'{PropertyName}' باید کمتر یا مساوی {max_length} باشد. {total_length} را وارد کردید",
            "LessThanOrEqualValidator": "'{PropertyName}' باید کمتر یا مساوی '{ComparisonValue}' باشد.",
            "LessThanValidator": "'{PropertyName}' باید کمتر از '{ComparisonValue}' باشد.",
            "NotEmptyValidator": "وارد کردن '{PropertyName}' ضروری است.",
            "NotEqualValidator": "'{PropertyName}' نباید برابر با '{ComparisonValue}' باشد.",
            "NotNullValidator": "وارد کردن '{PropertyName}' ضروری است.",
            "PredicateValidator": "شرط تعیین شده برای '{PropertyName}' برقرار نیست.",
            "AsyncPredicateValidator": "شرط تعیین شده برای '{PropertyName}' برقرار نیست.",
            "RegularExpressionValidator": "'{PropertyName}' دارای قالب صحیح نیست.",
            "EqualValidator": "مقادیر وارد شده برای '{PropertyName}' و '{ComparisonValue}' یکسان نیستند.",
            "ExactLengthValidator": "'{PropertyName}' باید دقیقا {max_length} کاراکتر باشد اما مقدار وارد شده {total_length} کاراکتر دارد.",
            "InclusiveBetweenValidator": "'{PropertyName}' باید بین {From} و {To} باشد. اما مقدار وارد شده ({PropertyValue}) در این محدوده نیست.",
            "ExclusiveBetweenValidator": "'{PropertyName}' باید بیشتر از {From} و کمتر از {To} باشد. اما مقدار وارد شده ({PropertyValue}) در این محدوده نیست.",
            "CreditCardValidator": "'{PropertyName}' وارد شده معتبر نیست.",
            "ScalePrecisionValidator": "'{PropertyName}' نباید بیش از {ExpectedPrecision} رقم، شامل {ExpectedScale} رقم اعشار داشته باشد. مقدار وارد شده {Digits} رقم و {ActualScale} رقم اعشار دارد.",
            "EmptyValidator": "'{PropertyName}' باید خالی باشد.",
            "NullValidator": "'{PropertyName}' باید خالی باشد.",
            "EnumValidator": "مقدار '{PropertyValue}' در لیست مقادیر قابل قبول برای '{PropertyName}' نمی باشد.",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' باید حداقل {min_length} و حداکثر {max_length} کاراکتر داشته باشد.",
            "MinimumLength_Simple": "'{PropertyName}' باید بزرگتر یا برابر با {min_length} کاراکتر باشد.",
            "MaximumLength_Simple": "'{PropertyName}' باید کمتر یا مساوی {max_length} باشد.",
            "ExactLength_Simple": "'{PropertyName}' باید دقیقا {max_length} کاراکتر.",
            "InclusiveBetween_Simple": "'{PropertyName}' باید بین {From} و {To} باشد.",
        }
        return dicc.get(key, None)
