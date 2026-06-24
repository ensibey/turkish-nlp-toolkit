import unittest
try:
    import pytest
except ImportError:
    pytest = None
from turkish_nlp import normalizer


class TestNormalizer(unittest.TestCase):

    def test_turkish_lowercase_I(self):
        """İ must become i, I must become ı (stdlib .lower() gets this wrong)."""
        self.assertEqual(normalizer.to_lower("İ"), "i")
        self.assertEqual(normalizer.to_lower("I"), "ı")

    def test_turkish_lowercase_word(self):
        self.assertEqual(normalizer.to_lower("İSTANBUL"), "istanbul")

    def test_normalize_strips_spaces(self):
        result = normalizer.normalize("  merhaba   dünya  ")
        self.assertEqual(result, "merhaba dünya")

    def test_normalize_lowercase(self):
        self.assertEqual(normalizer.normalize("TÜRKÇE"), "türkçe")

    def test_fix_chars(self):
        text = "Türkiye'nin"  # RIGHT SINGLE QUOTATION MARK
        fixed = normalizer.fix_chars(text)
        self.assertNotIn("'", fixed)
        self.assertIn("'", fixed)

    def test_normalize_full(self):
        result = normalizer.normalize("  İSTANBUL'DA yaşıyorum!  ")
        self.assertEqual(result, "istanbul'da yaşıyorum!")


# pytest compatibility
def test_turkish_lowercase_I(): TestNormalizer().test_turkish_lowercase_I()
def test_turkish_lowercase_word(): TestNormalizer().test_turkish_lowercase_word()
def test_normalize_strips_spaces(): TestNormalizer().test_normalize_strips_spaces()
def test_normalize_lowercase(): TestNormalizer().test_normalize_lowercase()
def test_fix_chars(): TestNormalizer().test_fix_chars()
def test_normalize_full(): TestNormalizer().test_normalize_full()


if __name__ == "__main__":
    unittest.main()
