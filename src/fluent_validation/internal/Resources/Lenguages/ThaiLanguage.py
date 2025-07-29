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


class ThaiLanguage:
    Culture: str = "th"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}'ไม่ใช่อีเมลที่ถูกต้อง",
            "GreaterThanOrEqualValidator": "'{PropertyName}'ต้องมีค่ามากกว่าหรือเท่ากับ'{ComparisonValue}'",
            "GreaterThanValidator": "'{PropertyName}'ต้องมีค่ามากกว่า'{ComparisonValue}'",
            "LengthValidator": "'{PropertyName}'ต้องมีจำนวนตัวอักษรอยู่ระหว่าง{min_length}และ{max_length}ตัวอักษร คุณให้ข้อมูลทั้งหมด{total_length}ตัวอักษร",
            "MinimumLengthValidator": "จำนวนตัวอักษร'{PropertyName}'ต้องมีอย่างน้อย{min_length}ตัวอักษร คุณให้ข้อมูลทั้งหมด{total_length}ตัวอักษร",
            "MaximumLengthValidator": "จำนวนตัวอักษร'{PropertyName}'ต้องเท่ากับ{max_length}ตัวอักษรหรือน้อยกว่า คุณให้ข้อมูลทั้งหมด{total_length}ตัวอักษร",
            "LessThanOrEqualValidator": "'{PropertyName}'ต้องมีค่าน้อยกว่าหรือเท่ากับ'{ComparisonValue}'.",
            "LessThanValidator": "'{PropertyName}'ต้องมีค่าน้อยกว่า'{ComparisonValue}'",
            "NotEmptyValidator": "'{PropertyName}'ต้องไม่มีค่าว่างเปล่า",
            "NotEqualValidator": "'{PropertyName}'ต้องไม่เท่ากับ'{ComparisonValue}'",
            "NotNullValidator": "'{PropertyName}'ต้องมีค่า",
            "PredicateValidator": "ข้อมูลของ'{PropertyName}'ผิดกฎเกณฑ์ที่กำหนดไว้",
            "AsyncPredicateValidator": "ข้อมูลของ'{PropertyName}'ผิดกฎเกณฑ์ที่กำหนดไว้",
            "RegularExpressionValidator": "ข้อมูลของ'{PropertyName}'ผิดรูปแบบ",
            "EqualValidator": "'{PropertyName}'ต้องมีค่าเท่ากับ'{ComparisonValue}'",
            "ExactLengthValidator": "'{PropertyName}'ต้องมีจำนวนตัวอักษร{max_length}ตัวอักษร คุณให้ข้อมูลทั้งหมด{total_length}ตัวอักษร",
            "InclusiveBetweenValidator": "'{PropertyName}'ต้องมีค่าระหว่าง{From}ถึง{To} คุณให้ข้อมูล{PropertyValue}",
            "ExclusiveBetweenValidator": "'{PropertyName}'ต้องมีค่าอยู่ระหว่างแต่ไม่รวม{From}และ{To} คุณให้ข้อมูล{PropertyValue}",
            "CreditCardValidator": "'{PropertyName}'ไม่ใช่ตัวเลขบัตรเครดิตที่ถูกต้อง",
            "ScalePrecisionValidator": "'{PropertyName}'ต้องไม่มีจำนวนตัวเลขมากกว่า{ExpectedPrecision}ตำแหน่งทั้งหมด และมีจุดทศนิยม{ExpectedScale}ตำแหน่ง ข้อมูลมีตัวเลขค่าเต็ม{Digits}ตำแหน่งและจุดทศนิยม{ActualScale}ตำแหน่ง",
            "EmptyValidator": "'{PropertyName}'ต้องมีค่าว่างเปล่า",
            "NullValidator": "'{PropertyName}'ต้องไม่มีค่า",
            "EnumValidator": "ค่าของ'{PropertyValue}'ไม่ได้อยู่ในค่าของ'{PropertyName}'",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}'ต้องมีจำนวนตัวอักษรระหว่าง{min_length}แหละ{max_length}ตัวอักษร",
            "MinimumLength_Simple": "จำนวนตัวอักษรของ'{PropertyName}'ต้องมีอย่างน้อย{min_length}ตัวอักษร",
            "MaximumLength_Simple": "จำนวนตัวอักษรของ'{PropertyName}'ต้องเท่ากับหรือน้อยกว่า{max_length}ตัวอักษร",
            "ExactLength_Simple": "จำนวนตัวอักษรของ'{PropertyName}'ต้องเท่ากับ{max_length}ตัวอักษร",
            "InclusiveBetween_Simple": "'{PropertyName}'ต้องมีค่าระหว่าง{From}ถึง{To}",
        }
        return dicc.get(key, None)
