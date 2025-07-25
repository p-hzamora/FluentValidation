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


class IcelandicLanguage:
    Culture: str = "is"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' er ekki gilt netfang.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' verður að vera meiri en eða jöfn '{ComparisonValue}'.",
            "GreaterThanValidator": "'{PropertyName}' verður að vera meiri en '{ComparisonValue}'.",
            "LengthValidator": "'{PropertyName}' verður að vera á milli {min_length} og {max_length} stafir. Þú slóst inn {total_length} stafi.",
            "MinimumLengthValidator": "Lengdin '{PropertyName}' verður að vera að minnsta kosti {min_length} stafir. Þú slóst inn {total_length} stafi.",
            "MaximumLengthValidator": "Lengd '{PropertyName}' verður að vera {max_length} stafir eða færri. Þú slóst inn {total_length} stafi.",
            "LessThanOrEqualValidator": "'{PropertyName}' verður að vera minna en eða jafnt og '{ComparisonValue}'.",
            "LessThanValidator": "'{PropertyName}' verður að vera minna en '{ComparisonValue}'.",
            "NotEmptyValidator": "'{PropertyName} má ekki vera tómt.",
            "NotEqualValidator": "'{PropertyName}' má ekki vera jafnt og '{ComparisonValue}'.",
            "NotNullValidator": "'{PropertyName} má ekki vera tómt.",
            "PredicateValidator": "Tilgreindu skilyrði var ekki uppfyllt fyrir '{PropertyName}'.",
            "AsyncPredicateValidator": "Tilgreindu skilyrði var ekki uppfyllt fyrir '{PropertyName}'.",
            "RegularExpressionValidator": "'{PropertyName}' er ekki með réttu sniði.",
            "EqualValidator": "'{PropertyName}' verður að vera jafnt og '{ComparisonValue}'.",
            "ExactLengthValidator": "'{PropertyName}' verður að vera {max_length} stafir að lengd. Þú slóst inn {total_length} stafi.",
            "InclusiveBetweenValidator": "'{PropertyName}' verður að frá {From} til {To}. Þú slóst inn {PropertyValue}.",
            "ExclusiveBetweenValidator": "'{PropertyName}' verður að vera á milli {From} og {To}. Þú slóst inn {PropertyValue}.",
            "CreditCardValidator": "'{PropertyName}' er ekki gilt kreditkortanúmer.",
            "ScalePrecisionValidator": "'{PropertyName}' má ekki vera meira en {ExpectedPrecision} tölustafir samtals, með heimild fyrir {ExpectedScale} aukastöfum. {Digits} tölustafir og {ActualScale} aukastafir fundust.",
            "EmptyValidator": "'{PropertyName}' verður að vera tómt.",
            "NullValidator": "'{PropertyName}' verður að vera tómt.",
            "EnumValidator": "'{PropertyName}' hefur svið gilda sem innihalda ekki '{PropertyValue}'.",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' verður að vera á milli {min_length} og {max_length} stafir.",
            "MinimumLength_Simple": "Lengdin '{PropertyName}' verður að vera að minnsta kosti {min_length} stafir.",
            "MaximumLength_Simple": "Lengd '{PropertyName}' verður að vera {max_length} stafir eða færri.",
            "ExactLength_Simple": "'{PropertyName}' verður að vera {max_length} stafir að lengd.",
            "InclusiveBetween_Simple": "'{PropertyName}' verður að vera á milli {From} og {To}.",
        }
        return dicc.get(key, None)
