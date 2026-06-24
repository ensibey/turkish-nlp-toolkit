"""Turkish text normalizer with correct I/i mapping."""
import re, unicodedata

_TR_LOWER = str.maketrans("\u0130I\u011e\xdc\u015e\xd6\xc7", "i\u0131\u011f\xfc\u015f\xf6\xe7")
_CHAR_FIXES = {"\u2019":"'","\u201c":'"',"\u201d":'"',"\u2013":"-","\u2014":"-","\xa0":" ","\u200b":""}

def to_lower(text):
    """Correct Turkish lowercasing: I->i, i->i (not i\u0307)"""
    return text.translate(_TR_LOWER).lower()

def to_upper(text):
    return text.translate(str.maketrans("i\u0131\u011f\xfc\u015f\xf6\xe7","\u0130I\u011e\xdc\u015e\xd6\xc7")).upper()

def fix_chars(text):
    for bad, good in _CHAR_FIXES.items():
        text = text.replace(bad, good)
    return text

def fix_spaces(text):
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()

def normalize(text, lowercase=True, fix_encoding=True, unicode_form="NFC", collapse_spaces=True):
    """
    Full normalization pipeline for Turkish text.
    Correctly handles I->i (not i\u0307) unlike Python stdlib.
    """
    if fix_encoding: text = fix_chars(text)
    if unicode_form: text = unicodedata.normalize(unicode_form, text)
    if lowercase: text = to_lower(text)
    if collapse_spaces: text = fix_spaces(text)
    return text
