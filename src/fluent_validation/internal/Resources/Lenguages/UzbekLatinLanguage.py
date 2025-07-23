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


class UzbekLatinLanguage:
    Culture: str = "uz"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' yaroqli elektron pochta manzili emas.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' kamida '{ComparisonValue}'ga teng bo'lishi shart.",
            "GreaterThanValidator": "'{PropertyName}' '{ComparisonValue}'dan katta bo'lishi shart.",
            "LengthValidator": "'{PropertyName}' {min_length}tadan {max_length}tagacha belgidan iborat bo'lishi shart. Siz {total_length}ta belgi kiritdingiz.",
            "MinimumLengthValidator": "'{PropertyName}' kamida {min_length}ta belgidan iborat bo'lishi shart. Siz {total_length}ta belgi kiritdingiz.",
            "MaximumLengthValidator": "'{PropertyName}' ko'pi bilan {max_length}ta belgidan iborat bo'lishi shart. Siz {total_length}ta belgi kiritdingiz.",
            "LessThanOrEqualValidator": "'{PropertyName}' '{ComparisonValue}'dan kam yoki teng bo'lishi shart.",
            "LessThanValidator": "'{PropertyName}' '{ComparisonValue}'dan kam bo'lishi shart.",
            "NotEmptyValidator": "'{PropertyName}' bo'sh bo'lishi mumkin emas.",
            "NotEqualValidator": "'{PropertyName}' '{ComparisonValue}'ga teng bo'lishi mumkin emas.",
            "NotNullValidator": "'{PropertyName}' bo'sh bo'lishi mumkin emas.",
            "PredicateValidator": "'{PropertyName}'ning belgilangan sharti bajarilmadi.",
            "AsyncPredicateValidator": "'{PropertyName}'ning belgilangan sharti bajarilmadi.",
            "RegularExpressionValidator": "'{PropertyName}' noto'g'ri formatda.",
            "EqualValidator": "'{PropertyName}' '{ComparisonValue}'ga teng bo'lishi shart.",
            "ExactLengthValidator": "'{PropertyName}'ning uzunligi {max_length}ta belgidan iborat bo'lishi shart. Siz {total_length}ta belgi kiritdingiz.",
            "InclusiveBetweenValidator": "'{PropertyName}' {From}dan {To}gacha bo'lishi shart. Siz {PropertyValue} kiritdingiz.",
            "ExclusiveBetweenValidator": "'{PropertyName}' {From}dan {To}gacha bo'lishi shart (ushbu qiymatlar hisobga olinmaydi). Siz {PropertyValue} kiritdingiz.",
            "CreditCardValidator": "'{PropertyName}' yaroqli kredit karta raqami emas.",
            "ScalePrecisionValidator": "'{PropertyName}' butun qismi jami {ExpectedPrecision}ta raqamdan oshmasligi shart, jumladan ruxsat etilgan {ExpectedScale} xona kasr(lar) aniqlikda. Butun qismda {Digits}ta raqam(lar) va {ActualScale} xona kasr(lar) topildi.",
            "EmptyValidator": "'{PropertyName}' bo'sh bo'lishi shart.",
            "NullValidator": "'{PropertyName}' bo'sh bo'lishi shart.",
            "EnumValidator": "'{PropertyName}' qiymatlari orasida '{PropertyValue}' yo'q.",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' {min_length}tadan {max_length}tagacha belgidan iborat bo'lishi shart.",
            "MinimumLength_Simple": "'{PropertyName}' kamida {min_length}ta belgidan iborat bo'lishi shart.",
            "MaximumLength_Simple": "'{PropertyName}' ko'pi bilan {max_length}ta belgidan iborat bo'lishi shart.",
            "ExactLength_Simple": "'{PropertyName}' aynan {max_length}ta belgidan iborat bo'lishi shart.",
            "InclusiveBetween_Simple": "'{PropertyName}'ning qiymati {From}dan {To}gacha bo'lishi shart.",
        }
        return dicc.get(key, None)
