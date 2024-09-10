from typing import Optional, override

from .ILanguageManager import ILanguageManager, CultureInfo
from .Lenguages import *  # noqa: F403


class LanguageManager(ILanguageManager):
    # readonly ConcurrentDictionary<string, string> _languages = new ConcurrentDictionary<string, string>();
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
    def Enabled(self) -> bool:
        return True

    @property
    @override
    def Culture(self) -> CultureInfo:
        if not CultureInfo.CurrentUICulture:
            return CultureInfo().CurrentUICulture
        return CultureInfo.CurrentUICulture

    @override
    def GetString(self, key: str, culture: CultureInfo = None) -> Optional[str]:
        if culture is None:
            self.Culture
        return self.GetTranslation(self.Culture, key)
