import json
import locale
import os

# Translation module for main

# Global dictionary with the translations
TRANSLATIONS = {}

# Supported languages
languages = ["en", "es", "ca", "va", "fr"] # Maybe in separate file?

# Get user language
def get_system_locale():
    try:
        system_locale = locale.getlocale()[0]
        if system_locale:
            return system_locale[:2]
    except: # Don't know how to fix
        pass
    return "en" # Fallback to english

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
        language = "es" # Fallback to english if file not found
        with open("translations/en.json", "r", encoding="utf-8") as f:
            TRANSLATIONS = json.load(f)

# Get translation
def t(key: str) -> str:
    return str(TRANSLATIONS.get(key, key)) # Fallback to the same key

# On start get the language and translations
load_translations()