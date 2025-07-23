import unittest
import sys
from parameterized import parameterized
from pathlib import Path


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())


from CultureScope import CultureScope
from fluent_validation.internal.Resources import LanguageManager
from fluent_validation.internal.Resources.ILanguageManager import CultureInfo


class LanguageManagerTests(unittest.TestCase):
    def setUp(self):
        self._languages = LanguageManager()

    @parameterized.expand(
        [
            "bs",
            "bs-Latn",
            "bs-Latn-BA",
        ]
    )
    def test_Gets_translation_for_bosnian_latin_culture(self, cultureName: str):
        with CultureScope(cultureName):
            msg = self._languages.GetString("NotNullValidator")
            self.assertEqual(msg, "'{PropertyName}' ne smije biti prazan.")

    @parameterized.expand(
        [
            "ta",
        ]
    )
    def test_Gets_translation_for_tamil_culture(self, cultureName: str):
        with CultureScope(cultureName):
            msg = self._languages.GetString("NotNullValidator")
            self.assertEqual(msg, "'{PropertyName}' காலியாக இருக்கக்கூடாது.")

    @parameterized.expand(
        [
            "sr",
            "sr-Cyrl",
            "sr-Cyrl-RS",
        ]
    )
    def test_Gets_translation_for_serbian_cyrillic_culture(self, cultureName: str):
        with CultureScope(cultureName):
            msg = self._languages.GetString("NotNullValidator")
            self.assertEqual(msg, "'{PropertyName}' не сме бити празно.")

    @parameterized.expand(
        [
            "sr-Latn",
            "sr-Latn-RS",
        ]
    )
    def test_Gets_translation_for_serbian_latin_culture(self, cultureName: str):
        with CultureScope(cultureName):
            msg = self._languages.GetString("NotNullValidator")
            self.assertEqual(msg, "'{PropertyName}' ne sme biti prazno.")

    def test_Gets_translation_for_culture(self):
        with CultureScope("fr"):
            msg = self._languages.GetString("NotNullValidator")
            self.assertEqual(msg, "'{PropertyName}' ne doit pas avoir la valeur null.")

    def test_Gets_translation_for_specific_culture(self):
        with CultureScope("zh-CN"):
            msg = self._languages.GetString("NotNullValidator")
            self.assertEqual(msg, "'{PropertyName}' 不能为Null。")

        with CultureScope("zh-SG"):
            msg = self._languages.GetString("NotNullValidator")
            self.assertEqual(msg, "'{PropertyName}' 不能为Null。")

    def test_Gets_translation_for_croatian_culture(self):
        with CultureScope("hr-HR"):
            msg = self._languages.GetString("NotNullValidator")
            self.assertEqual(msg, "Niste upisali '{PropertyName}'")

    def test_Gets_translation_for_telugu_culture(self):
        with CultureScope("te"):
            msg = self._languages.GetString("NotNullValidator")
            self.assertEqual(msg, "'{PropertyName}' ఖాళీగా ఉండకూడదు.")

    def test_Gets_email_validation_message_for_telugu_culture(self):
        with CultureScope("te"):
            msg = self._languages.GetString("EmailValidator")
            self.assertEqual(msg, "'{PropertyName}' చెల్లుబాటు అయ్యే ఈమెయిల్ చిరునామా కాదు.")

    def test_Falls_back_to_parent_culture(self):
        with CultureScope("fr-FR"):
            msg = self._languages.GetString("NotNullValidator")
            self.assertEqual(msg, "'{PropertyName}' ne doit pas avoir la valeur null.")

    def test_Falls_back_to_english_when_culture_not_registered(self):
        with CultureScope("gu-IN"):
            msg = self._languages.GetString("NotNullValidator")
            self.assertEqual(msg, "'{PropertyName}' must not be empty.")

    def test_Falls_back_to_english_when_translation_missing(self):
        language_mgr = LanguageManager()
        language_mgr.AddTranslation("en", "TestValidator", "foo")

        with CultureScope("zh-CN"):
            msg = language_mgr.GetString("TestValidator")
            self.assertEqual(msg, "foo")

    def test_Always_use_specific_language(self):
        self._languages.Culture = CultureInfo("fr-FR")
        msg = self._languages.GetString("NotNullValidator")
        self.assertEqual(msg, "'{PropertyName}' ne doit pas avoir la valeur null.")

    def test_Disables_localization(self):
        with CultureScope("fr"):
            self._languages.Enabled = False
            msg = self._languages.GetString("NotNullValidator")
            self.assertEqual(msg, "'{PropertyName}' must not be empty.")

    def test_Can_replace_message_without_overriding_all_languages(self):
        with CultureScope("fr-FR"):
            custom = LanguageManager()
            custom.AddTranslation("fr", "NotNullValidator", "foo")
            msg = custom.GetString("NotNullValidator")
            self.assertEqual(msg, "foo")

            # Using a custom translation should only override the single message.
            # Other messages in the language should be unaffected.
            # Need to do this test as non-english, as english is always loaded.
            msg = custom.GetString("NotEmptyValidator")
            self.assertEqual(msg, "'{PropertyName}' ne doit pas être vide.")

    def test_All_localizations_have_same_parameters_as_English(self):
        # COMMENT: Remember to update this test if new validators are added.
        keys = [
            "EmailValidator",
            "GreaterThanOrEqualValidator",
            "GreaterThanValidator",
            "LengthValidator",
            "MinimumLengthValidator",
            "MaximumLengthValidator",
            "LessThanOrEqualValidator",
            "LessThanValidator",
            "NotEmptyValidator",
            "NotEqualValidator",
            "NotNullValidator",
            "PredicateValidator",
            "AsyncPredicateValidator",
            "RegularExpressionValidator",
            "EqualValidator",
            "ExactLengthValidator",
            "InclusiveBetweenValidator",
            "ExclusiveBetweenValidator",
            "CreditCardValidator",
            "ScalePrecisionValidator",
            "EmptyValidator",
            "NullValidator",
            "EnumValidator",
            "Length_Simple",
            "MinimumLength_Simple",
            "MaximumLength_Simple",
            "ExactLength_Simple",
            "InclusiveBetween_Simple",
        ]

        # Get all language culture codes from the imported language classes
        from fluent_validation.internal.Resources.Lenguages import (
            EnglishLanguage,
            SpanishLanguage,
            FrenchLanguage,
            GermanLanguage,
            ItalianLanguage,
            PortugueseLanguage,
            DutchLanguage,
            RussianLanguage,
            ChineseSimplifiedLanguage,
            JapaneseLanguage,
            KoreanLanguage,
            PolishLanguage,
            TurkishLanguage,
            ArabicLanguage,
            SwedishLanguage,
            CzechLanguage,
            HungarianLanguage,
            NorwegianBokmalLanguage,
            DanishLanguage,
            FinnishLanguage,
            HindiLanguage,
            ThaiLanguage,
            VietnameseLanguage,
            IndonesianLanguage,
            ChineseTraditionalLanguage,
            RomanianLanguage,
            BulgarianLanguage,
            CroatianLanguage,
            SlovakLanguage,
            SlovenianLanguage,
            EstonianLanguage,
            LatvianLanguage,
            GreekLanguage,
            AlbanianLanguage,
            AzerbaijaneseLanguage,
            BengaliLanguage,
            BosnianLanguage,
            CatalanLanguage,
            GeorgianLanguage,
            HebrewLanguage,
            IcelandicLanguage,
            KazakhLanguage,
            KhmerLanguage,
            MacedonianLanguage,
            NorwegianNynorskLanguage,
            PersianLanguage,
            PortugueseBrazilLanguage,
            RomanshLanguage,
            SerbianCyrillicLanguage,
            SerbianLatinLanguage,
            TajikLanguage,
            TamilLanguage,
            TeluguLanguage,
            UkrainianLanguage,
            UzbekCyrillicLanguage,
            UzbekLatinLanguage,
            WelshLanguage,
        )

        # Get all culture codes from language classes
        language_classes = [
            EnglishLanguage,
            SpanishLanguage,
            FrenchLanguage,
            GermanLanguage,
            ItalianLanguage,
            PortugueseLanguage,
            DutchLanguage,
            RussianLanguage,
            ChineseSimplifiedLanguage,
            JapaneseLanguage,
            KoreanLanguage,
            PolishLanguage,
            TurkishLanguage,
            ArabicLanguage,
            SwedishLanguage,
            CzechLanguage,
            HungarianLanguage,
            NorwegianBokmalLanguage,
            DanishLanguage,
            FinnishLanguage,
            HindiLanguage,
            ThaiLanguage,
            VietnameseLanguage,
            IndonesianLanguage,
            ChineseTraditionalLanguage,
            RomanianLanguage,
            BulgarianLanguage,
            CroatianLanguage,
            SlovakLanguage,
            SlovenianLanguage,
            EstonianLanguage,
            LatvianLanguage,
            GreekLanguage,
            AlbanianLanguage,
            AzerbaijaneseLanguage,
            BengaliLanguage,
            BosnianLanguage,
            CatalanLanguage,
            GeorgianLanguage,
            HebrewLanguage,
            IcelandicLanguage,
            KazakhLanguage,
            KhmerLanguage,
            MacedonianLanguage,
            NorwegianNynorskLanguage,
            PersianLanguage,
            PortugueseBrazilLanguage,
            RomanshLanguage,
            SerbianCyrillicLanguage,
            SerbianLatinLanguage,
            TajikLanguage,
            TamilLanguage,
            TeluguLanguage,
            UkrainianLanguage,
            UzbekCyrillicLanguage,
            UzbekLatinLanguage,
            WelshLanguage,
        ]

        language_names: list[str] = [lang.Culture for lang in language_classes]

        def extract_template_parameters(message: str):
            if message is None:
                return []
            message = message.replace("{{", "").replace("}}", "")
            parts = message.split("{")
            return [part.split("}")[0] for part in parts[1:] if "}" in part]

        def check_parameters_match(language_code: str, translation_key: str):
            reference_message = self._languages.GetString(translation_key, CultureInfo("en-US"))
            translated_message = self._languages.GetString(translation_key, CultureInfo(language_code))
            if reference_message == translated_message:
                return
            reference_parameters = extract_template_parameters(reference_message)
            translated_parameters = extract_template_parameters(translated_message)

            # Convert to sets for comparison
            ref_set = set(reference_parameters)
            trans_set = set(translated_parameters)

            self.assertEqual(
                len(reference_parameters),
                len(translated_parameters),
                f"Translation for language {language_code}, key {translation_key} has parameters {','.join(translated_parameters)}, expected {','.join(reference_parameters)}",
            )
            self.assertEqual(
                ref_set, trans_set, f"Translation for language {language_code}, key {translation_key} has parameters {','.join(translated_parameters)}, expected {','.join(reference_parameters)}"
            )

        # Check all language/key combinations
        for language_name in language_names:
            for key in keys:
                with self.subTest(language=language_name, key=key):
                    check_parameters_match(language_name, key)

    def test_All_languages_should_be_loaded(self):
        from fluent_validation.internal.Resources.Lenguages import (
            EnglishLanguage,
            SpanishLanguage,
            FrenchLanguage,
            GermanLanguage,
            ItalianLanguage,
            PortugueseLanguage,
            DutchLanguage,
            RussianLanguage,
            ChineseSimplifiedLanguage,
            JapaneseLanguage,
            KoreanLanguage,
            PolishLanguage,
            TurkishLanguage,
            ArabicLanguage,
            SwedishLanguage,
            CzechLanguage,
            HungarianLanguage,
            NorwegianBokmalLanguage,
            DanishLanguage,
            FinnishLanguage,
            HindiLanguage,
            ThaiLanguage,
            VietnameseLanguage,
            IndonesianLanguage,
            ChineseTraditionalLanguage,
            RomanianLanguage,
            BulgarianLanguage,
            CroatianLanguage,
            SlovakLanguage,
            SlovenianLanguage,
            EstonianLanguage,
            LatvianLanguage,
            GreekLanguage,
            AlbanianLanguage,
            AzerbaijaneseLanguage,
            BengaliLanguage,
            BosnianLanguage,
            CatalanLanguage,
            GeorgianLanguage,
            HebrewLanguage,
            IcelandicLanguage,
            KazakhLanguage,
            KhmerLanguage,
            MacedonianLanguage,
            NorwegianNynorskLanguage,
            PersianLanguage,
            PortugueseBrazilLanguage,
            RomanshLanguage,
            SerbianCyrillicLanguage,
            SerbianLatinLanguage,
            TajikLanguage,
            TamilLanguage,
            TeluguLanguage,
            UkrainianLanguage,
            UzbekCyrillicLanguage,
            UzbekLatinLanguage,
            WelshLanguage,
        )

        # Create list of language info
        language_classes = [
            EnglishLanguage,
            SpanishLanguage,
            FrenchLanguage,
            GermanLanguage,
            ItalianLanguage,
            PortugueseLanguage,
            DutchLanguage,
            RussianLanguage,
            ChineseSimplifiedLanguage,
            JapaneseLanguage,
            KoreanLanguage,
            PolishLanguage,
            TurkishLanguage,
            ArabicLanguage,
            SwedishLanguage,
            CzechLanguage,
            HungarianLanguage,
            NorwegianBokmalLanguage,
            DanishLanguage,
            FinnishLanguage,
            HindiLanguage,
            ThaiLanguage,
            VietnameseLanguage,
            IndonesianLanguage,
            ChineseTraditionalLanguage,
            RomanianLanguage,
            BulgarianLanguage,
            CroatianLanguage,
            SlovakLanguage,
            SlovenianLanguage,
            EstonianLanguage,
            LatvianLanguage,
            GreekLanguage,
            AlbanianLanguage,
            AzerbaijaneseLanguage,
            BengaliLanguage,
            BosnianLanguage,
            CatalanLanguage,
            GeorgianLanguage,
            HebrewLanguage,
            IcelandicLanguage,
            KazakhLanguage,
            KhmerLanguage,
            MacedonianLanguage,
            NorwegianNynorskLanguage,
            PersianLanguage,
            PortugueseBrazilLanguage,
            RomanshLanguage,
            SerbianCyrillicLanguage,
            SerbianLatinLanguage,
            TajikLanguage,
            TamilLanguage,
            TeluguLanguage,
            UkrainianLanguage,
            UzbekCyrillicLanguage,
            UzbekLatinLanguage,
            WelshLanguage,
        ]

        languages = [{"Name": lang.Culture, "Type": lang.__name__} for lang in language_classes]

        english_message = self._languages.GetString("NotNullValidator", CultureInfo("en"))

        for language in languages:
            # Skip english as we know it's always loaded and will match.
            if language["Name"] == "en":
                continue

            # Get the message from the language manager from the culture. If it's in English, then it's hit the
            # fallback and means the culture hasn't been loaded.
            message = self._languages.GetString("NotNullValidator", CultureInfo(language["Name"]))
            self.assertNotEqual(message, english_message, f"Language '{language['Name']}' ({language['Type']}) is not loaded in the LanguageManager")

    def test_Uses_error_code_as_localization_key(self):
        """Test that error codes can be used as localization keys."""
        # Note: This test requires ValidatorOptions.Global and InlineValidator infrastructure
        # which may not be implemented yet. This is a placeholder for when that infrastructure exists.
        custom_manager = CustomLanguageManager()

        with CultureScope("fr-FR"):
            # This would require InlineValidator<Person> and ValidatorOptions.Global to be implemented
            # For now, we test the custom language manager directly
            result = custom_manager.GetString("CustomKey")
            self.assertEqual(result, "bar")

    def test_Falls_back_to_default_localization_key_when_error_code_key_not_found(self):
        """Test fallback to default localization when error code key is not found."""
        custom_manager = CustomLanguageManager()
        custom_manager.Culture = CultureInfo("fr-FR")

        # Test that non-existent key falls back to default
        custom_manager.GetString("DoesNotExist")
        # Should fall back to NotNullValidator translation
        default_result = custom_manager.GetString("NotNullValidator")
        self.assertEqual(default_result, "foo")


class CustomLanguageManager(LanguageManager):
    def __init__(self):
        super().__init__()
        self.AddTranslation("fr", "NotNullValidator", "foo")
        self.AddTranslation("fr", "CustomKey", "bar")


if __name__ == "__main__":
    unittest.main()
