# Localization

Out of the box, FluentValidation provides translations for the default validation messages in several languages. By default, the language specified in the .NET's framework's current UI culture will be used (`CultureInfo.CurrentUICulture`) when translating messages.

You can also use the `with_message` and `WithLocalizedMessage` methods to specify a localized error message for a single validation rule.

### with_message
If you are using Visual Studio's built in support for `.resx` files and their strongly-typed wrappers, then you can localize a message by calling the overload of `with_message` that accepts a lambda expression:

```
rule_for(x => x.Surname).not_null().with_message(x => MyLocalizedMessages.SurnameRequired)
```
You could also use the same approach if you need to obtain the localized message from another source (such as a database) by obtaining the string from within the lambda.

<!-- ### IStringLocalizer

The above 2 examples assume you're using a strongly-typed wrapper around a resource file, where each static property on the class corresponds to a key within the resource file. This is the "old" way of working with resources prior to ASP.NET Core, but is not relevant if you're using ASP.NET Core's `IStringLocalizer`.

If you are using `IStringLocalizer` to handle localization then all you need to do is inject your localizer into your validator, and use it within a `with_message` callback, for example:

```python
public class PersonValidator : AbstractValidator<Person> 
{
  public PersonValidator(IStringLocalizer<Person> localizer)
   {
    rule_for(x => x.Surname).not_null().with_message(x => localizer["Surname is required"])
  }
}
``` -->

### Default Messages
If you want to replace all (or some) of FluentValidation's default messages then you can do this by implementing a custom version of the `ILanguageManager` interface.

For example, the default message for the `not_null` validator is `'{PropertyName}' must not be empty.`. If you wanted to replace this message for all uses of the `not_null` validator in your application, you could write a custom Language Manager:

```python
public class CustomLanguageManager : FluentValidation.Resources.LanguageManager
{
  public CustomLanguageManager() 
  {
    AddTranslation("en", "NotNullValidator", "'{PropertyName}' is required.")
    AddTranslation("en-US", "NotNullValidator", "'{PropertyName}' is required.")
    AddTranslation("en-GB", "NotNullValidator", "'{PropertyName}' is required.")
  }
}
```

Here we have a custom class that inherits from the base `LanguageManager`. In its constructor we call the `AddTranslation` method passing in the language we're using, the name of the validator we want to override, and the new message.

Once this is done, we can replace the default LanguageManager by setting the LanguageManager property in the static `ValidatorOptions` class during your application's startup routine:

```python
ValidatorOptions.Global.LanguageManager = CustomLanguageManager()
```

Note that if you replace messages in the `en` culture, you should consider also replacing the messages for `en-US` and `en-GB` too, as these will take precedence for users from these locales.

This is a simple example that only replaces one validator's message in English only, but could be extended to replace the messages for all languages. Instead of inheriting from the default LanguageManager, you could also implement the `ILanguageManager` interface directly if you want to load the messages from a completely different location other than the FluentValidation default (for example, if you wanted to store FluentValidation's default messages in a database).

Of course, if all you want to do is replace this message for a single use of a validator, then you could just use `with_message("'{PropertyName}' is required")`

### Contributing Languages
If you'd like to contribute a translation of FluentValidation's default messages, please open a pull request that adds a language file to the project. The current language files are [located in the GitHub repository](https://github.com/JeremySkinner/FluentValidation/tree/master/src/FluentValidation/Resources/Languages). Additionally you'll need to [add the new language to the default LanguageManager](https://github.com/p-hzamora/FluentValidation/blob/main/src/FluentValidation/Resources/LanguageManager.cs#L38) 

[The default English messages are stored here](https://github.com/JeremySkinner/FluentValidation/blob/master/src/FluentValidation/Resources/Languages/EnglishLanguage.cs)

### Disabling Localization
You can completely disable FluentValidation's support for localization, which will force the default English messages to be used, regardless of the thread's `CurrentUICulture`. This can be done in your application's startup routine by calling into the static `ValidatorOptions` class:

```python
ValidatorOptions.Global.LanguageManager.Enabled = False
```
You can also force the default messages to always be displayed in a specific language:

```python
ValidatorOptions.Global.LanguageManager.Culture = CultureInfo("fr")
```
