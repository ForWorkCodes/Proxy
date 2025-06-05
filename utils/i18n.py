SUPPORTED_LANGUAGES = ["ru", "en"]
DEFAULT_LANGUAGE = "en"


def resolve_language(code: str | None) -> str:
    if code and code in SUPPORTED_LANGUAGES:
        return code
    return DEFAULT_LANGUAGE
