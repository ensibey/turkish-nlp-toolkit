"""
Zero-dependency Turkish structured entity extractor.

Extracts Turkish postal codes (01xxx–81xxx), TR phone numbers, TR IBANs,
checksum-verified 11-digit TCKN identifiers, emails, and TRY currency amounts.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List

EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
TR_IBAN_RE = re.compile(r"\bTR\d{2}(?:[\s-]?\d{4}){5}[\s-]?\d{2}\b", re.IGNORECASE)
TR_PHONE_RE = re.compile(
    r"(?<!\w)(?:\+90[\s.-]?|0)?(?:\(?5\d{2}\)?|\(?[234]\d{2}\)?)[\s.-]\d{3}[\s.-]?\d{2}[\s.-]?\d{2}(?!\w)"
)
POSTAL_CODE_RE = re.compile(r"\b((?:0[1-9]|[1-7]\d|8[01])\d{3})\b")
TCKN_RE = re.compile(r"\b[1-9]\d{10}\b")
CURRENCY_RE = re.compile(r"(?:₺\s?\d{1,3}(?:\.\d{3})*(?:,\d{1,2})?|\b\d{1,3}(?:\.\d{3})*(?:,\d{1,2})?\s?(?:TL|TRY|₺)\b)", re.IGNORECASE)


def validate_tckn(value: str) -> bool:
    if len(value) != 11 or not value.isdigit() or value[0] == "0":
        return False
    d = [int(c) for c in value]
    d10 = ((sum(d[0:9:2]) * 7) - sum(d[1:8:2])) % 10
    d11 = sum(d[:10]) % 10
    return d[9] == d10 and d[10] == d11


@dataclass
class TurkishEntities:
    emails: List[str] = field(default_factory=list)
    phones: List[str] = field(default_factory=list)
    ibans: List[str] = field(default_factory=list)
    postal_codes: List[str] = field(default_factory=list)
    tckns: List[str] = field(default_factory=list)
    amounts: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, List[str]]:
        return {
            "emails": self.emails,
            "phones": self.phones,
            "ibans": self.ibans,
            "postal_codes": self.postal_codes,
            "tckns": self.tckns,
            "amounts": self.amounts,
        }


def extract_entities(text: str) -> TurkishEntities:
    """Extract structured Turkish domain entities from raw text."""
    raw = text or ""
    emails = sorted(set(EMAIL_RE.findall(raw)))
    ibans = sorted({re.sub(r"[\s-]", "", m).upper() for m in TR_IBAN_RE.findall(raw)})
    phones = sorted({m.strip() for m in TR_PHONE_RE.findall(raw)})
    tckns = sorted({m for m in TCKN_RE.findall(raw) if validate_tckn(m)})
    amounts = sorted({m.strip() for m in CURRENCY_RE.findall(raw)})

    # Remove IBANs and phones before postal code matching to avoid substring collisions
    cleaned_for_zip = TR_IBAN_RE.sub(" ", TR_PHONE_RE.sub(" ", raw))
    postal_codes = sorted(set(POSTAL_CODE_RE.findall(cleaned_for_zip)))

    return TurkishEntities(
        emails=emails,
        phones=phones,
        ibans=ibans,
        postal_codes=postal_codes,
        tckns=tckns,
        amounts=amounts,
    )
