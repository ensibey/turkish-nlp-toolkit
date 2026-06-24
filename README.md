# turkish-nlp-toolkit

The missing NLP toolkit for Turkish text.

## Install
```
pip install turkish-nlp-toolkit
```

## Quick Start
```python
from turkish_nlp import Pipeline

pipe = (
    Pipeline()
    .clean(urls=True, emojis=True)
    .normalize(lowercase=True)
    .expand_abbreviations()
    .tokenize()
    .remove_stopwords()
)
tokens = pipe.run("Dr. Ayse Istanbul'da calisiyor! https://example.com")
```

## Features
- **Normalizer**: Turkish-aware lowercasing (correct İ→i, I→ı mapping)
- **Cleaner**: HTML, URL, emoji, mention removal
- **Abbreviations**: 150+ Turkish abbreviations
- **Tokenizer**: Sentence + word tokenization with apostrophe support
- **Stopwords**: 350+ Turkish function words
- **Pipeline**: Fluent chainable API
- **BERT**: TurkishClassifier for `dbmdz/bert-base-turkish-cased`

## License
MIT
