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


class RomanshLanguage:
    Culture: str = "rm"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' n'è betg ina adressa email valaibla.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' duai esser pli grond u uguagli a '{ComparisonValue}'.",
            "GreaterThanValidator": "'{PropertyName}' duai esser pli grond che '{ComparisonValue}'.",
            "LengthValidator": "'{PropertyName}' duai esser lunga tranter {min_length} e {max_length} caracters. Vus avais mess {total_length} caracters.",
            "MinimumLengthValidator": "La lunghezza da '{PropertyName}' duai esser almain {min_length} caracters. Vus avais mess {total_length} caracters.",
            "MaximumLengthValidator": "La lunghezza da '{PropertyName}' po esser massim {max_length} caracters. Vus avais mess {total_length} caracters.",
            "LessThanOrEqualValidator": "'{PropertyName}' duai esser pli pitschen u uguagli a '{ComparisonValue}'.",
            "LessThanValidator": "'{PropertyName}' duai esser pli pitschen che '{ComparisonValue}'.",
            "NotEmptyValidator": "'{PropertyName}' n'ha betg da vegnir mussà.",
            "NotEqualValidator": "'{PropertyName}' n'ha betg da vegnir uguaglià cun '{ComparisonValue}'.",
            "NotNullValidator": "'{PropertyName}' n'ha betg da vegnir mussà.",
            "PredicateValidator": "La condiziun specificada n'è betg vegnida ademplida per ''{PropertyName}'.",
            "AsyncPredicateValidator": "La condiziun specificada n'è betg vegnida ademplida per ''{PropertyName}'.",
            "RegularExpressionValidator": "'{PropertyName}' n'è betg en il format correct.",
            "EqualValidator": "'{PropertyName}' duai esser uguaglià cun '{ComparisonValue}'.",
            "ExactLengthValidator": "'{PropertyName}' duai esser lunga {max_length} caracters. Vus avais mess {total_length} caracters.",
            "ExclusiveBetweenValidator": "'{PropertyName}' duai esser tranter {From} e {To} (exclusiv). Vus avais mess {PropertyValue}.",
            "InclusiveBetweenValidator": "'{PropertyName}' duai esser tranter {From} e {To}. Vus avais mess {PropertyValue}.",
            "CreditCardValidator": "'{PropertyName}' n'è betg ina cifra da carta da credit valaibla.",
            "ScalePrecisionValidator": "'{PropertyName}' n'ha betg pli che {ExpectedPrecision} cifras en total, cun toleranza per {ExpectedScale} decimalas. Sunt vegnidas chattadas {Digits} cifras e {ActualScale} decimalas.",
            "EmptyValidator": "'{PropertyName}' n'ha betg da vegnir mussà.",
            "NullValidator": "'{PropertyName}' n'ha betg da vegnir mussà.",
            "EnumValidator": "'{PropertyName}' ha ina gama da valurs che n'incloa betg '{PropertyValue}'.",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' duai esser lunga tranter {min_length} e {max_length} caracters.",
            "MinimumLength_Simple": "La lunghezza da '{PropertyName}' duai esser almain {min_length} caracters.",
            "MaximumLength_Simple": "La lunghezza da '{PropertyName}' po esser massim {max_length} caracters.",
            "ExactLength_Simple": "'{PropertyName}' duai esser lunga {max_length} caracters.",
            "InclusiveBetween_Simple": "'{PropertyName}' duai esser tranter {From} e {To}.",
        }
        return dicc.get(key, None)
