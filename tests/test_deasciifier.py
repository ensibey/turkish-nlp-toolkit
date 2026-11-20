"""Tests for Turkish diacritic restoration (deasciifier)."""

from turkish_nlp.deasciifier import restore_diacritics


def test_restores_diacritics_preserving_case():
    raw = "Cok guzel urun, Kadikoy ve Besiktas teslimat cok hizli! TESEKKURLER."
    restored = restore_diacritics(raw)
    assert "Çok güzel ürün" in restored
    assert "Kadıköy" in restored
    assert "Beşiktaş" in restored
    assert "hızlı" in restored
    assert "TEŞEKKÜRLER" in restored


def test_leaves_unknown_and_already_correct_words_untouched():
    assert restore_diacritics("Python 3.11 FastAPI") == "Python 3.11 FastAPI"
    assert restore_diacritics("") == ""
