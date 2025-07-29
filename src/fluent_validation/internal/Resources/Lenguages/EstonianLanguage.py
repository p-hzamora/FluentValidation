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


class EstonianLanguage:
    Culture: str = "et"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' ei ole sobiv e-posti aadress.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' peab olema suurem või sama suur kui '{ComparisonValue}'.",
            "GreaterThanValidator": "'{PropertyName}' peab olema suurem kui '{ComparisonValue}'.",
            "LengthValidator": "'{PropertyName}' peab olema {min_length}-{max_length} märki. Sisestasid {total_length} märki.",
            "MinimumLengthValidator": "'{PropertyName}' peab olema vähemalt {min_length} märki. Sisestasid {total_length} märki.",
            "MaximumLengthValidator": "'{PropertyName}' võib olla kõige rohkem {max_length} märki. Sisestasid {total_length} märki.",
            "LessThanOrEqualValidator": "'{PropertyName}' peab olema väiksem või sama suur kui '{ComparisonValue}'.",
            "LessThanValidator": "'{PropertyName}' peab olema väiksem kui '{ComparisonValue}'.",
            "NotEmptyValidator": "'{PropertyName}' ei või olla tühi.",
            "NotEqualValidator": "'{PropertyName}' ei või olla sama nagu '{ComparisonValue}'.",
            "NotNullValidator": "'{PropertyName}' ei või olla tühi.",
            "PredicateValidator": "'{PropertyName}' ei vasta eeskirjale.",
            "AsyncPredicateValidator": "'{PropertyName}' ei vasta eeskirjale.",
            "RegularExpressionValidator": "'{PropertyName}' ei ole õige kujuga.",
            "EqualValidator": "'{PropertyName}' peab olema sama väärtusega nagu '{ComparisonValue}'.",
            "ExactLengthValidator": "'{PropertyName}' peab olema {max_length} märki. Sisestasid {total_length} märki.",
            "InclusiveBetweenValidator": "'{PropertyName}' peab olema vahemikus {From}-{To}. Sisestasid {PropertyValue}.",
            "ExclusiveBetweenValidator": "'{PropertyName}' peab olema vahemikus {From}-{To}. Sisestasid {PropertyValue}.",
            "CreditCardValidator": "'{PropertyName}' ei ole sobiv krediitkaardi number.",
            "ScalePrecisionValidator": "'{PropertyName}' ei tohi olla pikem kui {ExpectedPrecision} numbrit, {ExpectedScale} kümndendikku. Sisestatud {Digits} numbrit ja {ActualScale} kümnendikku.",
            "EmptyValidator": "'{PropertyName}' peab olema tühi.",
            "NullValidator": "'{PropertyName}' peab olema tühi.",
            "EnumValidator": "'{PropertyName}' lubatud väärtuste hulgas ei ole '{PropertyValue}'.",
            #  Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' peab olema {min_length}-{max_length} märki.",
            "MinimumLength_Simple": "'{PropertyName}' pikkus peab olema vähemalt {min_length} märki.",
            "MaximumLength_Simple": "'{PropertyName}' võib olla kõige rohkem {max_length} märki.",
            "ExactLength_Simple": "'{PropertyName}' peab olema {max_length} märgi pikkune.",
            "InclusiveBetween_Simple": "'{PropertyName}' peab olema vahemikus {From}-{To}.",
        }
        return dicc.get(key, None)
