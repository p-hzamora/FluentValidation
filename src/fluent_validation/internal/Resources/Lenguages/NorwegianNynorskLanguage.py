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


class NorwegianNynorskLanguage:
    Culture: str = "nn"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' er ikkje ei gyldig e-postadresse.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' skal vera større enn eller lik '{ComparisonValue}'.",
            "GreaterThanValidator": "'{PropertyName}' skal vera større enn '{ComparisonValue}'.",
            "LengthValidator": "'{PropertyName}' skal vere mellom {min_length} og {max_length} teikn. Du har tasta inn {total_length} teikn.",
            "MinimumLengthValidator": "'{PropertyName}' skal vera større enn eller lik {min_length} teikn. Du tasta inn {total_length} teikn.",
            "MaximumLengthValidator": "'{PropertyName}' skal vera mindre enn eller lik {max_length} teikn. Du tasta inn {total_length} teikn.",
            "LessThanOrEqualValidator": "'{PropertyName}' skal vera mindre enn eller lik '{ComparisonValue}'.",
            "LessThanValidator": "'{PropertyName}' skal vera mindre enn '{ComparisonValue}'.",
            "NotEmptyValidator": "'{PropertyName}' kan ikkje vera tom.",
            "NotEqualValidator": "'{PropertyName}' kan ikkje vera lik '{ComparisonValue}'.",
            "NotNullValidator": "'{PropertyName}' kan ikkje vera tom.",
            "PredicateValidator": "Den angjevne føresetnaden var ikkje oppfylt for '{PropertyName}'.",
            "AsyncPredicateValidator": "Den angjevne føresetnaden var ikkje oppfylt for '{PropertyName}'.",
            "RegularExpressionValidator": "'{PropertyName}' har ikkje rett format.",
            "EqualValidator": "'{PropertyName}' skal vera lik '{ComparisonValue}'.",
            "ExactLengthValidator": "'{PropertyName}' skal vera {max_length} teikn langt. Du har tasta inn {total_length} teikn.",
            "InclusiveBetweenValidator": "'{PropertyName}' skal vera mellom {From} og {To}. Du har tasta inn {PropertyValue}.",
            "ExclusiveBetweenValidator": "'{PropertyName}' skal vera mellom {From} og {To} (unntatt). Du har tasta inn {PropertyValue}.",
            "CreditCardValidator": "'{PropertyName}' er ikkje eit gyldig kredittkortnummer.",
            "ScalePrecisionValidator": "'{PropertyName}' kan ikkje vera meir enn {ExpectedPrecision} siffer totalt, inkludert {ExpectedScale} desimalar. {Digits} siffer og {ActualScale} desimalar vart funnen.",
            "EmptyValidator": "'{PropertyName}' skal vera tomt.",
            "NullValidator": "'{PropertyName}' skal vera tomt.",
            "EnumValidator": "'{PropertyName}' har ei rekkje verdiar men inneheld ikkje '{PropertyValue}'.",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' skal vera mellom {min_length} og {max_length} teikn.",
            "MinimumLength_Simple": "'{PropertyName}' skal vera større enn eller lik {min_length} teikn.",
            "MaximumLength_Simple": "'{PropertyName}' skal vera mindre enn eller lik {max_length} teikn.",
            "ExactLength_Simple": "'{PropertyName}' skal vera {max_length} teikn langt.",
            "InclusiveBetween_Simple": "'{PropertyName}' skal vera mellom {From} og {To}.",
        }
        return dicc.get(key, None)
