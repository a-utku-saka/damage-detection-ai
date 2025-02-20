LANGUAGE_CODES = {
    "en-us": "English",
    "tr-tr": "Turkish",
    "it-it": "Italian ",
    "fr-fr": "French",
    "es-es": "Spanish",
    "pt-pt": "Portuguese",
    "de-de": "German",
    "nl-nl": "Dutch"
    }

def _get_language_from_header(accept_language_header):
    """Returns language name from Accept-Language header."""
    # Lowercase and separate language codes
    accepted_languages = [lang.partition(';')[0].lower() for lang in accept_language_header.split(',')]

    # Loop until you find a suitable language in the LANGUAGE_CODES dictionary
    for lang_code in accepted_languages:
        if lang_code in LANGUAGE_CODES:
            return LANGUAGE_CODES[lang_code]

    # Select a default language if no suitable language is found
    return "Turkish"  # Default language can be set here