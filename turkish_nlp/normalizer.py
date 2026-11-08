"""Turkish text normalizer with locale-aware I/i case folding."""
from __future__ import annotations

import re
import unicodedata

_TR_LOWER = str.maketrans(
    "\u0130I\u011e\xdc\u015e\xd6\xc7",
    "i\u0131\u011f\xfc\u015f\xf6\xe7",
)
_TR_UPPER = str.maketrans(
    "i\u0131\u011f\xfc\u015f\xf6\xe7",
    "\u0130I\u011e\xdc\u015e\xd6\xc7",
)
_CHAR_FIXES = {
    "\u2019": "'",
    "\u2018": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u2013": "-",
    "\u2014": "-",
    "\xa0": " ",
    "\u200b": "",
}


def to_lower(text: str) -> str:
    """Lowercase string using Turkish dotted/dotless I rules (İ -> i, I -> ı)."""
    return text.translate(_TR_LOWER).lower()


def to_upper(text: str) -> str:
    """Uppercase string using Turkish dotted/dotless I rules (i -> İ, ı -> I)."""
    return text.translate(_TR_UPPER).upper()


def fix_chars(text: str) -> str:
    """Replace typographic quotes, dashes, and zero-width spaces with ASCII equivalents."""
    for bad, good in _CHAR_FIXES.items():
        text = text.replace(bad, good)
    return text


def fix_spaces(text: str) -> str:
    """Collapse consecutive horizontal whitespace and excessive blank lines."""
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def normalize(
    text: str,
    lowercase: bool = True,
    fix_encoding: bool = True,
    unicode_form: str = "NFC",
    collapse_spaces: bool = True,
) -> str:
    """Run character normalization, Unicode NFC composition, and Turkish case folding."""
    if fix_encoding:
        text = fix_chars(text)
    if unicode_form:
        text = unicodedata.normalize(unicode_form, text)
    if lowercase:
        text = to_lower(text)
    if collapse_spaces:
        text = fix_spaces(text)
    return text
