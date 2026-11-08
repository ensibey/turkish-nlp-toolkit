"""
address.py — Turkish Logistics Address Standardization & Component Parser.

Engineered from techniques developed for the TEKNOFEST Address Resolution
Hackathon (Ranked 27th / 255 nationwide - Top 11%). Standardizes noisy,
abbreviated Turkish delivery addresses into canonical forms and extracts
hierarchical entities (mahalle, cadde, sokak, bina no, kat, daire, il/ilce).
"""

from __future__ import annotations

import re
from typing import Dict, Optional


# Canonical Turkish address token expansions
_ADDRESS_PATTERNS = [
    (r"\bmah\.?(?=\s|$)", "mahallesi"),
    (r"\bmh\.?(?=\s|$)", "mahallesi"),
    (r"\bcad\.?(?=\s|$)", "caddesi"),
    (r"\bcd\.?(?=\s|$)", "caddesi"),
    (r"\bsok\.?(?=\s|$)", "sokak"),
    (r"\bsk\.?(?=\s|$)", "sokak"),
    (r"\bblv\.?(?=\s|$)", "bulvarı"),
    (r"\bbulv\.?(?=\s|$)", "bulvarı"),
    (r"\bapt\.?(?=\s|$)", "apartmanı"),
    (r"\bap\.?(?=\s|$)", "apartmanı"),
    (r"\bsit\.?(?=\s|$)", "sitesi"),
    (r"\bblk\.?(?=\s|$)", "blok"),
    (r"\bno\s*[:.\-]?\s*(\d+[a-zA-Z]?)", r"no:\1"),
    (r"\bk\s*[:.\-]\s*(\d+)", r"kat:\1"),
    (r"\bkat\s*[:.\-]?\s*(\d+)", r"kat:\1"),
    (r"\bd\s*[:.\-]\s*(\d+)", r"daire:\1"),
    (r"\bdaire\s*[:.\-]?\s*(\d+)", r"daire:\1"),
]

# Common ASCII-to-Turkish city/location restorations
_ASCII_LOCATION_MAP = {
    "istanbul": "istanbul",
    "uskudar": "üsküdar",
    "kadikoy": "kadıköy",
    "besiktas": "beşiktaş",
    "sisli": "şişli",
    "atasehir": "ataşehir",
    "umraniye": "ümraniye",
    "bagcilar": "bağcılar",
    "bakirkoy": "bakırköy",
    "beyoglu": "beyoğlu",
    "cankaya": "çankaya",
    "kecioren": "keçiören",
    "karsiyaka": "karşıyaka",
    "nilufer": "nilüfer",
    "osmangazi": "osmangazi",
    "sehitkamil": "şehitkamil",
    "cukurova": "çukurova",
    "ataturk": "atatürk",
    "cumhuriyet": "cumhuriyet",
    "inonu": "inönü",
    "fevzi cakmak": "fevzi çakmak",
}


def standardize_address(text: str) -> str:
    """
    Normalize a raw, noisy Turkish postal/logistics address into a clean,
    canonical representation suitable for BERT classification or geocoding.
    """
    if not text:
        return ""

    # Lowercase using Turkish İ/I rules
    s = text.replace("İ", "i").replace("I", "ı").lower()
    s = re.sub(r"[/\\,;]+", " ", s)

    # Restore common ASCII location names
    for ascii_form, tr_form in _ASCII_LOCATION_MAP.items():
        s = re.sub(rf"\b{re.escape(ascii_form)}\b", tr_form, s)

    # Apply canonical address abbreviations
    for pattern, repl in _ADDRESS_PATTERNS:
        s = re.sub(pattern, repl, s, flags=re.IGNORECASE)

    s = re.sub(r"\s+", " ", s).strip()
    return s


def parse_address_components(text: str) -> Dict[str, Optional[str]]:
    """
    Extract structured fields (mahalle, cadde, sokak, no, kat, daire)
    from a Turkish address string.
    """
    norm = standardize_address(text)
    components: Dict[str, Optional[str]] = {
        "normalized": norm,
        "mahalle": None,
        "cadde_bulvar": None,
        "sokak": None,
        "bina_no": None,
        "kat": None,
        "daire": None,
    }

    mah_match = re.search(r"([a-zçğıöşü0-9\s]+?)\s+mahallesi\b", norm)
    if mah_match:
        tokens = mah_match.group(1).strip().split()
        components["mahalle"] = " ".join(tokens[-2:]) if len(tokens) > 2 else mah_match.group(1).strip()

    cad_match = re.search(r"([a-zçğıöşü0-9]+(?:\s+[a-zçğıöşü0-9]+)?)\s+(?:caddesi|bulvarı)\b", norm)
    if cad_match:
        components["cadde_bulvar"] = cad_match.group(1).strip()

    sok_match = re.search(r"([a-zçğıöşü0-9]+)\s+sokak\b", norm)
    if sok_match:
        components["sokak"] = sok_match.group(1).strip()

    no_match = re.search(r"\bno:(\d+[a-z]?)\b", norm)
    if no_match:
        components["bina_no"] = no_match.group(1)

    kat_match = re.search(r"\bkat:(\d+)\b", norm)
    if kat_match:
        components["kat"] = kat_match.group(1)

    daire_match = re.search(r"\bdaire:(\d+)\b", norm)
    if daire_match:
        components["daire"] = daire_match.group(1)

    return components
