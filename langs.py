import json
import locale
import os

# Translation module for main

# Global dictionary with the translations
TRANSLATIONS = {}

# Supported languages
languages = ["en", "es", "ca", "va", "fr", "pr", "it", "de", "ja", "zh"] # Maybe in separate file?

# Default to english
language = "en"

# Get user language
def get_system_locale() -> str:
    try:
        system_locale = locale.getlocale()[0]
        if not system_locale:
            system_locale = locale.getdefaultlocale()[0]  # e.g. "es_ES"
        if system_locale:
            code = system_locale[:2].lower()
            if code in languages:
                return code
    except (ValueError, locale.Error):
        pass
    return "en"

# Change language and reload translations
def change_locale(new_locale: str):
    global language, TRANSLATIONS, languages

    if new_locale in languages:
        language = new_locale
        load_translations()
        return True
    return False

# Load the translations from json file
def load_translations():
    global TRANSLATIONS, language

    file_path = os.path.join("translations", f"{language}.json")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            TRANSLATIONS = json.load(f)
    except FileNotFoundError:
        print(f"File {language}.json not found")
        language = "en" # Fallback to english if file not found
        with open("translations/en.json", "r", encoding="utf-8") as f:
            TRANSLATIONS = json.load(f)

# Get translation
def t(key: str) -> str:
    """

    :rtype: str
    """
    return str(TRANSLATIONS.get(key, key)) # Fallback to the same key

# On start get the language and translations
load_translations()