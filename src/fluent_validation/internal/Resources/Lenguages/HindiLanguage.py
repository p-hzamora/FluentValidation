class HindiLanguage:
    Culture: str = "hi"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' मान्य ईमेल एड्रेस नहीं है।",
            "GreaterThanOrEqualValidator": "'{PropertyName}' '{ComparisonValue}' से अधिक या के उसके बराबर होनी चाहिए।",
            "GreaterThanValidator": "'{PropertyName}' '{ComparisonValue}' से अधिक होनी चाहिए।",
            "LengthValidator": "'{PropertyName}' {min_length} और {max_length} अक्षरों के बीच होना चाहिए। आपने {total_length} अक्षर दर्ज किए हैं।",
            "MinimumLengthValidator": "'{PropertyName}' {min_length} वर्णों से अधिक या उसके बराबर होना चाहिए। आपने {total_length} वर्णों को दर्ज किया है",
            "MaximumLengthValidator": "'{PropertyName}' {max_length} वर्णों से कम या उसके बराबर होना चाहिए। आपने {total_length} वर्णों को दर्ज किया है",
            "LessThanOrEqualValidator": "'{PropertyName}' '{ComparisonValue}' से कम या के उसके बराबर होनी चाहिए।",
            "LessThanValidator": "'{PropertyName}' '{ComparisonValue}' से कम होनी चाहिए।",
            "NotEmptyValidator": "'{PropertyName}' खाली नहीं होना चाहिए।",
            "NotEqualValidator": "'{PropertyName}' '{ComparisonValue}' से बराबर नहीं होना चाहिए।",
            "NotNullValidator": "'{PropertyName}' खाली नहीं होना चाहिए।",
            "PredicateValidator": "निर्दिष्ट स्थिति को '{PropertyName}' के लिए पूरा नहीं किया गया।",
            "AsyncPredicateValidator": "निर्दिष्ट स्थिति को '{PropertyName}' के लिए पूरा नहीं किया गया।",
            "RegularExpressionValidator": "'{PropertyName}' सही प्रारूप में नहीं है।",
            "EqualValidator": "'{PropertyName}' '{ComparisonValue}' से बराबर होना चाहिए।",
            "ExactLengthValidator": "'{PropertyName}' {max_length} अक्षरों के उसके बराबर होनी चाहिए। आपने {total_length} अक्षर दर्ज किए हैं।",
            "InclusiveBetweenValidator": "'{PropertyName}' {From} और {To} के बीच में होनी चाहिए।. आपने {PropertyValue} दर्ज किया है।",
            "ExclusiveBetweenValidator": "'{PropertyName}' {From} और {To} (अनन्य) के बीच में होनी चाहिए।. आपने {PropertyValue} दर्ज किया है।",
            "CreditCardValidator": "'{PropertyName}' मान्य क्रेडिट कार्ड नंबर नहीं है।",
            "ScalePrecisionValidator": "'{PropertyName}' कुल में {ExpectedPrecision} अंकों से अधिक नहीं हो सकता है, {ExpectedScale} दशमलव के के साथ।. {Digits} अंक और {ActualScale} दशमलव पाए गए है।",
            "EmptyValidator": "'{PropertyName}' खाली होना चाहिए।",
            "NullValidator": "'{PropertyName}' खाली होना चाहिए।",
            "EnumValidator": "'{PropertyName}' में कई मान हैं जिनमें '{PropertyValue}' शामिल नहीं है।",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' {min_length} और {max_length} अक्षरों के बीच होना चाहिए।",
            "MinimumLength_Simple": "'{PropertyName}' {min_length} वर्णों से अधिक या उसके बराबर होना चाहिए।",
            "MaximumLength_Simple": "'{PropertyName}' {max_length} वर्णों से कम या उसके बराबर होना चाहिए।",
            "ExactLength_Simple": "'{PropertyName}' {max_length} अक्षरों के उसके बराबर होनी चाहिए।",
            "InclusiveBetween_Simple": "'{PropertyName}' {From} और {To} के बीच में होनी चाहिए।",
        }
        return dicc.get(key, None)
