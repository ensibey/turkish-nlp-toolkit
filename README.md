# turkish-nlp-toolkit

[![Turkish NLP Toolkit CI](https://github.com/ensibey/turkish-nlp-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/ensibey/turkish-nlp-toolkit/actions/workflows/ci.yml)
![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-3776AB?logo=python&logoColor=white)
![Zero Core Dependencies](https://img.shields.io/badge/core%20dependencies-0-10B981)
![License: MIT](https://img.shields.io/badge/license-MIT-10B981)
![Tests: 27 passing](https://img.shields.io/badge/tests-27%20passing-10B981)

A **zero-dependency Python NLP library** for Turkish text preprocessing, agglutinative stemming, abbreviation-aware sentence splitting, diacritic restoration, structured Turkish entity extraction, postal address normalization (**TEKNOFEST Hepsiburada Hackathon Top 11% — 27th / 255 teams**), and optional Turkish BERT (`dbmdz/bert-base-turkish-cased`) fine-tuning.

---

## Modules

| Module | Capability |
| :--- | :--- |
| `turkish_nlp.normalizer` | Locale-accurate `İ/I` case folding (`İ -> i`, `I -> ı`), Unicode NFC normalization |
| `turkish_nlp.cleaner` | URL, HTML, punctuation, and noise removal |
| `turkish_nlp.abbreviations` | Turkish domain & address abbreviation expansion (`Mah.`, `Cad.`, `Sok.`, `Apt.`, `vb.`) |
| `turkish_nlp.sentence` | Abbreviation- & ordinal-aware Turkish sentence boundary splitter (`Prof. Dr.`, `3. sınıf`, `No. 14`) |
| `turkish_nlp.deasciifier` | Case-preserving Turkish diacritic restoration (`Cok guzel urun, Kadikoy` → `Çok güzel ürün, Kadıköy`) |
| `turkish_nlp.entities` | Zero-dependency extractor for Turkish postal codes (`01xxx`–`81xxx`), TR phones, TR IBANs, checksum-verified TCKN, emails, and TRY amounts |
| `turkish_nlp.address` | Postal address standardization & component parsing (neighborhood, street, building, district, city) |
| `turkish_nlp.stemmer` | Rule-based agglutinative suffix stripping for Turkish morphology |
| `turkish_nlp.pipeline` | Fluent chainable preprocessing pipeline (`clean().normalize().expand_abbreviations().tokenize().remove_stopwords().stem()`) |
| `turkish_nlp.bert` | Optional transfer-learning wrapper around `dbmdz/bert-base-turkish-cased` |

---

## Reproducible Throughput & Accuracy Benchmark

Measured on single-threaded Python 3.10 with zero external dependencies (`benchmarks/run_benchmark.py`):

```bash
python benchmarks/run_benchmark.py
```

| Benchmark | Measured Result |
| :--- | :---: |
| **Full Preprocessing Pipeline** (`clean → normalize → expand → tokenize → stopwords → stem`) | **`9,776.5 docs/sec`** |
| **Address Standardization** (`address.standardize_address`) | **`15,611.2 addrs/sec`** |
| **Sentence Splitter / Entity Extractor / Deasciifier Exact Checks** | **`100% pass`** |

---

## Quick Start

### Install

```bash
pip install -e .
# Optional BERT fine-tuning extras:
pip install -e ".[bert]"
```

### Python API

```python
from turkish_nlp import Pipeline, address, deasciifier, entities, sentence

pipe = Pipeline().clean().normalize().expand_abbreviations().tokenize().remove_stopwords().stem()
print(pipe.run("İSTANBUL Kadıköy Moda Mah. hızlı kargo teslimatı yapıldı."))

print(sentence.split_sentences("Prof. Dr. Ali 3. sınıfta okuyor. Kargo Atatürk Mah. No. 5 adresine gitti!"))
print(deasciifier.restore_diacritics("Cok guzel urun, Besiktas ve Kadikoy teslimat cok hizli!"))
print(entities.extract_entities("Posta: 34710, IBAN: TR330006100519786457841326, Tutar: 1.250,50 TL").to_dict())
print(address.parse_address_components("Atatürk Mah. Cumhuriyet Cad. No:12 D:4 Kadıköy/İstanbul"))
```

### CLI

```bash
turkish-nlp normalize "İSTANBUL IĞDIR"
turkish-nlp sentences "Prof. Dr. Ali geldi. Kargo teslim edildi."
turkish-nlp deasciify "Cok guzel urun, Kadikoy"
turkish-nlp entities "Mail: ali@ornek.com, Posta: 34710, Tutar: 499,90 TL"
turkish-nlp address "Atatürk Mah. Cumhuriyet Cad. No:12 Kadıköy/İstanbul" --json
```

### Tests

```bash
pytest -v tests/
```

---

## License

MIT
