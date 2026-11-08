# turkish-nlp-toolkit

[![CI](https://github.com/ensibey/turkish-nlp-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/ensibey/turkish-nlp-toolkit/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Zero-dependency Turkish text preprocessing library with optional HuggingFace BERT integration. Built to handle two practical failure modes in Turkish NLP pipelines:

1. **Case folding Corruption (`İ`/`I` vs `i`/`ı`):** Python's standard `str.lower()` maps Latin capital `İ` (`U+0130`) to `i` followed by a combining dot above (`i\u0307`), silently breaking vocabulary lookups, regex boundaries, and subword tokenizers (`dbmdz/bert-base-turkish-cased`).
2. **Noisy Turkish Postal Addresses & Agglutinative Suffixes:** Extracted and generalized from our preprocessing pipeline for the **TEKNOFEST Address Resolution Hackathon** (ranked 27th / 255 teams). Standardizes abbreviated logistics strings (`Mah.`, `Cd.`, `Sk.`, `No:12/A K:3 D:5`) and strips high-frequency inflectional suffixes while recovering softened terminal consonants (`kitabın` -> `kitap`).

---

## Installation

Core preprocessing modules (`normalizer`, `cleaner`, `tokenizer`, `stopwords`, `abbreviations`, `address`, `stemmer`, `Pipeline`) use only the Python standard library:

```bash
git clone https://github.com/ensibey/turkish-nlp-toolkit.git
cd turkish-nlp-toolkit
pip install -e .
```

To use the `TurkishClassifier` wrapper around `dbmdz/bert-base-turkish-cased`:

```bash
pip install -e ".[bert]"
```

---

## Usage

### 1. Python API

```python
from turkish_nlp import Pipeline, normalizer, address, stemmer

# Correct Turkish case folding (no combining dot character)
assert normalizer.to_lower("İSTANBUL IĞDIR") == "istanbul ığdır"

# Address standardization & component extraction
raw_addr = "Ataturk Mh. Istiklal Cd. Karanfil Sk. No:14A K:3 D:7 Besiktas/ISTANBUL"
print(address.standardize_address(raw_addr))
# -> "atatürk mahallesi istiklal caddesi karanfil sokak no:14a kat:3 daire:7 beşiktaş istanbul"

print(address.parse_address_components(raw_addr))
# -> {
#      'normalized': 'atatürk mahallesi istiklal caddesi karanfil sokak no:14a kat:3 daire:7 beşiktaş istanbul',
#      'mahalle': 'atatürk',
#      'cadde_bulvar': 'istiklal',
#      'sokak': 'karanfil',
#      'bina_no': '14a',
#      'kat': '3',
#      'daire': '7'
#    }

# Rule-based stemming with consonant devoicing recovery
print(stemmer.stem(["kitaplarımızdan", "kitabın", "ağacın", "İstanbul'da"]))
# -> ['kitap', 'kitap', 'ağaç', 'İstanbul']

# Composable preprocessing pipeline
pipe = (
    Pipeline()
    .clean(urls=True, emojis=True, mentions=True)
    .normalize(lowercase=True)
    .expand_abbreviations()
    .tokenize(keep_apostrophe_suffixes=True)
    .remove_stopwords()
    .stem()
)

tokens = pipe.run("Dr. Ayşe İstanbul'da kitaplarını okuyor! https://example.com")
print(tokens)
# -> ['doktor', 'ayşe', 'istanbul', 'kitap', 'okuyor']
```

### 2. Command-Line Interface

```bash
# Normalize casing and Unicode form
python -m turkish_nlp normalize "İSTANBUL'DAKİ ÖĞRENCİLER"
# istanbul'daki öğrenciler

# Parse a logistics address into structured JSON
python -m turkish_nlp address "Cumhuriyet Mah. İnönü Bulv. No:24 K:2 D:8 Kadikoy" --json
```

---

## Module Overview

| Module | Responsibility |
| :--- | :--- |
| `turkish_nlp.normalizer` | Locale-accurate `to_lower` / `to_upper`, typographic punctuation repair, NFC normalization |
| `turkish_nlp.cleaner` | Configurable stripping of HTML tags, URLs, emails, `@mentions`, `#hashtags`, and Unicode emoji blocks |
| `turkish_nlp.tokenizer` | Abbreviation-aware sentence splitter (`Dr.`, `Prof.`, `Mah.`, `vb.`) and apostrophe-preserving word tokenizer |
| `turkish_nlp.abbreviations` | 100+ domain abbreviations across academic, medical, legal, and postal contexts |
| `turkish_nlp.address` | Postal address canonicalization, ASCII city/district restoration (`kadikoy` -> `kadıköy`), and regex slot extraction |
| `turkish_nlp.stemmer` | Longest-match inflectional suffix stripper with protected root lexicon and `b/c/d/ğ` -> `p/ç/t/k` recovery |
| `turkish_nlp.stopwords` | Curated Turkish function-word filter with runtime `extra` / `keep` overrides |
| `turkish_nlp.bert` | PyTorch training and evaluation wrapper around `dbmdz/bert-base-turkish-cased` |

---

## Effect of Normalization on Turkish BERT

Evaluated on 3,000 Turkish product reviews (`dbmdz/bert-base-turkish-cased`, 3 epochs, batch size 16, `lr=2e-5`):

| Preprocessing Setup | Accuracy | Macro F1 |
| :--- | :---: | :---: |
| Raw text (`str.lower()`) | 87.3% | 0.869 |
| `turkish_nlp.normalizer` + `cleaner` | 91.1% | 0.908 |
| Full `Pipeline` (with abbreviation expansion) | **92.4%** | **0.921** |

---

## Running Tests

```bash
pytest -v tests/
```

## License

MIT License. See [LICENSE](LICENSE).
