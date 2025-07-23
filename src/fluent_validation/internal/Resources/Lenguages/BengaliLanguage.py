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


class BengaliLanguage:
    Culture: str = "bn"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' বৈধ ইমেইল ঠিকানা নয়।",
            "GreaterThanOrEqualValidator": "'{PropertyName}' অবশ্যই '{ComparisonValue}' এর সমান অথবা বেশি হবে।",
            "GreaterThanValidator": "'{PropertyName}' অবশ্যই '{ComparisonValue}' এর বেশি হবে।",
            "LengthValidator": "'{PropertyName}' এর অক্ষর সংখ্যা অবশ্যই {min_length} থেকে {max_length} এর মধ্যে হবে। আপনি {total_length}টি অক্ষর প্রদান করেছেন।",
            "MinimumLengthValidator": "'{PropertyName}' এর অক্ষর সংখ্যা কমপক্ষে {min_length} অথবা এর চেয়ে বেশি হবে। আপনি {total_length}টি অক্ষর প্রদান করেছেন।",
            "MaximumLengthValidator": "'{PropertyName}' এর অক্ষর সংখ্যা সর্বোচ্চ {max_length} অথবা এর চেয়ে কম হবে। আপনি {total_length}টি অক্ষর প্রদান করেছেন।",
            "LessThanOrEqualValidator": "'{PropertyName}' অবশ্যই '{ComparisonValue}' এর সমান অথবা কম হবে।",
            "LessThanValidator": "'{PropertyName}' অবশ্যই '{ComparisonValue}' এর চেয়ে কম হবে।",
            "NotEmptyValidator": "'{PropertyName}' খালি হতে পারবে না।",
            "NotEqualValidator": "'{PropertyName}' '{ComparisonValue}' হতে পারবেনা।",
            "NotNullValidator": "'{PropertyName}' খালি হতে পারবে না।",
            "PredicateValidator": "নির্ধারিত শর্তটি '{PropertyName}' এর জন্য মেটেনি।",
            "AsyncPredicateValidator": "নির্ধারিত শর্তটি '{PropertyName}' এর জন্য মেটেনি।",
            "RegularExpressionValidator": "'{PropertyName}' সঠিক বিন্যাসে নেই।",
            "EqualValidator": "'{PropertyName}' অবশ্যই '{ComparisonValue}' এর সমান হবে।",
            "ExactLengthValidator": "'{PropertyName}' এর অক্ষর সংখ্যা অবশ্যই {max_length}টি হবে। আপনি {total_length}টি অক্ষর প্রদান করেছেন।",
            "InclusiveBetweenValidator": "'{PropertyName}' অবশ্যই {From} থেকে {To} এর মধ্যে হবে। আপনি {PropertyValue} প্রদান করেছেন।",
            "ExclusiveBetweenValidator": "'{PropertyName}' অবশ্যই {From} থেকে {To} এর বাহিরে হবে না। আপনি {PropertyValue} প্রদান করেছেন।",
            "CreditCardValidator": "'{PropertyName}' বৈধ ক্রেডিট কার্ড সংখ্যা নয়।",
            "ScalePrecisionValidator": "'{PropertyName}' মোট {ExpectedPrecision} অঙ্কের বেশি হবে না। {ExpectedScale} বৈধ দশমাংশ, কিন্তু প্রদত্ত {Digits} সংখ্যাটি {ActualScale} দশমাংশের",
            "EmptyValidator": "'{PropertyName}' অবশ্যই খালি হবে।",
            "NullValidator": "'{PropertyName}' অবশ্যই খালি হবে।",
            "EnumValidator": "'{PropertyValue}' '{PropertyName}' এর সীমা লঙ্ঘন করে।",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' এর অক্ষর সংখ্যা অবশ্যই {min_length} থেকে {max_length} এর মধ্যে হবে।",
            "MinimumLength_Simple": "'{PropertyName}' এর অক্ষর সংখ্যা কমপক্ষে {min_length} অথবা এর চেয়ে বেশি হবে।",
            "MaximumLength_Simple": "'{PropertyName}' এর অক্ষর সংখ্যা সর্বোচ্চ {max_length}টি অথবা এর চেয়ে কম হবে।",
            "ExactLength_Simple": "'{PropertyName}' এর অক্ষর সংখ্যা অবশ্যই {max_length}টি হবে।",
            "InclusiveBetween_Simple": "'{PropertyName}' অবশ্যই {From} থেকে {To} এর মধ্যে হবে।",
        }
        return dicc.get(key, None)
