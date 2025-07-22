class JapaneseLanguage:
    Culture: str = "ja"

    @staticmethod
    def GetTranslation(key: str) -> str:
        dicc: dict[str, str] = {
            "EmailValidator": "'{PropertyName}' は有効なメールアドレスではありません。",
            "GreaterThanOrEqualValidator": "'{PropertyName}' は '{ComparisonValue} 以上でなければなりません'.",
            "GreaterThanValidator": "'{PropertyName}' は '{ComparisonValue}' よりも大きくなければなりません。",
            "LengthValidator": "'{PropertyName}' は {min_length} から {max_length} 文字の間で入力する必要があります。 {total_length} 文字入力されています。",
            "MinimumLengthValidator": "'{PropertyName}' は少なくとも {min_length} 文字を入力しなければなりません。 {total_length} 文字入力されています。",
            "MaximumLengthValidator": "'{PropertyName}' は {max_length} 文字以下でなければなりません。 {total_length}  文字入力されています。",
            "LessThanOrEqualValidator": "'{PropertyName}' は '{ComparisonValue}' 以下である必要があります。",
            "LessThanValidator": "'{PropertyName}' は '{ComparisonValue}' 未満である必要があります。",
            "NotEmptyValidator": "'{PropertyName}' は空であってはなりません。",
            "NotEqualValidator": "'{PropertyName}' は '{ComparisonValue}' と等しくなってはなりません。",
            "NotNullValidator": "'{PropertyName}' は空であってはなりません。",
            "PredicateValidator": "'{PropertyName}' は指定された条件が満たされませんでした。",
            "AsyncPredicateValidator": "'{PropertyName}' は指定された条件が満たされませんでした。",
            "RegularExpressionValidator": "'{PropertyName}' は正しい形式ではありません。",
            "EqualValidator": "'{PropertyName}' は '{ComparisonValue}' と等しくなくてはなりません。",
            "ExactLengthValidator": "'{PropertyName}' は {max_length} 文字でなくてはなりません。 {total_length} 文字入力されています。",
            "InclusiveBetweenValidator": "'{PropertyName}' は {From} から {To} までの間でなければなりません。 {PropertyValue} と入力されています。",
            "ExclusiveBetweenValidator": "'{PropertyName}' は {From} と {To} の間でなければなりません。 {PropertyValue} と入力されています。",
            "CreditCardValidator": "'{PropertyName}' は有効なクレジットカード番号ではありません。",
            "ScalePrecisionValidator": "'{PropertyName}' は合計で {ExpectedPrecision} 桁、小数点以下は{ExpectedScale} 桁を超えてはなりません。 {Digits} 桁、小数点以下は{ActualScale} で入力されています。",
            "EmptyValidator": "'{PropertyName}' は空でなければなりません。",
            "NullValidator": "'{PropertyName}' は空でなければなりません。",
            "EnumValidator": "'{PropertyName}' の範囲に '{PropertyValue}' は含まれていません。",
            # Additional fallback messages used by clientside validation integration.
            "Length_Simple": "'{PropertyName}' は {min_length} から {max_length} 文字の間で入力する必要があります。",
            "MinimumLength_Simple": "'{PropertyName}' は少なくとも {min_length} 文字を入力しなければなりません。",
            "MaximumLength_Simple": "'{PropertyName}' は {max_length} 文字以下でなければなりません。",
            "ExactLength_Simple": "'{PropertyName}' は {max_length} 文字でなくてはなりません。",
            "InclusiveBetween_Simple": "'{PropertyName}' は {From} から {To} までの間でなければなりません。",
        }
        return dicc.get(key, None)