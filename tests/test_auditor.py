from pathlib import Path

from citation_auditor.auditor import audit_file, audit_item, load_corpus

ROOT = Path(__file__).resolve().parents[1]


def test_audit_ok_and_bad():
    corpus = load_corpus(ROOT / "samples" / "docs")
    ok = audit_item(
        "El descuento máximo autorizado en A1 es 12%.",
        ["politica_a1"],
        corpus,
        expected="politica_a1",
    )
    assert ok["ok"] is True

    bad = audit_item(
        "A1 incluye viaje gratis a la luna.",
        ["politica_a1"],
        corpus,
        expected="politica_a1",
    )
    assert bad["ok"] is False


def test_audit_file_score():
    report = audit_file(ROOT / "samples" / "cases.jsonl", ROOT / "samples" / "docs")
    assert report["total"] == 4
    assert 0 < report["score"] < 1
