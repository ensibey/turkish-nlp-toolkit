"""Regression test for turkish-nlp-toolkit throughput and accuracy benchmark."""

from benchmarks.run_benchmark import run_benchmark


def test_turkish_nlp_benchmark_passes():
    report = run_benchmark(iterations=50)
    assert report["pipeline_docs_per_sec"] > 500
    assert report["address_docs_per_sec"] > 1000
    assert report["sentence_splitter_exact"] is True
    assert report["entity_extractor_exact"] is True
    assert report["deasciifier_exact"] is True
