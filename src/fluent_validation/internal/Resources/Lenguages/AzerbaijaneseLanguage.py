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


class AzerbaijaneseLanguage:
    Culture: str = "az"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}'  keçərli bir e-poçt ünvanı deyil.",
            "GreaterThanOrEqualValidator": "'{PropertyName}' dəyəri '{ComparisonValue}' dəyərindən böyük və ya bərabər olmalıdır.",
            "GreaterThanValidator": "'{PropertyName}' dəyəri '{ComparisonValue}' dəyərindən böyük olmalıdır.",
            "LengthValidator": "'{PropertyName}', {min_length} və {max_length} aralığında simvol uzunluğunda olmalıdır . Ümumilikdə {total_length} ədəd simvol daxil etmisiniz.",
            "MinimumLengthValidator": "'{PropertyName}', {min_length} simvoldan böyük və ya bərabər olmalıdır. {total_length} simvol daxil etmisiniz.",
            "MaximumLengthValidator": "'{PropertyName}', {max_length} simvoldan kiçik və ya bərabər olmalıdır. {total_length} simvol daxil etmisiniz.",
            "LessThanOrEqualValidator": "'{PropertyName}', '{ComparisonValue}' dəyərindən kiçik və ya bərabər olmalıdır.",
            "LessThanValidator": "'{PropertyName}', '{ComparisonValue}' dəyərindən kiçik olmalıdır.",
            "NotEmptyValidator": "'{PropertyName}' boş olmamalıdır.",
            "NotEqualValidator": "'{PropertyName}', '{ComparisonValue}' dəyərinə bərabər olmamalıdır.",
            "NotNullValidator": "'{PropertyName}' daxil edilməlidir.",
            "PredicateValidator": "'{PropertyName}' təyin edilmiş şərtlərə uyğun deyil.",
            "AsyncPredicateValidator": "{PropertyName}' təyin edilmiş şərtlərə uyğun deyil.",
            "RegularExpressionValidator": "'{PropertyName}' dəyərinin formatı düzgün değil.",
            "EqualValidator": "'{PropertyName}', '{ComparisonValue}' dəyərinə bərabər olmalıdır.",
            "ExactLengthValidator": "'{PropertyName}', {max_length} simvol uzunluğunda olmalıdır. {total_length} ədəd simvol daxil etmisiniz.",
            "InclusiveBetweenValidator": "'{PropertyName}', {From} və {To} aralığında olmalıdır. {PropertyValue} dəyərini daxil etmisiniz.",
            "ExclusiveBetweenValidator": "'{PropertyName}', {From} (daxil deyil) və {To} (daxil deyil) aralığında olmalıdır. {PropertyValue} dəyərini daxil etmisiniz.",
            "CreditCardValidator": "'{PropertyName}' keçərli kredit kartı nömrəsi değil.",
            "ScalePrecisionValidator": "'{PropertyName}' icazə verilən {ExpectedScale} rəqəmli onluq hissə ilə birlikdə ümumilikdə {ExpectedPrecision} rəqəmdən ibarət olmalıdır. {Digits} tam və {ActualScale} onluq ədəd tapıldı.",
            "EmptyValidator": "'{PropertyName}' boş olmalıdır.",
            "NullValidator": "'{PropertyName}' boş olmalıdır.",
            "EnumValidator": "'{PropertyName}' -in mümkün qiymətlər çoxluğuna '{PropertyValue}' daxil deyil.",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}', {min_length} və {max_length} aralığında simvol uzunluğunda olmalıdır.",
            "MinimumLength_Simple": "'{PropertyName}', {min_length} simvoldan böyük və ya bərabər olmalıdır.",
            "MaximumLength_Simple": "'{PropertyName}', {max_length} simvoldan kiçik və ya bərabər olmalıdır.",
            "ExactLength_Simple": "'{PropertyName}', {max_length} simvol uzunluğunda olmalıdır.",
            "InclusiveBetween_Simple": "'{PropertyName}', {From} və {To} aralığında olmalıdır.",
        }
        return dicc.get(key, None)
