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


class GeorgianLanguage:
    Culture: str = "ka"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' არ არის ვალიდური ელ.ფოსტის მისამართი.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' უნდა იყოს '{ComparisonValue}'-ზე მეტი ან ტოლი.",
            "GreaterThanValidator": "'{PropertyName}' უნდა იყოს '{ComparisonValue}'-ზე მეტი.",
            "LengthValidator": "'{PropertyName}' უნდა იყოს {min_length}-დან {max_length} სიმბოლომდე. თქვენ შეიყვანეთ {total_length} სიმბოლო.",
            "MinimumLengthValidator": "'{PropertyName}'-ის სიგრძე უნდა აღემატებოდეს {min_length} სიმბოლოს. თქვენ შეიყვანეთ {total_length} სიმბოლო.",
            "MaximumLengthValidator": "'{PropertyName}'-ის სიგრძე არ უნდა აღემატებოდეს {max_length} სიმბოლოს. თქვენ შეიყვანეთ {total_length} სიმბოლო.",
            "LessThanOrEqualValidator": "'{PropertyName}' უნდა იყოს '{ComparisonValue}'-ზე ნაკლები ან ტოლი.",
            "LessThanValidator": "'{PropertyName}' უნდა იყოს '{ComparisonValue}'-ზე ნაკლები.",
            "NotEmptyValidator": "'{PropertyName}' არ უნდა იყოს ცარიელი.",
            "NotEqualValidator": "'{PropertyName}' არ უნდა უდრიდეს '{ComparisonValue}'-ს.",
            "NotNullValidator": "'{PropertyName}' არ უნდა იყოს ცარიელი.",
            "PredicateValidator": "'{PropertyName}'-ისთვის განსაზღვრული პირობა არ დაკმაყოფილდა.",
            "AsyncPredicateValidator": "'{PropertyName}'-ისთვის განსაზღვრული პირობა არ დაკმაყოფილდა.",
            "RegularExpressionValidator": "'{PropertyName}'-ის ფორმატი არასწორია.",
            "EqualValidator": "'{PropertyName}' უნდა უდრიდეს '{ComparisonValue}'-ს.",
            "ExactLengthValidator": "'{PropertyName}' უნდა უდრიდეს {max_length} სიმბოლოს. თქვენ შეიყვანეთ {total_length} სიმბოლო.",
            "InclusiveBetweenValidator": "'{PropertyName}' უნდა იყოს {From}-დან {To}-მდე (ჩათვლით). თქვენ შეიყვანეთ {PropertyValue}.",
            "ExclusiveBetweenValidator": "'{PropertyName}' უნდა იყოს {From}-სა და {To}-ს შორის. თქვენ შეიყვანეთ {PropertyValue}.",
            "CreditCardValidator": "'{PropertyName}' არ არის ვალიდური საკრედიტო ბარათის ნომერი.",
            "ScalePrecisionValidator": "'{PropertyName}' არ უნდა იყოს ჯამში {ExpectedPrecision} ციფრზე მეტი, {ExpectedScale} ათობითი ციფრის ჩათვლით. თქვენ შეიყვანეთ {Digits} ციფრი და {ActualScale} ათობითი სიმბოლო.",
            "EmptyValidator": "'{PropertyName}' უნდა იყოს ცარიელი.",
            "NullValidator": "'{PropertyName}' უნდა იყოს ცარიელი.",
            "EnumValidator": "'{PropertyValue}' არ შედის '{PropertyName}'-ის დასაშვებ მნიშვნელობებში.",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' უნდა იყოს {min_length}-დან {max_length} სიმბოლომდე.",
            "MinimumLength_Simple": "'{PropertyName}'-ის სიგრძე უნდა აღემატებოდეს {min_length} სიმბოლოს.",
            "MaximumLength_Simple": "'{PropertyName}'-ის სიგრძე არ უნდა აღემატებოდეს {max_length} სიმბოლოს.",
            "ExactLength_Simple": "'{PropertyName}' უნდა უდრიდეს {max_length} სიმბოლოს.",
            "InclusiveBetween_Simple": "'{PropertyName}' უნდა იყოს {From}-დან {To}-მდე (ჩათვლით).",
        }
        return dicc.get(key, None)
