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


class HebrewLanguage:
    Culture: str = "he"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' אינה כתובת דוא\"ל חוקית.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' חייב להיות גדול או שווה ל- '{ComparisonValue}'.",
            "GreaterThanValidator": "'{PropertyName}' חייב להיות גדול מ- '{ComparisonValue}'.",
            "LengthValidator": "אורך '{PropertyName}' חייב להיות בין {min_length} ל- {max_length}. הזנת {total_length} תווים.",
            "MinimumLengthValidator": "אורך '{PropertyName}' חייב להיות לפחות {min_length} תווים. הזנת {total_length} תווים.",
            "MaximumLengthValidator": "אורך '{PropertyName}' חייב להיות {max_length} תווים או פחות. הזנת {total_length} תווים.",
            "LessThanOrEqualValidator": "'{PropertyName}' חייב להיות קטן או שווה ל- '{ComparisonValue}'.",
            "LessThanValidator": "'{PropertyName}' חייב להיות קטן מ- '{ComparisonValue}'.",
            "NotEmptyValidator": "'{PropertyName}' לא אמור להיות ריק.",
            "NotEqualValidator": "'{PropertyName}' לא יכול להיות שווה ל- '{ComparisonValue}'.",
            "NotNullValidator": "'{PropertyName}' לא יכול להיות ריק.",
            "PredicateValidator": "התנאי שצוין לא התקיים עבור '{PropertyName}'.",
            "AsyncPredicateValidator": "התנאי שצוין לא התקיים עבור '{PropertyName}'.",
            "RegularExpressionValidator": "'{PropertyName}' אינו בפורמט הנכון.",
            "EqualValidator": "'{PropertyName}' אמור להיות שווה ל- '{ComparisonValue}'.",
            "ExactLengthValidator": "'{PropertyName}' חייב להיות באורך {max_length} תווים. הזנת {total_length} תווים.",
            "InclusiveBetweenValidator": "'{PropertyName}' חייב להיות בין {From} לבין {To}. הזנת {PropertyValue}.",
            "ExclusiveBetweenValidator": "'{PropertyName}' חייב להיות בין {From} לבין {To} (לא כולל). הזנת {PropertyValue}.",
            "CreditCardValidator": "'{PropertyName}' אינו מספר כרטיס אשראי חוקי.",
            "ScalePrecisionValidator": "'{PropertyName}' לא יכול לכלול יותר מ- {ExpectedPrecision} ספרות בסך הכל, עם הקצבה של {ExpectedScale} ספרות עשרוניות. נמצאו {Digits} ספרות ו- {ActualScale} ספרות עשרוניות.",
            "EmptyValidator": "'{PropertyName}' אמור להיות ריק.",
            "NullValidator": "'{PropertyName}' חייב להיות ריק.",
            "EnumValidator": "'{PropertyName}' מכיל טווח ערכים שאינו כולל את '{PropertyValue}'.",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "אורך '{PropertyName}' חייב להיות בין {min_length} ל- {max_length}.",
            "MinimumLength_Simple": "אורך '{PropertyName}' חייב להיות לפחות {min_length} תווים.",
            "MaximumLength_Simple": "אורך '{PropertyName}' חייב להיות {max_length} תווים או פחות.",
            "ExactLength_Simple": "'{PropertyName}' חייב להיות באורך {max_length} תווים.",
            "InclusiveBetween_Simple": "'{PropertyName}' חייב להיות בין {From} לבין {To}.",
        }
        return dicc.get(key, None)
