"""Support for i18n internationalization, using text_explainability to globally set the languages.

Todo:
- Add ability to extend text_explainability vocab per language
"""

from text_explainability.internationalization import translate_string, translate_list, set_locale, get_locale

__all__ = [translate_string, translate_list, set_locale, get_locale]
