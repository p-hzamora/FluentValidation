from typing import Optional, override

from .ILanguageManager import ILanguageManager, CultureInfo
from .Lenguages import *  # noqa: F403


class LanguageManager(ILanguageManager):
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
        dicc = {
            EnglishLanguage.AmericanCulture: lambda x: EnglishLanguage.GetTranslation(x),  # noqa: F405
            EnglishLanguage.BritishCulture: lambda x: EnglishLanguage.GetTranslation(x),  # noqa: F405
            EnglishLanguage.Culture: lambda x: EnglishLanguage.GetTranslation(x),  # noqa: F405
            # AlbanianLanguage.Culture: lambda x: AlbanianLanguage.GetTranslation(x),  # noqa: F405
            # ArabicLanguage.Culture: lambda x: ArabicLanguage.GetTranslation(x),  # noqa: F405
            # AzerbaijaneseLanguage.Culture: lambda x: AzerbaijaneseLanguage.GetTranslation(x),  # noqa: F405
            # BengaliLanguage.Culture: lambda x: BengaliLanguage.GetTranslation(x),  # noqa: F405
            # BosnianLanguage.Culture: lambda x: BosnianLanguage.GetTranslation(x),  # noqa: F405
            # BulgarianLanguage.Culture: lambda x: BulgarianLanguage.GetTranslation(x),  # noqa: F405
            # ChineseSimplifiedLanguage.Culture: lambda x: ChineseSimplifiedLanguage.GetTranslation(x),  # noqa: F405
            # ChineseTraditionalLanguage.Culture: lambda x: ChineseTraditionalLanguage.GetTranslation(x),  # noqa: F405
            # CroatianLanguage.Culture: lambda x: CroatianLanguage.GetTranslation(x),  # noqa: F405
            # CzechLanguage.Culture: lambda x: CzechLanguage.GetTranslation(x),  # noqa: F405
            # DanishLanguage.Culture: lambda x: DanishLanguage.GetTranslation(x),  # noqa: F405
            # DutchLanguage.Culture: lambda x: DutchLanguage.GetTranslation(x),  # noqa: F405
            # FinnishLanguage.Culture: lambda x: FinnishLanguage.GetTranslation(x),  # noqa: F405
            # EstonianLanguage.Culture: lambda x: EstonianLanguage.GetTranslation(x),  # noqa: F405
            # FrenchLanguage.Culture: lambda x: FrenchLanguage.GetTranslation(x),  # noqa: F405
            # GermanLanguage.Culture: lambda x: GermanLanguage.GetTranslation(x),  # noqa: F405
            # GeorgianLanguage.Culture: lambda x: GeorgianLanguage.GetTranslation(x),  # noqa: F405
            # GreekLanguage.Culture: lambda x: GreekLanguage.GetTranslation(x),  # noqa: F405
            # HebrewLanguage.Culture: lambda x: HebrewLanguage.GetTranslation(x),  # noqa: F405
            # HindiLanguage.Culture: lambda x: HindiLanguage.GetTranslation(x),  # noqa: F405
            # HungarianLanguage.Culture: lambda x: HungarianLanguage.GetTranslation(x),  # noqa: F405
            # IcelandicLanguage.Culture: lambda x: IcelandicLanguage.GetTranslation(x),  # noqa: F405
            # ItalianLanguage.Culture: lambda x: ItalianLanguage.GetTranslation(x),  # noqa: F405
            # IndonesianLanguage.Culture: lambda x: IndonesianLanguage.GetTranslation(x),  # noqa: F405
            # JapaneseLanguage.Culture: lambda x: JapaneseLanguage.GetTranslation(x),  # noqa: F405
            # KazakhLanguage.Culture: lambda x: KazakhLanguage.GetTranslation(x),  # noqa: F405
            # KhmerLanguage.Culture: lambda x: KhmerLanguage.GetTranslation(x),  # noqa: F405
            # KoreanLanguage.Culture: lambda x: KoreanLanguage.GetTranslation(x),  # noqa: F405
            # MacedonianLanguage.Culture: lambda x: MacedonianLanguage.GetTranslation(x),  # noqa: F405
            # NorwegianBokmalLanguage.Culture: lambda x: NorwegianBokmalLanguage.GetTranslation(x),  # noqa: F405
            # PersianLanguage.Culture: lambda x: PersianLanguage.GetTranslation(x),  # noqa: F405
            # PolishLanguage.Culture: lambda x: PolishLanguage.GetTranslation(x),  # noqa: F405
            # PortugueseLanguage.Culture: lambda x: PortugueseLanguage.GetTranslation(x),  # noqa: F405
            # PortugueseBrazilLanguage.Culture: lambda x: PortugueseBrazilLanguage.GetTranslation(x),  # noqa: F405
            # RomanianLanguage.Culture: lambda x: RomanianLanguage.GetTranslation(x),  # noqa: F405
            # RussianLanguage.Culture: lambda x: RussianLanguage.GetTranslation(x),  # noqa: F405
            # SlovakLanguage.Culture: lambda x: SlovakLanguage.GetTranslation(x),  # noqa: F405
            # SlovenianLanguage.Culture: lambda x: SlovenianLanguage.GetTranslation(x),  # noqa: F405
            SpanishLanguage.Culture: lambda x: SpanishLanguage.GetTranslation(x),  # noqa: F405
            # SerbianLanguage.Culture: lambda x: SerbianLanguage.GetTranslation(x),  # noqa: F405
            # SwedishLanguage.Culture: lambda x: SwedishLanguage.GetTranslation(x),  # noqa: F405
            # ThaiLanguage.Culture: lambda x: ThaiLanguage.GetTranslation(x),  # noqa: F405
            # TurkishLanguage.Culture: lambda x: TurkishLanguage.GetTranslation(x),  # noqa: F405
            # UkrainianLanguage.Culture: lambda x: UkrainianLanguage.GetTranslation(x),  # noqa: F405
            # VietnameseLanguage.Culture: lambda x: VietnameseLanguage.GetTranslation(x),  # noqa: F405
            # WelshLanguage.Culture: lambda x: WelshLanguage.GetTranslation(x),  # noqa: F405
            # UzbekLatinLanguage.Culture: lambda x: UzbekLatinLanguage.GetTranslation(x),  # noqa: F405
            # UzbekCyrillicLanguage.Culture: lambda x: UzbekCyrillicLanguage.GetTranslation(x),  # noqa: F405
            # CatalanLanguage.Culture: lambda x: CatalanLanguage.GetTranslation(x),  # noqa: F405
            # TajikLanguage.Culture: lambda x: TajikLanguage.GetTranslation(x),  # noqa: F405
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
                    culture =CultureInfo.CurrentUICulture()
            
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
