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


class KazakhLanguage:
    Culture: str = "kk"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' Қате электрондық пошта мекенжайы.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' мән мынадан -'{ComparisonValue}' үлкен немесе оған тең болуы керек.",
            "GreaterThanValidator": "'{PropertyName}' мән мынадан -'{ComparisonValue}' үлкенірек болуы керек.",
            "LengthValidator": "'{PropertyName}' таңбаларының саны {min_length} және {max_length} арасында болуы керек. Енгізілген таңбалар саны: {total_length}.",
            "MinimumLengthValidator": "'{PropertyName}' таңбаларының саны мынадан - {min_length} кем емес болуы керек. Енгізілген таңбалар саны: {total_length}.",
            "MaximumLengthValidator": "'{PropertyName}' таңбаларының саны мынадан - {max_length} көп емес болуы керек. Енгізілген таңбалар саны: {total_length}.",
            "LessThanOrEqualValidator": "'{PropertyName}' мән мынадан -'{ComparisonValue}' кіші немесе оған тең болуы керек.",
            "LessThanValidator": "'{PropertyName}' мән мынадан -'{ComparisonValue}' аз болуы керек.",
            "NotEmptyValidator": "'{PropertyName}' толтырылуы керек.",
            "NotEqualValidator": "'{PropertyName}' '{ComparisonValue}' мәніне тең болмауы керек.",
            "NotNullValidator": "'{PropertyName}' толтырылуы керек.",
            "PredicateValidator": "'{PropertyName}' үшін көрсетілген шарт орындалмады.",
            "AsyncPredicateValidator": "'{PropertyName}' үшін көрсетілген шарт орындалмады.",
            "RegularExpressionValidator": "'{PropertyName}' дұрыс пішімде емес.",
            "EqualValidator": "'{PropertyName}' '{ComparisonValue}' мәніне тең болуы керек.",
            "ExactLengthValidator": "'{PropertyName}' ұзындығы {max_length} таңба болуы керек. Енгізілген таңбалар саны: {total_length}.",
            "InclusiveBetweenValidator": "'{PropertyName}' {From} және {To} аралығында болуы керек. Енгізілген мән: {PropertyValue}.",
            "ExclusiveBetweenValidator": "'{PropertyName}' {From} және {To} аралығында болуы керек (осы мәндерді қоспағанда). Енгізілген мән: {PropertyValue}.",
            "CreditCardValidator": "'{PropertyName}' қате карта нөмірі.",
            "ScalePrecisionValidator": "Жалпы алғанда, '{PropertyName}' {ExpectedPrecision} цифрдан аспауы, оның ішінде {ExpectedScale} ондық таңба. Енгізілген мән бүтін бөліктегі {Digits} цифрдан тұрады және {ActualScale} ондық белгі.",
            "EmptyValidator": "'{PropertyName}' бос болуы керек.",
            "NullValidator": "'{PropertyName}' бос болуы керек.",
            "EnumValidator": "'{PropertyName}' жарамсыз мәнді қамтиды '{PropertyValue}'.",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' таңбаларының саны {min_length} және {max_length} арасында болуы керек.",
            "MinimumLength_Simple": "'{PropertyName}' таңбаларының саны мынадан - {min_length} кем емес болуы керек.",
            "MaximumLength_Simple": "'{PropertyName}' таңбаларының саны мынадан - {max_length} көп емес болуы керек.",
            "ExactLength_Simple": "'{PropertyName}' ұзындығы {max_length} таңба болуы керек.",
            "InclusiveBetween_Simple": "'{PropertyName}' {From} және {To} аралығында болуы керек.",
        }
        return dicc.get(key, None)
