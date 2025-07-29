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


class NorwegianBokmalLanguage:
    Culture: str = "nb"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' er ikke en gyldig e-postadresse.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' skal være større enn eller lik '{ComparisonValue}'.",
            "GreaterThanValidator": "'{PropertyName}' skal være større enn '{ComparisonValue}'.",
            "LengthValidator": "'{PropertyName}' skal være mellom {min_length} og {max_length} tegn. Du har tastet inn {total_length} tegn.",
            "MinimumLengthValidator": "'{PropertyName}' skal være større enn eller lik {min_length} tegn. Du tastet inn {total_length} tegn.",
            "MaximumLengthValidator": "'{PropertyName}' skal være mindre enn eller lik {max_length} tegn. Du tastet inn {total_length} tegn.",
            "LessThanOrEqualValidator": "'{PropertyName}' skal være mindre enn eller lik '{ComparisonValue}'.",
            "LessThanValidator": "'{PropertyName}' skal være mindre enn '{ComparisonValue}'.",
            "NotEmptyValidator": "'{PropertyName}' kan ikke være tom.",
            "NotEqualValidator": "'{PropertyName}' kan ikke være lik med '{ComparisonValue}'.",
            "NotNullValidator": "'{PropertyName}' kan ikke være tom.",
            "PredicateValidator": "Den angitte betingelsen var ikke oppfylt for '{PropertyName}'.",
            "AsyncPredicateValidator": "Den angitte betingelsen var ikke oppfylt for '{PropertyName}'.",
            "RegularExpressionValidator": "'{PropertyName}' har ikke riktig format.",
            "EqualValidator": "'{PropertyName}' skal være lik med '{ComparisonValue}'.",
            "ExactLengthValidator": "'{PropertyName}' skal være {max_length} tegn langt. Du har tastet inn {total_length} tegn.",
            "InclusiveBetweenValidator": "'{PropertyName}' skal være mellom {From} og {To}. Du har tastet inn {PropertyValue}.",
            "ExclusiveBetweenValidator": "'{PropertyName}' skal være mellom {From} og {To} (eksklusiv). Du har tastet inn {PropertyValue}.",
            "CreditCardValidator": "'{PropertyName}' er ikke et gyldig kredittkortnummer.",
            "ScalePrecisionValidator": "'{PropertyName}' kan ikke være mer enn {ExpectedPrecision} siffer totalt, med hensyn til {ExpectedScale} desimaler. {Digits} siffer og {ActualScale} desimaler ble funnet.",
            "EmptyValidator": "'{PropertyName}' skal være tomt.",
            "NullValidator": "'{PropertyName}' skal være tomt.",
            "EnumValidator": "'{PropertyName}' har en rekke verdier men inneholder ikke '{PropertyValue}'.",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' skal være mellom {min_length} og {max_length} tegn.",
            "MinimumLength_Simple": "'{PropertyName}' skal være større enn eller lik {min_length} tegn.",
            "MaximumLength_Simple": "'{PropertyName}' skal være mindre enn eller lik {max_length} tegn.",
            "ExactLength_Simple": "'{PropertyName}' skal være {max_length} tegn langt.",
            "InclusiveBetween_Simple": "'{PropertyName}' skal være mellom {From} og {To}.",
        }
        return dicc.get(key, None)
