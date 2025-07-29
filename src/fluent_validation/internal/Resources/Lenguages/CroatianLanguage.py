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


class CroatianLanguage:
    Culture: str = "hr"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' nije ispravna e-mail adresa.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' mora biti veći ili jednak '{ComparisonValue}'.",
            "GreaterThanValidator": "'{PropertyName}' mora biti veći od '{ComparisonValue}'.",
            "LengthValidator": "'{PropertyName}' mora biti između {min_length} i {max_length} znakova. Upisali ste {total_length} znakova.",
            "MinimumLengthValidator": "'{PropertyName}' mora imati duljinu veću ili jednaku {min_length}. Unijeli ste {total_length} znakova.",
            "MaximumLengthValidator": "'{PropertyName}' mora imati duljinu manju ili jednaku {max_length}. Unijeli ste {total_length} znakova.",
            "LessThanOrEqualValidator": "'{PropertyName}' mora biti manji ili jednak '{ComparisonValue}'.",
            "LessThanValidator": "'{PropertyName}' mora biti manji od '{ComparisonValue}'.",
            "NotEmptyValidator": "'{PropertyName}' ne smije biti prazan.",
            "NotEqualValidator": "'{PropertyName}' ne smije biti jednak '{ComparisonValue}'.",
            "NotNullValidator": "Niste upisali '{PropertyName}'",
            "PredicateValidator": "'{PropertyName}' nije ispravan.",
            "AsyncPredicateValidator": "'{PropertyName}' nije ispravan.",
            "RegularExpressionValidator": "'{PropertyName}' nije u odgovarajućem formatu.",
            "EqualValidator": "'{PropertyName}' mora biti jednak '{ComparisonValue}'.",
            "ExactLengthValidator": "'{PropertyName}' mora sadržavati {max_length} znakova. Upisali ste {total_length} znakova.",
            "InclusiveBetweenValidator": "'{PropertyName}' mora biti između {From} i {To}. Upisali ste {PropertyValue}.",
            "ExclusiveBetweenValidator": "'{PropertyName}' mora biti između {From} i {To} (ne uključujući granice). Upisali ste {PropertyValue}.",
            "CreditCardValidator": "'{PropertyName}' nije odgovarajuća kreditna kartica.",
            "ScalePrecisionValidator": "'{PropertyName}' ne smije imati više od {ExpectedPrecision} znamenki, sa {ExpectedScale} decimalna mjesta. Upisali ste {Digits} znamenki i {ActualScale} decimalna mjesta.",
            "EmptyValidator": "'{PropertyName}' mora biti prazan.",
            "NullValidator": "'{PropertyName}' mora biti prazan.",
            "EnumValidator": "'{PropertyName}' ima raspon vrijednosti koji ne uključuje '{PropertyValue}'.",
            #  Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' mora biti između {min_length} i {max_length} znakova.",
            "MinimumLength_Simple": "'{PropertyName}' mora imati duljinu veću ili jednaku {min_length}.",
            "MaximumLength_Simple": "'{PropertyName}' mora imati duljinu manju ili jednaku {max_length}.",
            "ExactLength_Simple": "'{PropertyName}' mora sadržavati {max_length} znakova.",
            "InclusiveBetween_Simple": "'{PropertyName}' mora biti između {From} i {To}.",
        }
        return dicc.get(key, None)
