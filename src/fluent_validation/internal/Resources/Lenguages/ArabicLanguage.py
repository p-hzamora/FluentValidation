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


class ArabicLanguage:
    Culture: str = "ar"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' ليس بريد الكتروني صحيح.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' يجب أن يكون أكبر من أو يساوي '{ComparisonValue}'.",
            "GreaterThanValidator": "'{PropertyName}' يجب أن يكون أكبر من '{ComparisonValue}'.",
            "LengthValidator": "'{PropertyName}' عدد الحروف يجب أن يكون بين {min_length} و {max_length}. عدد ما تم ادخاله {total_length}.",
            "MinimumLengthValidator": "الحد الأدنى لعدد الحروف في '{PropertyName}' هو {min_length}. عدد ما تم ادخاله {total_length}.",
            "MaximumLengthValidator": "الحد الأقصى لعدد الحروف في '{PropertyName}' هو {max_length}. عدد ما تم ادخاله {total_length}.",
            "LessThanOrEqualValidator": "'{PropertyName}' يجب أن يكون أقل من أو يساوي '{ComparisonValue}'.",
            "LessThanValidator": "'{PropertyName}' يجب أن يكون أقل من '{ComparisonValue}'.",
            "NotEmptyValidator": "'{PropertyName}' لا يجب أن يكون فارغاً.",
            "NotEqualValidator": "'{PropertyName}' يجب ألا يساوي '{ComparisonValue}'.",
            "NotNullValidator": "'{PropertyName}' لا يجب أن يكون فارغاً.",
            "PredicateValidator": "الشرط المحدد لا يتفق مع '{PropertyName}'.",
            "AsyncPredicateValidator": "الشرط المحدد لا يتفق مع '{PropertyName}'.",
            "RegularExpressionValidator": "'{PropertyName}' ليس بالتنسيق الصحيح.",
            "EqualValidator": "'{PropertyName}' يجب أن يساوي '{ComparisonValue}'.",
            "ExactLengthValidator": "الحد الأقصى لعدد الحروف في '{PropertyName}' هو {max_length}. عدد ما تم ادخاله {total_length}.",
            "InclusiveBetweenValidator": "'{PropertyName}' يجب أن يكون بين {From} و {To}. ما تم ادخاله {PropertyValue}.",
            "ExclusiveBetweenValidator": "'{PropertyName}' يجب أن يكون بين {From} و {To} (حصرياً). ما تم ادخاله {PropertyValue}.",
            "CreditCardValidator": "'{PropertyName}' ليس رقم بطاقة ائتمان صحيح.",
            "ScalePrecisionValidator": "'{PropertyName}' لا يجب أن يكون أكبر من {ExpectedPrecision} رقما صحيحاً في المجمل, ومسموح بـ {ExpectedScale} أرقام عشرية. ما تم ادخاله {Digits} أرقام صحيحة و {ActualScale} أرقام عشرية.",
            "EmptyValidator": "'{PropertyName}' يجب أن يكون فارغاً.",
            "NullValidator": "'{PropertyName}' يجب أن يكون فارغاً.",
            "EnumValidator": "'{PropertyName}' يحتوي على مجموعة من القيم التي لا تتضمن '{PropertyValue}'.",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' عدد الحروف يجب أن يكون بين {min_length} و {max_length}.",
            "MinimumLength_Simple": "الحد الأدنى لعدد الحروف في '{PropertyName}' هو {min_length}.",
            "MaximumLength_Simple": "الحد الأقصى لعدد الحروف في '{PropertyName}' هو {max_length}.",
            "ExactLength_Simple": "الحد الأقصى لعدد الحروف في '{PropertyName}' هو {max_length}.",
            "InclusiveBetween_Simple": "'{PropertyName}' يجب أن يكون بين {From} و {To}.",
        }
        return dicc.get(key, None)
