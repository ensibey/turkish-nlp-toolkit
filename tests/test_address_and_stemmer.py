"""Unit tests for Turkish Address Standardization, Stemmer, and Composable Pipeline."""

from turkish_nlp import Pipeline, address, stemmer, tokenizer


def test_address_standardization_and_parsing():
    raw = "Ataturk Mah. Cumhuriyet Cad. Gul Sk. No: 12B Kat:3 D:8 Kadikoy/Istanbul"
    norm = address.standardize_address(raw)
    assert "atatürk mahallesi" in norm
    assert "cumhuriyet caddesi" in norm
    assert "gül sokak" in norm or "gul sokak" in norm
    assert "no:12b" in norm
    assert "kat:3" in norm
    assert "daire:8" in norm
    assert "kadıköy" in norm

    parsed = address.parse_address_components(raw)
    assert parsed["mahalle"] == "atatürk"
    assert parsed["cadde_bulvar"] == "cumhuriyet"
    assert parsed["bina_no"] == "12b"
    assert parsed["kat"] == "3"
    assert parsed["daire"] == "8"


def test_turkish_agglutinative_stemmer():
    assert stemmer.stem_word("kitaplarımızdan") == "kitap"
    assert stemmer.stem_word("kitabın") == "kitap"
    assert stemmer.stem_word("okullarda") == "okul"
    assert stemmer.stem_word("İstanbul'da") == "İstanbul"


def test_end_to_end_pipeline():
    pipe = (
        Pipeline()
        .clean(urls=True, emojis=True)
        .normalize(lowercase=True)
        .expand_abbreviations()
        .tokenize()
        .remove_stopwords()
        .stem()
    )
    tokens = pipe.run("Prof. Dr. Ahmet kitaplarımızdan bahsetti https://example.com")
    assert "profesör" in tokens
    assert "doktor" in tokens
    assert "kitap" in tokens
