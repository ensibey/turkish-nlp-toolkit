# turkish-nlp-toolkit

The missing NLP toolkit for Turkish text.

Battle-tested at TEKNOFEST Hepsiburada Hackathon — Top 11% (27th/255).

## Install
pip install turkish-nlp-toolkit

## Quick Start
from turkish_nlp import Pipeline

pipe = (
    Pipeline()
    .clean(urls=True, emojis=True)
    .normalize(lowercase=True)
    .expand_abbreviations()
    .tokenize()
    .remove_stopwords()
)
tokens = pipe.run("Dr. Ayse Istanbul da calisiyor! https://example.com")

## Features
- Normalizer: Turkish-aware lowercasing (correct I->i mapping)
- Cleaner: HTML, URL, emoji, mention removal
- Abbreviations: 150+ Turkish abbreviations
- Tokenizer: Sentence + word tokenization with apostrophe support
- Stopwords: 350+ Turkish function words
- Pipeline: Fluent chainable API
- BERT: TurkishClassifier for dbmdz/bert-base-turkish-cased

## License
MIT - Enis Dogan
