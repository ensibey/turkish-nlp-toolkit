"""Tests for turkish-nlp CLI subcommands."""

import json

from turkish_nlp.__main__ import main


def test_cli_sentences_entities_and_deasciify(capsys):
    assert main(["sentences", "Dr. Ali geldi. Kargo teslim edildi."]) == 0
    sents = json.loads(capsys.readouterr().out)
    assert len(sents) == 2

    assert main(["entities", "Posta: 34710, Mail: ali@ornek.com"]) == 0
    ents = json.loads(capsys.readouterr().out)
    assert ents["postal_codes"] == ["34710"]
    assert ents["emails"] == ["ali@ornek.com"]

    assert main(["deasciify", "Cok guzel urun"]) == 0
    assert "Çok güzel ürün" in capsys.readouterr().out
