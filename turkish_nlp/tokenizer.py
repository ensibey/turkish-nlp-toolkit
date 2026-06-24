"""Turkish tokenizer — sentence splitting and word tokenization."""
import re
from . import abbreviations as _abbrev

_SENT_SPLIT = re.compile(r"(?<!\w\.\w.)(?<![A-Z\u00c7\u011e\u0130\u00d6\u015e\u00dc][a-z\u00e7\u011f\u0131\u00f6\u015f\u00fc]\.)(?<=\.|\!|\?)\s")
_WORD_SPLIT = re.compile(r"[\s]+")
_PUNCT_STRIP = re.compile(r"^[^\w\u00c7\u011e\u0130\u00d6\u015e\u00dc\u00e7\u011f\u0131\u00f6\u015f\u00fc\']+|[^\w\u00c7\u011e\u0130\u00d6\u015e\u00dc\u00e7\u011f\u0131\u00f6\u015f\u00fc\']+$")

def sent_tokenize(text):
    """
    Split text into sentences with Turkish abbreviation awareness.
    Handles Dr., Prof., Mah., Cad. etc. without false splits.
    """
    placeholder = "##A##"
    masked = text
    for abbrev in sorted(_abbrev.ABBREVIATIONS.keys(), key=len, reverse=True):
        if abbrev.endswith("."):
            masked = re.sub(r"(?<!\w)" + re.escape(abbrev),
                           abbrev[:-1] + placeholder, masked, flags=re.IGNORECASE)
    sentences = _SENT_SPLIT.split(masked)
    return [s.replace(placeholder, ".").strip() for s in sentences if s.strip()]

def word_tokenize(text, keep_apostrophe_suffixes=True):
    """
    Tokenize text into words, preserving Turkish apostrophe suffixes.
    Example: "Istanbul'da" stays as one token (not split at apostrophe).
    """
    tokens = _WORD_SPLIT.split(text)
    result = []
    for tok in tokens:
        tok = _PUNCT_STRIP.sub("", tok)
        if not tok: continue
        if not keep_apostrophe_suffixes and "'" in tok:
            result.extend(p for p in tok.split("'") if p)
        else:
            result.append(tok)
    return result

def char_tokenize(text): return list(text)

def ngrams(tokens, n):
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]
