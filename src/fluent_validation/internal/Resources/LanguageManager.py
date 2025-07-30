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

from typing import Callable, Optional, override

from .ILanguageManager import ILanguageManager, CultureInfo
from .Lenguages import (
    EnglishLanguage,
    AlbanianLanguage,
    ArabicLanguage,
    AzerbaijaneseLanguage,
    BengaliLanguage,
    BosnianLanguage,
    BulgarianLanguage,
    CatalanLanguage,
    ChineseSimplifiedLanguage,
    ChineseTraditionalLanguage,
    CroatianLanguage,
    CzechLanguage,
    DanishLanguage,
    DutchLanguage,
    EstonianLanguage,
    FinnishLanguage,
    FrenchLanguage,
    GermanLanguage,
    GeorgianLanguage,
    GreekLanguage,
    HebrewLanguage,
    HindiLanguage,
    HungarianLanguage,
    IcelandicLanguage,
    IndonesianLanguage,
    ItalianLanguage,
    JapaneseLanguage,
    KazakhLanguage,
    KhmerLanguage,
    KoreanLanguage,
    LatvianLanguage,
    MacedonianLanguage,
    NorwegianBokmalLanguage,
    NorwegianNynorskLanguage,
    PersianLanguage,
    PolishLanguage,
    PortugueseLanguage,
    PortugueseBrazilLanguage,
    RomanianLanguage,
    RomanshLanguage,
    RussianLanguage,
    SerbianCyrillicLanguage,
    SerbianLatinLanguage,
    SlovakLanguage,
    SlovenianLanguage,
    SpanishLanguage,
    SwedishLanguage,
    TajikLanguage,
    TamilLanguage,
    TeluguLanguage,
    ThaiLanguage,
    TurkishLanguage,
    UkrainianLanguage,
    UzbekCyrillicLanguage,
    UzbekLatinLanguage,
    VietnameseLanguage,
    WelshLanguage,
)


class LanguageManagerExtension:
    def ResolveErrorMessageUsingErrorCode(languageManager: ILanguageManager, error_code: str, fall_back_Key: str) -> str:
        if error_code is not None:
            result: str = languageManager.GetString(error_code)

            if result is not None and not result.isspace():
                return result
        return languageManager.GetString(fall_back_Key)


class LanguageManager(ILanguageManager, LanguageManagerExtension):
    """Allows the default error message translations to be managed."""

    _enabled: bool
    _languages: dict[str, str]

    def __init__(self):
        self._languages = {}
        self._enabled = True
        self._culture: Optional[CultureInfo] = None

    @property
    def Enabled(self) -> bool:
        return self._enabled

    @Enabled.setter
    def Enabled(self, value: bool) -> None:
        self._enabled = value

    @staticmethod
    def GetTranslation(culture: str, key: str) -> Optional[str]:
        """
        Language factory.

        Args:
            culture: The culture code
            key: The key to load

        Returns:
        Optional[str]: The corresponding Language instance or null.
        """

        dicc: dict[str, Callable[[str], str]] = {
            EnglishLanguage.AmericanCulture: lambda x: EnglishLanguage.GetTranslation(x),
            EnglishLanguage.BritishCulture: lambda x: EnglishLanguage.GetTranslation(x),
            EnglishLanguage.Culture: lambda x: EnglishLanguage.GetTranslation(x),
            AlbanianLanguage.Culture: lambda x: AlbanianLanguage.GetTranslation(x),
            ArabicLanguage.Culture: lambda x: ArabicLanguage.GetTranslation(x),
            AzerbaijaneseLanguage.Culture: lambda x: AzerbaijaneseLanguage.GetTranslation(x),
            BengaliLanguage.Culture: lambda x: BengaliLanguage.GetTranslation(x),
            BosnianLanguage.Culture: lambda x: BosnianLanguage.GetTranslation(x),
            BulgarianLanguage.Culture: lambda x: BulgarianLanguage.GetTranslation(x),
            CatalanLanguage.Culture: lambda x: CatalanLanguage.GetTranslation(x),
            ChineseSimplifiedLanguage.Culture: lambda x: ChineseSimplifiedLanguage.GetTranslation(x),
            ChineseTraditionalLanguage.Culture: lambda x: ChineseTraditionalLanguage.GetTranslation(x),
            CroatianLanguage.Culture: lambda x: CroatianLanguage.GetTranslation(x),
            CzechLanguage.Culture: lambda x: CzechLanguage.GetTranslation(x),
            DanishLanguage.Culture: lambda x: DanishLanguage.GetTranslation(x),
            DutchLanguage.Culture: lambda x: DutchLanguage.GetTranslation(x),
            EstonianLanguage.Culture: lambda x: EstonianLanguage.GetTranslation(x),
            FinnishLanguage.Culture: lambda x: FinnishLanguage.GetTranslation(x),
            FrenchLanguage.Culture: lambda x: FrenchLanguage.GetTranslation(x),
            GermanLanguage.Culture: lambda x: GermanLanguage.GetTranslation(x),
            GeorgianLanguage.Culture: lambda x: GeorgianLanguage.GetTranslation(x),
            GreekLanguage.Culture: lambda x: GreekLanguage.GetTranslation(x),
            HebrewLanguage.Culture: lambda x: HebrewLanguage.GetTranslation(x),
            HindiLanguage.Culture: lambda x: HindiLanguage.GetTranslation(x),
            HungarianLanguage.Culture: lambda x: HungarianLanguage.GetTranslation(x),
            IcelandicLanguage.Culture: lambda x: IcelandicLanguage.GetTranslation(x),
            IndonesianLanguage.Culture: lambda x: IndonesianLanguage.GetTranslation(x),
            ItalianLanguage.Culture: lambda x: ItalianLanguage.GetTranslation(x),
            JapaneseLanguage.Culture: lambda x: JapaneseLanguage.GetTranslation(x),
            KazakhLanguage.Culture: lambda x: KazakhLanguage.GetTranslation(x),
            KhmerLanguage.Culture: lambda x: KhmerLanguage.GetTranslation(x),
            KoreanLanguage.Culture: lambda x: KoreanLanguage.GetTranslation(x),
            LatvianLanguage.Culture: lambda x: LatvianLanguage.GetTranslation(x),
            MacedonianLanguage.Culture: lambda x: MacedonianLanguage.GetTranslation(x),
            NorwegianBokmalLanguage.Culture: lambda x: NorwegianBokmalLanguage.GetTranslation(x),
            NorwegianNynorskLanguage.Culture: lambda x: NorwegianNynorskLanguage.GetTranslation(x),
            PersianLanguage.Culture: lambda x: PersianLanguage.GetTranslation(x),
            PolishLanguage.Culture: lambda x: PolishLanguage.GetTranslation(x),
            PortugueseLanguage.Culture: lambda x: PortugueseLanguage.GetTranslation(x),
            PortugueseBrazilLanguage.Culture: lambda x: PortugueseBrazilLanguage.GetTranslation(x),
            RomanianLanguage.Culture: lambda x: RomanianLanguage.GetTranslation(x),
            RomanshLanguage.Culture: lambda x: RomanshLanguage.GetTranslation(x),
            RussianLanguage.Culture: lambda x: RussianLanguage.GetTranslation(x),
            SerbianCyrillicLanguage.Culture: lambda x: SerbianCyrillicLanguage.GetTranslation(x),
            SerbianLatinLanguage.Culture: lambda x: SerbianLatinLanguage.GetTranslation(x),
            SlovakLanguage.Culture: lambda x: SlovakLanguage.GetTranslation(x),
            SlovenianLanguage.Culture: lambda x: SlovenianLanguage.GetTranslation(x),
            SpanishLanguage.Culture: lambda x: SpanishLanguage.GetTranslation(x),
            SwedishLanguage.Culture: lambda x: SwedishLanguage.GetTranslation(x),
            TajikLanguage.Culture: lambda x: TajikLanguage.GetTranslation(x),
            TamilLanguage.Culture: lambda x: TamilLanguage.GetTranslation(x),
            TeluguLanguage.Culture: lambda x: TeluguLanguage.GetTranslation(x),
            ThaiLanguage.Culture: lambda x: ThaiLanguage.GetTranslation(x),
            TurkishLanguage.Culture: lambda x: TurkishLanguage.GetTranslation(x),
            UkrainianLanguage.Culture: lambda x: UkrainianLanguage.GetTranslation(x),
            UzbekCyrillicLanguage.Culture: lambda x: UzbekCyrillicLanguage.GetTranslation(x),
            UzbekLatinLanguage.Culture: lambda x: UzbekLatinLanguage.GetTranslation(x),
            VietnameseLanguage.Culture: lambda x: VietnameseLanguage.GetTranslation(x),
            WelshLanguage.Culture: lambda x: WelshLanguage.GetTranslation(x),
        }
        value = dicc.get(culture, None)
        return value(key) if value is not None else None

    @property
    @override
    def Culture(self) -> Optional[CultureInfo]:
        return self._culture

    @Culture.setter
    def Culture(self, value: CultureInfo) -> None:
        self._culture = value

    def Clear(self) -> None:
        """Removes all languages except the default."""
        self._languages.clear()

    def AddTranslation(self, culture: str, key: str, message: str) -> None:
        """Adds a custom translation for a specific culture and key."""

        if culture == "":
            raise ValueError(f"'{culture}' must not be empty")
        if key == "":
            raise ValueError(f"'{key}' must not be empty")
        if message == "":
            raise ValueError(f"'{message}' must not be empty")

        self._languages[f"{culture}:{key}"] = message

    @override
    def GetString(self, key: str, culture: Optional[CultureInfo] = None) -> str:
        """
        Gets a translated string based on its key. If the culture is specific and it isn't registered, we try the neutral culture instead.
        If no matching culture is found  to be registered we use English.

        Args:
            key: The key
            culture: The culture to translate into

        Return:
            str

        """
        if self._enabled:
            if culture is None:
                if self.Culture is not None:
                    culture = self.Culture
                else:
                    culture = CultureInfo.CurrentUICulture()

            currentCultureKey: str = culture.Name + ":" + key

            value = self._languages.get(currentCultureKey, self.GetTranslation(culture.Name, key))
            currentCulture = culture
            while value is None and currentCulture.Parent != CultureInfo.InvariantCulture():
                currentCulture = currentCulture.Parent
                parentCultureKey: str = currentCulture.Name + ":" + key
                value = self._languages.get(parentCultureKey, self.GetTranslation(currentCulture.Name, key))

            if value is None and culture.Name != EnglishLanguage.Culture:
                # If it couldn't be found, try the fallback English (if we haven't tried it already).
                if not culture.IsNeutralCulture and culture.Parent.Name != EnglishLanguage.Culture:
                    value = self._languages.get(EnglishLanguage.Culture + ":" + key, EnglishLanguage.GetTranslation(key))
        else:
            value = self._languages.get(EnglishLanguage.Culture + ":" + key, EnglishLanguage.GetTranslation(key))

        return value if value is not None else ""
