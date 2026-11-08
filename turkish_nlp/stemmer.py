"""
stemmer.py — Lightweight Rule-Based Agglutinative Turkish Stemmer.

Handles high-frequency nominal, plural, case, possessive, and derivational
suffixes while respecting Turkish vowel harmony and consonant softening
(p->b, ç->c, t->d, k->ğ).
"""

from __future__ import annotations

from typing import List, Union

# Ordered longest-first so compound suffixes strip cleanly in sequence
_INFLECTIONAL_SUFFIXES = [
    "larından", "lerinden", "larımız", "lerimiz", "larınız", "leriniz",
    "larında", "lerinde", "larına", "lerine", "larını", "lerini",
    "lardan", "lerden", "운",
    "dan", "den", "tan", "ten",
    "nda", "nde", "da", "de", "ta", "te",
    "nın", "nin", "nun", "nün", "ın", "in", "un", "ün",
    "lar", "ler",
    "yla", "yle", "la", "le",
    "lık", "lik", "luk", "lük",
    "sız", "siz", "suz", "süz",
    "cı", "ci", "cu", "cü", "çı", "çi", "çu", "çü",
    "ım", "im", "um", "üm",
    "ya", "ye", "na", "ne",
]

_SOFTENED_CONSONANTS = {
    "b": "p",
    "c": "ç",
    "d": "t",
    "ğ": "k",
}

# Common words that end with suffix-like characters but are roots themselves
_PROTECTED_ROOTS = {
    "elma", "araba", "masa", "kedi", "köpek", "deniz", "kalem", "kitap",
    "okul", "istanbul", "ankara", "izmir", "insan", "zaman", "dünya",
}


def stem_word(word: str, min_root_len: int = 3) -> str:
    """
    Strip Turkish inflectional/derivational suffixes from a single token
    and restore terminal consonant devoicing (e.g., 'kitabın' -> 'kitap').
    """
    w = word.strip()
    if len(w) <= min_root_len or w in _PROTECTED_ROOTS:
        return w

    # Strip apostrophe suffixes directly (e.g., "İstanbul'da" -> "İstanbul")
    if "'" in w or "’" in w:
        parts = w.replace("’", "'").split("'")
        if len(parts[0]) >= 2:
            return parts[0]

    current = w
    changed = True
    max_passes = 3
    passes = 0

    while changed and passes < max_passes:
        changed = False
        passes += 1
        for suf in _INFLECTIONAL_SUFFIXES:
            if current.endswith(suf) and (len(current) - len(suf)) >= min_root_len:
                current = current[: -len(suf)]
                changed = True
                if current in _PROTECTED_ROOTS:
                    changed = False
                break

    # Restore softened final consonant for common roots (e.g., kitab -> kitap, ağac -> ağaç)
    if len(current) >= min_root_len and current[-1] in _SOFTENED_CONSONANTS:
        candidate = current[:-1] + _SOFTENED_CONSONANTS[current[-1]]
        if candidate in _PROTECTED_ROOTS or current.endswith(("kitab", "ağac", "renğ", "sokag", "yemeğ")):
            current = candidate

    return current


def stem(tokens: Union[str, List[str]]) -> Union[str, List[str]]:
    """Stem either a single word string or a list of tokens."""
    if isinstance(tokens, str):
        return stem_word(tokens)
    return [stem_word(t) for t in tokens]
