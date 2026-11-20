"""
Reproducible Throughput & Accuracy Benchmark for turkish-nlp-toolkit.

Measures:
- Full Pipeline throughput (docs/sec) on Turkish text
- Address standardization throughput (addresses/sec)
- Abbreviation-aware sentence boundary accuracy
- Turkish structured entity extraction accuracy

Usage:
    python benchmarks/run_benchmark.py
    python benchmarks/run_benchmark.py --json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from turkish_nlp import Pipeline, address, deasciifier, entities, sentence

SAMPLE_DOCS: List[str] = [
    "İSTANBUL Kadıköy Moda Mah. 3. Cad. No: 14 Daire: 5 adresine hızlı kargo teslimatı yapıldı.",
    "Prof. Dr. Ahmet Yılmaz 2. sınıf öğrencileriyle doğal dil işleme dersinde BERT modellerini inceledi.",
    "Cok guzel ve kaliteli urun, paketleme saglamdi, tesekkurler!",
    "ANKARA Çankaya Kızılay Bul. No. 22 Kat: 4 adresindeki ofise fatura 1.450,00 TL olarak kesildi.",
    "Şirketlerin kurum içi verilerini gizli tutan yerel RAG sistemleri büyük ilgi görüyor.",
]

SAMPLE_ADDRESSES: List[str] = [
    "Atatürk Mah. Cumhuriyet Cad. No:12 D:4 Kadıköy/İstanbul",
    "Bahçelievler Mh. 7. Cd. 45. Sk. No:8 Çankaya Ankara",
    "Bostanlı Mah. Cemal Gürsel Blv. No:102 K:3 Karşıyaka İzmir",
    "Nilüfer Mah. Fatih Sultan Mehmet Bulv. No:21 Bursa",
]


def run_benchmark(iterations: int = 200) -> Dict[str, Any]:
    pipe = Pipeline().clean().normalize().expand_abbreviations().tokenize().remove_stopwords().stem()

    # 1. Pipeline throughput
    total_docs = len(SAMPLE_DOCS) * iterations
    t0 = time.perf_counter()
    for _ in range(iterations):
        for doc in SAMPLE_DOCS:
            pipe.run(doc)
    pipe_sec = time.perf_counter() - t0
    pipe_docs_per_sec = total_docs / max(pipe_sec, 1e-6)

    # 2. Address standardization throughput
    total_addrs = len(SAMPLE_ADDRESSES) * iterations
    t1 = time.perf_counter()
    for _ in range(iterations):
        for addr in SAMPLE_ADDRESSES:
            address.standardize_address(addr)
    addr_sec = time.perf_counter() - t1
    addrs_per_sec = total_addrs / max(addr_sec, 1e-6)

    # 3. Functional accuracy checks
    sents = sentence.split_sentences(
        "Prof. Dr. Ali 3. sınıfta okuyor. Kargo Atatürk Mah. No. 5 adresine gitti! Teşekkürler."
    )
    sent_exact = len(sents) == 3

    ent_res = entities.extract_entities(
        "Mail: test@ornek.com, Tel: +90 532 555 12 34, Posta: 34710, IBAN: TR330006100519786457841326, Tutar: 499,90 TL"
    )
    ent_exact = (
        ent_res.emails == ["test@ornek.com"]
        and len(ent_res.phones) == 1
        and ent_res.postal_codes == ["34710"]
        and len(ent_res.ibans) == 1
        and ent_res.amounts == ["499,90 TL"]
    )

    deasc_exact = deasciifier.restore_diacritics("Cok guzel urun, Kadikoy") == "Çok güzel ürün, Kadıköy"

    return {
        "pipeline_docs_evaluated": total_docs,
        "pipeline_docs_per_sec": round(pipe_docs_per_sec, 1),
        "address_docs_evaluated": total_addrs,
        "address_docs_per_sec": round(addrs_per_sec, 1),
        "sentence_splitter_exact": sent_exact,
        "entity_extractor_exact": ent_exact,
        "deasciifier_exact": deasc_exact,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run turkish-nlp-toolkit throughput and accuracy benchmark.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = run_benchmark()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("turkish-nlp-toolkit Throughput & Accuracy Benchmark")
        print("=" * 54)
        print(f"Full Pipeline Throughput : {report['pipeline_docs_per_sec']:,.1f} docs/sec ({report['pipeline_docs_evaluated']} docs)")
        print(f"Address Normalizer Speed : {report['address_docs_per_sec']:,.1f} addrs/sec ({report['address_docs_evaluated']} addrs)")
        print(f"Sentence Splitter Exact  : {report['sentence_splitter_exact']}")
        print(f"Entity Extractor Exact   : {report['entity_extractor_exact']}")
        print(f"Deasciifier Exact        : {report['deasciifier_exact']}")

    ok = report["sentence_splitter_exact"] and report["entity_extractor_exact"] and report["deasciifier_exact"]
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
