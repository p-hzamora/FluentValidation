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


class LatvianLanguage:
    Culture: str = "lv"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' nesatur pareizu e-pasta adresi.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' vērtībai ir jābūt lielākai vai vienādai ar '{ComparisonValue}'.",
            "GreaterThanValidator": "'{PropertyName}' vērtībai ir jābūt lielākai par '{ComparisonValue}'.",
            "LengthValidator": "'{PropertyName}' vērtībai ir jābūt no {min_length} līdz {max_length} simbolu garai. Ievadīti {total_length} simboli.",
            "MinimumLengthValidator": "'{PropertyName}' garumam ir jābūt vismaz {min_length} simbolu garam. Ievadīti {total_length} simboli.",
            "MaximumLengthValidator": "'{PropertyName}' garumam ir jābūt maksimāli {max_length} simbolu garam. Ievadīti {total_length} simboli.",
            "LessThanOrEqualValidator": "'{PropertyName}' vērtībai ir jābūt mazākai vai vienādai ar '{ComparisonValue}'.",
            "LessThanValidator": "'{PropertyName}' vērtībai ir jābūt mazākai par '{ComparisonValue}'.",
            "NotEmptyValidator": "'{PropertyName}' vērtība nevar būt tukša.",
            "NotEqualValidator": "'{PropertyName}' vērtība nedrīkst būt vienāda ar '{ComparisonValue}'.",
            "NotNullValidator": "'{PropertyName}' vērtība nevar būt tukša.",
            "PredicateValidator": "Definētā pārbaude nepieļauj ievadīto '{PropertyName}' vērtību.",
            "AsyncPredicateValidator": "Definētā pārbaude nepieļauj ievadīto '{PropertyName}' vērtību.",
            "RegularExpressionValidator": "'{PropertyName}' nav ievadīts vajadzīgajā formātā.",
            "EqualValidator": "'{PropertyName}' vērtībai ir jābūt vienādai ar '{ComparisonValue}'.",
            "ExactLengthValidator": "'{PropertyName}' vērtībai ir jābūt {max_length} simbolu garai. Ievadīti {total_length} simboli.",
            "InclusiveBetweenValidator": "'{PropertyName}' vērtībai ir jābūt no {From} līdz {To}. Ievadītā vērtība: {PropertyValue}.",
            "ExclusiveBetweenValidator": "'{PropertyName}' vērtībai ir jābūt no {From} līdz {To} (neiekļaujot šīs vērtības). Ievadītā vērtība: {PropertyValue}.",
            "CreditCardValidator": "'{PropertyName}' nesatur pareizu kredītkartes numuru.",
            "ScalePrecisionValidator": "'{PropertyName}' vērtība nedrīkst saturēt vairāk par {ExpectedPrecision} ciparu kopā, tajā skaitā {ExpectedScale} ciparu aiz komata. Ievadītā vērtība satur {Digits} ciparu kopā un {ActualScale} ciparu aiz komata.",
            "EmptyValidator": "'{PropertyName}' jābūt tukšai.",
            "NullValidator": "'{PropertyName}' jābūt tukšai.",
            "EnumValidator": "'{PropertyName}' satur noteiktas vērtības, kuras neietver ievadīto '{PropertyValue}'.",
            #  Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' vērtībai ir jābūt no {min_length} līdz {max_length} simbolu garai.",
            "MinimumLength_Simple": "'{PropertyName}' vērtībai ir jābūt vismaz {min_length} simbolu garai.",
            "MaximumLength_Simple": "'{PropertyName}' vērtībai ir jābūt maksimums {max_length} simbolu garai.",
            "ExactLength_Simple": "'{PropertyName}' vērtībai ir jābūt {max_length} simbolu garai.",
            "InclusiveBetween_Simple": "'{PropertyName}' vērtībai ir jābūt no {From} līdz {To}.",
        }
        return dicc.get(key, None)
