"""Composable NLP pipeline for Turkish text."""
from typing import Callable, Dict, List, Optional, Set, Union
from . import cleaner as _cleaner, normalizer as _normalizer
from . import abbreviations as _abbreviations, tokenizer as _tokenizer, stopwords as _stopwords

class Pipeline:
    """
    Fluent builder for Turkish NLP preprocessing.

    Example:
        pipe = (Pipeline()
            .clean(urls=True, emojis=True)
            .normalize(lowercase=True)
            .expand_abbreviations()
            .tokenize()
            .remove_stopwords())
        tokens = pipe.run("Dr. Ayse Istanbul'da calisiyor!")
    """
    def __init__(self): self._steps = []

    def clean(self, html=True, urls=True, emails=True, mentions=True,
              hashtags=True, emojis=True, numbers=False, punctuation=False):
        def _step(text):
            return _cleaner.clean(text, html=html, urls=urls, emails=emails,
                mentions=mentions, hashtags=hashtags, emojis=emojis,
                numbers=numbers, punctuation=punctuation)
        self._steps.append(("clean", _step)); return self

    def normalize(self, lowercase=True, fix_encoding=True, collapse_spaces=True):
        def _step(text):
            return _normalizer.normalize(text, lowercase=lowercase,
                fix_encoding=fix_encoding, collapse_spaces=collapse_spaces)
        self._steps.append(("normalize", _step)); return self

    def expand_abbreviations(self, extra=None):
        def _step(text): return _abbreviations.expand(text, extra=extra)
        self._steps.append(("expand_abbreviations", _step)); return self

    def tokenize(self, keep_apostrophe_suffixes=True):
        def _step(text):
            if isinstance(text, list): return text
            return _tokenizer.word_tokenize(text, keep_apostrophe_suffixes=keep_apostrophe_suffixes)
        self._steps.append(("tokenize", _step)); return self

    def remove_stopwords(self, extra=None, keep=None):
        def _step(tokens):
            if isinstance(tokens, str): tokens = _tokenizer.word_tokenize(tokens)
            return _stopwords.remove_stopwords(tokens, extra=extra, keep=keep)
        self._steps.append(("remove_stopwords", _step)); return self

    def apply(self, fn, name="custom"):
        self._steps.append((name, fn)); return self

    def run(self, text):
        result = text
        for _, step in self._steps: result = step(result)
        return result

    def run_batch(self, texts): return [self.run(t) for t in texts]

    def __repr__(self):
        return "Pipeline([" + " -> ".join(n for n,_ in self._steps) + "])"
