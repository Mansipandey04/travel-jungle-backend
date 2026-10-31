import re
import unicodedata


_HTML_TAG = re.compile(r"<[^>]+>")
_SLUG_SAFE = re.compile(r"[^a-z0-9]+")


def strip_html(text: str) -> str:
    return _HTML_TAG.sub("", text)


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = value.lower().strip()
    value = _SLUG_SAFE.sub("-", value).strip("-")
    return value[:120] or "item"
