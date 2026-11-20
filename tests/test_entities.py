"""Tests for Turkish structured entity extractor."""

from turkish_nlp.entities import extract_entities, validate_tckn


def test_extracts_turkish_domain_entities():
    text = (
        "Alıcı: enis@ornek.com, Tel: +90 532 555 12 34, Posta Kodu: 34710 Kadıköy. "
        "IBAN: TR33 0006 1005 1978 6457 8413 26, Tutar: 1.250,50 TL, TC: 10000000146."
    )
    ents = extract_entities(text)
    assert ents.emails == ["enis@ornek.com"]
    assert len(ents.phones) == 1
    assert ents.ibans == ["TR330006100519786457841326"]
    assert ents.postal_codes == ["34710"]
    assert ents.tckns == ["10000000146"]
    assert ents.amounts == ["1.250,50 TL"]


def test_rejects_invalid_postal_code_and_tckn():
    assert validate_tckn("12345678901") is False
    ents = extract_entities("Kod: 99999 ve 00123")
    assert ents.postal_codes == []
