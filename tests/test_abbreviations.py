import unittest
try:
    import pytest
except ImportError:
    pytest = None
from turkish_nlp import abbreviations


class TestAbbreviations(unittest.TestCase):

    def test_expand_basic(self):
        result = abbreviations.expand("Dr. Ayse")
        self.assertIn("doktor", result.lower())

    def test_expand_address(self):
        result = abbreviations.expand("Mah. No. 5")
        self.assertIn("mahallesi", result.lower())
        self.assertIn("numara", result.lower())

    def test_expand_case_insensitive(self):
        result = abbreviations.expand("dr. mehmet")
        self.assertIn("doktor", result.lower())

    def test_add_custom_abbreviation(self):
        abbreviations.add_abbreviation("xyz.", "xyzSirketi")
        result = abbreviations.expand("xyz.")
        self.assertIn("xyzsirketi", result.lower())
        abbreviations.remove_abbreviation("xyz.")

    def test_get_abbreviations_returns_dict(self):
        d = abbreviations.get_abbreviations()
        self.assertIsInstance(d, dict)
        self.assertGreater(len(d), 50)


# pytest compatibility
def test_expand_basic(): TestAbbreviations().test_expand_basic()
def test_expand_address(): TestAbbreviations().test_expand_address()
def test_expand_case_insensitive(): TestAbbreviations().test_expand_case_insensitive()
def test_add_custom_abbreviation(): TestAbbreviations().test_add_custom_abbreviation()
def test_get_abbreviations_returns_dict(): TestAbbreviations().test_get_abbreviations_returns_dict()


if __name__ == "__main__":
    unittest.main()
