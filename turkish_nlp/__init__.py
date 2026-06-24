"""
turkish-nlp-toolkit
===================
A comprehensive NLP toolkit for the Turkish language.

Quick start:
    from turkish_nlp import Pipeline
    pipe = Pipeline().clean().normalize().expand_abbreviations().tokenize().remove_stopwords()
    tokens = pipe.run("Dr. Ayse Istanbul'da calisiyor!")
"""

__version__ = "0.1.0"
__author__ = "Enis Dogan"

from . import abbreviations
from . import cleaner
from . import normalizer
from . import stopwords
from . import tokenizer
from .pipeline import Pipeline

__all__ = ["Pipeline", "normalizer", "cleaner", "tokenizer", "stopwords", "abbreviations", "__version__"]
