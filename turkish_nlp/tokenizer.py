"""Sentence and word tokenization with Turkish abbreviation and apostrophe rules."""
from __future__ import annotations

import re
from typing import List, Sequence, Tuple

from . import abbreviations as _abbrev

_SENT_SPLIT = re.compile(
    r"(?<!\w\.\w.)(?<![A-Z\u00c7\u011e\u0130\u00d6\u015e\u00dc][a-z\u00e7\u011f\u0131\u00f6\u015f\u00fc]\.)(?<=\.|\!|\?)\s"
)
_WORD_SPLIT = re.compile(r"[\s]+")
_PUNCT_STRIP = re.compile(
    r"^[^\w\u00c7\u011e\u0130\u00d6\u015e\u00dc\u00e7\u011f\u0131\u00f6\u015f\u00fc']+|"
    r"[^\w\u00c7\u011e\u0130\u00d6\u015e\u00dc\u00e7\u011f\u0131\u00f6\u015f\u00fc']+$"
)


def sent_tokenize(text: str) -> List[str]:
    """Split text into sentences without breaking on known Turkish abbreviations."""
    placeholder = "\x00DOT\x00"
    masked = text
    for abbrev in sorted(_abbrev.ABBREVIATIONS.keys(), key=len, reverse=True):
        if abbrev.endswith("."):
            masked = re.sub(
                r"(?<!\w)" + re.escape(abbrev),
                abbrev[:-1] + placeholder,
                masked,
                flags=re.IGNORECASE,
            )
    sentences = _SENT_SPLIT.split(masked)
    return [s.replace(placeholder, ".").strip() for s in sentences if s.strip()]


def word_tokenize(text: str, keep_apostrophe_suffixes: bool = True) -> List[str]:
    """Tokenize text into words, optionally keeping apostrophe-separated case suffixes attached."""
    tokens = _WORD_SPLIT.split(text)
    result: List[str] = []
    for tok in tokens:
        tok = _PUNCT_STRIP.sub("", tok)
        if not tok:
            continue
        if not keep_apostrophe_suffixes and "'" in tok:
            result.extend(part for part in tok.split("'") if part)
        else:
            result.append(tok)
    return result


def char_tokenize(text: str) -> List[str]:
    """Return list of characters in text."""
    return list(text)


def ngrams(tokens: Sequence[str], n: int) -> List[Tuple[str, ...]]:
    """Generate contiguous n-gram tuples from a token sequence."""
    if n <= 0 or len(tokens) < n:
        return []
    return [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]
