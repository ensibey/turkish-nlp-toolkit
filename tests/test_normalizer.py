import unittest
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
        text = "Türkiye\u2019nin"  # RIGHT SINGLE QUOTATION MARK
        fixed = normalizer.fix_chars(text)
        self.assertNotIn("\u2019", fixed)
        self.assertIn("'", fixed)

    def test_normalize_full(self):
        result = normalizer.normalize("  İSTANBUL'DA yaşıyorum!  ")
        self.assertEqual(result, "istanbul'da yaşıyorum!")


if __name__ == "__main__":
    unittest.main()
