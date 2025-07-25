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


class WelshLanguage:
    Culture: str = "cy"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "Nid yw '{PropertyName}' yn gyfeiriad e-bost dilys.",
            "GreaterThanOrEqualValidator": "Rhaid i '{PropertyName}' fod yn fwy na '{ComparisonValue}', neu'n gyfartal ag o.",
            "GreaterThanValidator": "Rhaid i '{PropertyName}' fod yn fwy na '{ComparisonValue}'.",
            "LengthValidator": "Rhaid i '{PropertyName}' fod rhwng {min_length} a {max_length} o nodau. Rydych wedi rhoi {total_length} nod.",
            "MinimumLengthValidator": "Rhaid i '{PropertyName}' fod o leiaf {min_length} nod o hyd. Rydych wedi rhoi {total_length} nod.",
            "MaximumLengthValidator": "Rhaid i '{PropertyName}' fod yn {max_length} nod o hyd neu lai. Rydych wedi rhoi {total_length} nod.",
            "LessThanOrEqualValidator": "Rhaid i '{PropertyName}' fod yn llai na '{ComparisonValue}', neu'n gyfartal ag o.",
            "LessThanValidator": "Rhaid i '{PropertyName}' fod yn llai na '{ComparisonValue}'.",
            "NotEmptyValidator": "Ni ddylai '{PropertyName}' fod yn wag.",
            "NotEqualValidator": "Ni ddylai '{PropertyName}' fod yn gyfartal â '{ComparisonValue}'.",
            "NotNullValidator": "Ni ddylai '{PropertyName}' fod yn wag.",
            "PredicateValidator": "Ni chyflawnwyd y gofyniad penodol ar gyfer '{PropertyName}'.",
            "AsyncPredicateValidator": "Ni chyflawnwyd y gofyniad penodol ar gyfer '{PropertyName}'.",
            "RegularExpressionValidator": "Nid yw '{PropertyName}' yn y fformat cywir.",
            "EqualValidator": "Mae'n rhaid i '{PropertyName}' fod yn gyfartal â '{ComparisonValue}'.",
            "ExactLengthValidator": "Mae'n rhaid i '{PropertyName}' fod yn {max_length} nod o hyd. Rydych wedi rhoi {total_length} nod.",
            "InclusiveBetweenValidator": "Rhaid i '{PropertyName}' fod rhwng {From} a {To}. Rydych wedi rhoi {PropertyValue}.",
            "ExclusiveBetweenValidator": "Rhaid i '{PropertyName}' fod rhwng {From} a {To} (ddim yn gynwysedig). Rydych wedi rhoi {PropertyValue}.",
            "CreditCardValidator": "Nid yw '{PropertyName}' yn rhif cerdyn credyd dilys.",
            "ScalePrecisionValidator": "Ni ddylai '{PropertyName}' fod yn fwy na {ExpectedPrecision} digid i gyd  gan ganiatáu ar gyfer {ExpectedScale} degolyn. Canfuwyd {Digits} digid a {ActualScale} degolyn.",
            "EmptyValidator": "Rhaid i '{PropertyName}' fod yn wag.",
            "NullValidator": "Rhaid i '{PropertyName}' fod yn wag.",
            "EnumValidator": "Mae gan '{PropertyName}' ystod o werthoedd nad ydynt yn cynnwys '{PropertyValue}'.",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "Rhaid i '{PropertyName}' fod rhwng {min_length} a {max_length} o nodau.",
            "MinimumLength_Simple": "Rhaid i '{PropertyName}' fod o leiaf {min_length} nod o hyd.",
            "MaximumLength_Simple": "Rhaid i '{PropertyName}' fod yn {max_length} nod o hyd neu lai.",
            "ExactLength_Simple": "Mae'n rhaid i '{PropertyName}' fod yn {max_length} nod o hyd.",
            "InclusiveBetween_Simple": "Rhaid i '{PropertyName}' fod rhwng {From} a {To}.",
        }
        return dicc.get(key, None)
