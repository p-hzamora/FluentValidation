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


class SlovakLanguage:
    Culture: str = "sk"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "Pole '{PropertyName}' musí obsahovať platnú emailovú adresu.",
            "GreaterThanOrEqualValidator": "Hodnota poľa '{PropertyName}' musí byť väčšia alebo sa rovnať '{ComparisonValue}'.",
            "GreaterThanValidator": "Hodnota poľa '{PropertyName}' musí byť väčšia ako '{ComparisonValue}'.",
            "LengthValidator": "Dĺžka poľa '{PropertyName}' musí byť medzi {min_length} a {max_length} znakmi. Vami zadaná dĺžka je {total_length} znakov.",
            "MinimumLengthValidator": "Dĺžka poľa '{PropertyName}' musí byť väčšia alebo rovná {min_length} znakom. Vami zadaná dĺžka je {total_length} znakov.",
            "MaximumLengthValidator": "Dĺžka poľa '{PropertyName}' musí byť menšia alebo rovná {max_length} znakom. Vami zadaná dĺžka je {total_length} znakov.",
            "LessThanOrEqualValidator": "Hodnota poľa '{PropertyName}' musí byť menšia alebo sa rovnať '{ComparisonValue}'.",
            "LessThanValidator": "Hodnota poľa '{PropertyName}' musí byť menšia ako '{ComparisonValue}'.",
            "NotEmptyValidator": "Pole '{PropertyName}' nesmie byť prázdne.",
            "NotEqualValidator": "Pole '{PropertyName}' sa nesmie rovnať '{ComparisonValue}'.",
            "NotNullValidator": "Pole '{PropertyName}' nesmie byť prázdne.",
            "PredicateValidator": "Nebola splnená podmienka pre pole '{PropertyName}'.",
            "AsyncPredicateValidator": "Nebola splnená podmienka pre pole '{PropertyName}'.",
            "RegularExpressionValidator": "Pole '{PropertyName}' nemá správny formát.",
            "EqualValidator": "Hodnota poľa '{PropertyName}' musí byť rovná '{ComparisonValue}'.",
            "ExactLengthValidator": "Dĺžka poľa '{PropertyName}' musí byť {max_length} znakov. Vami zadaná dĺžka je {total_length} znakov.",
            "InclusiveBetweenValidator": "Hodnota poľa '{PropertyName}' musí byť medzi {From} a {To} (vrátane). Vami zadaná hodnota je {PropertyValue}.",
            "ExclusiveBetweenValidator": "Hodnota poľa '{PropertyName}' musí byť väčšia ako {From} a menšia ako {To}. Vami zadaná hodnota {PropertyValue}.",
            "CreditCardValidator": "Pole '{PropertyName}' nie je správné číslo kreditnej karty.",
            "ScalePrecisionValidator": "Pole '{PropertyName}' nemôže mať viac  ako {ExpectedPrecision} čísiel a {ExpectedScale} desatinných miest. Vami bolo zadané {Digits} číslic a {ActualScale} desatinných miest.",
            "EmptyValidator": "Pole '{PropertyName}' musí byť prázdne.",
            "NullValidator": "Pole '{PropertyName}' musí byť prázdne.",
            "EnumValidator": "Pole '{PropertyName}' má rozsah hodnôt, ktoré neobsahujú '{PropertyValue}'.",
            #  Additional fallback messages used by clientside validation integration.
            "Length_Simple": "Dĺžka poľa '{PropertyName}' musí byť medzi {min_length} a {max_length} znakmi.",
            "MinimumLength_Simple": "Dĺžka poľa '{PropertyName}' musí byť väčšia alebo rovná {min_length} znakom.",
            "MaximumLength_Simple": "Dĺžka poľa '{PropertyName}' musí byť menšia alebo rovná {max_length} znakom.",
            "ExactLength_Simple": "Dĺžka poľa '{PropertyName}' musí byť {max_length} znakov. ",
            "InclusiveBetween_Simple": "Hodnota poľa '{PropertyName}' musí byť medzi {From} a {To} (vrátane).",
        }
        return dicc.get(key, None)
