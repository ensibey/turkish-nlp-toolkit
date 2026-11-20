"""Tests for abbreviation- and ordinal-aware Turkish sentence splitter."""

from turkish_nlp.sentence import split_sentences


def test_preserves_honorifics_addresses_and_ordinals():
    text = (
        "Prof. Dr. Ahmet Yılmaz 3. sınıf öğrencileriyle görüştü. "
        "Kargo Atatürk Mah. 2. Cad. No. 14 adresine teslim edildi! "
        "Başka bir soru var mı? Hayır, teşekkürler."
    )
    sents = split_sentences(text)
    assert len(sents) == 4
    assert sents[0].startswith("Prof. Dr. Ahmet Yılmaz 3. sınıf")
    assert "Atatürk Mah. 2. Cad. No. 14" in sents[1]
    assert sents[2] == "Başka bir soru var mı?"
    assert sents[3] == "Hayır, teşekkürler."


def test_handles_empty_and_no_punctuation():
    assert split_sentences("   ") == []
    assert split_sentences("Noktasız tek cümle") == ["Noktasız tek cümle"]
