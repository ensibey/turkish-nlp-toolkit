"""
Abbreviation- and ordinal-aware Turkish sentence boundary splitter.

Avoids false splits on Turkish honorifics (Dr., Prof., Av.), address markers
(Mah., Sok., Cad., Apt., No.), ordinal numerals (1., 2., 19.), and common
abbreviations (vb., vs., bk., örn., M.Ö.).
"""

from __future__ import annotations

import re
from typing import List, Set

PROTECTED_ABBREVIATIONS: Set[str] = {
    "dr", "prof", "doç", "yrd", "av", "müh", "mim", "uzm", "alb", "yzb", "bnb",
    "mah", "sok", "sk", "cad", "cd", "bul", "blv", "apt", "no", "kat", "daire",
    "vb", "vs", "bk", "bkz", "örn", "ör", "yy", "sy", "sf", "s", "c", "m",
    "a.ş", "ltd", "şti", "tic", "san", "t.c", "m.ö", "m.s", "st",
}

BOUNDARY_RE = re.compile(r"([.!?]+)(\s+|$)")


def split_sentences(text: str) -> List[str]:
    """Split Turkish text into sentences without breaking on abbreviations or ordinals."""
    cleaned = re.sub(r"\s+", " ", (text or "").strip())
    if not cleaned:
        return []

    sentences: List[str] = []
    start = 0

    for match in BOUNDARY_RE.finditer(cleaned):
        punct = match.group(1)
        end_of_punct = match.end(1)
        end_of_match = match.end()

        if punct == ".":
            # Extract token immediately preceding the period
            prefix = cleaned[start : match.start()]
            token_match = re.search(r"([0-9a-zA-ZçğıöşüÇĞİÖŞÜ.]+)$", prefix)
            prev_token = token_match.group(1) if token_match else ""
            prev_lower = prev_token.replace("İ", "i").replace("I", "ı").lower()

            # Protect known abbreviations
            if prev_lower in PROTECTED_ABBREVIATIONS:
                continue

            # Protect Turkish ordinals (e.g. "1. sınıf", "19. yüzyıl", "3. Cadde")
            if prev_token.isdigit():
                following = cleaned[end_of_match : end_of_match + 20]
                if following and not following.startswith(("VE ",)):
                    # Ordinals are followed by a lowercase word or street/rank noun
                    if following[0].islower() or re.match(r"^(Cad|Sok|Mah|Kat|Sınıf|Yüzyıl)", following):
                        continue

            # Protect single-letter initials (e.g. "M. Kemal")
            if len(prev_token) == 1 and prev_token.isalpha():
                continue

        chunk = cleaned[start:end_of_punct].strip()
        if chunk:
            sentences.append(chunk)
        start = end_of_match

    tail = cleaned[start:].strip()
    if tail:
        sentences.append(tail)

    return sentences
