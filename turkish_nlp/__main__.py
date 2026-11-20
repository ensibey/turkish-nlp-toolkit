"""Command-line entry point for turkish_nlp."""
from __future__ import annotations

import argparse
import json
import sys
from typing import List, Optional

from . import address, deasciifier, entities, normalizer, sentence, stemmer, tokenizer
from .pipeline import Pipeline


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="turkish-nlp",
        description="Turkish text preprocessing, stemming, and address standardization CLI.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_norm = sub.add_parser("normalize", help="Normalize Turkish text (İ/I lowercasing, NFC)")
    p_norm.add_argument("text", help="Input text string")

    p_stem = sub.add_parser("stem", help="Tokenize and strip agglutinative suffixes")
    p_stem.add_argument("text", help="Input word or sentence")

    p_addr = sub.add_parser("address", help="Standardize and parse a Turkish postal address")
    p_addr.add_argument("text", help="Raw address string")
    p_addr.add_argument("--json", action="store_true", help="Output parsed components as JSON")

    p_pipe = sub.add_parser("pipeline", help="Run full preprocessing pipeline on text")
    p_pipe.add_argument("text", help="Input text string")

    p_sent = sub.add_parser("sentences", help="Split Turkish text into sentences (abbreviation-aware)")
    p_sent.add_argument("text", help="Input text string")

    p_ent = sub.add_parser("entities", help="Extract Turkish emails, phones, IBANs, postal codes, and TCKN")
    p_ent.add_argument("text", help="Input text string")

    p_deasc = sub.add_parser("deasciify", help="Restore Turkish diacritics on ASCII-typed text")
    p_deasc.add_argument("text", help="Input ASCII-typed Turkish text")

    args = parser.parse_args(argv)

    if args.command == "normalize":
        print(normalizer.normalize(args.text))
    elif args.command == "stem":
        tokens = tokenizer.word_tokenize(normalizer.normalize(args.text))
        print(" ".join(stemmer.stem(tokens)))
    elif args.command == "address":
        if args.json:
            print(json.dumps(address.parse_address_components(args.text), ensure_ascii=False, indent=2))
        else:
            print(address.standardize_address(args.text))
    elif args.command == "pipeline":
        pipe = (
            Pipeline()
            .clean()
            .normalize()
            .expand_abbreviations()
            .tokenize()
            .remove_stopwords()
            .stem()
        )
        print(" ".join(pipe.run(args.text)))
    elif args.command == "sentences":
        print(json.dumps(sentence.split_sentences(args.text), ensure_ascii=False, indent=2))
    elif args.command == "entities":
        print(json.dumps(entities.extract_entities(args.text).to_dict(), ensure_ascii=False, indent=2))
    elif args.command == "deasciify":
        print(deasciifier.restore_diacritics(args.text))

    return 0


if __name__ == "__main__":
    sys.exit(main())
