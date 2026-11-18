from __future__ import annotations

import json
import re
from pathlib import Path

TOKEN = re.compile(r"[a-zA-ZáéíóúñÁÉÍÓÚÑ0-9]+")
STOP = {"el", "la", "los", "las", "de", "del", "un", "una", "y", "o", "en", "para", "con", "por", "que", "es", "son"}


def tokenize(text: str) -> set[str]:
    return {t.lower() for t in TOKEN.findall(text) if t.lower() not in STOP and len(t) > 2}


def load_corpus(docs_dir: Path) -> dict[str, str]:
    return {
        path.stem: path.read_text(encoding="utf-8")
        for path in sorted(docs_dir.glob("*.txt"))
    }


def audit_item(answer: str, citations: list[str], corpus: dict[str, str], expected: str | None = None) -> dict:
    missing = [c for c in citations if c not in corpus]
    present = [c for c in citations if c in corpus]
    contexts = [corpus[c] for c in present]
    ctx_tokens: set[str] = set()
    for text in contexts:
        ctx_tokens |= tokenize(text)
    ans_tokens = tokenize(answer)
    supported = len([t for t in ans_tokens if t in ctx_tokens])
    support_ratio = supported / len(ans_tokens) if ans_tokens else 1.0
    expected_ok = True if expected is None else expected in citations
    ok = (
        len(citations) > 0
        and len(missing) == 0
        and support_ratio >= 0.45
        and expected_ok
    )
    return {
        "ok": ok,
        "citations": citations,
        "missing_docs": missing,
        "support_ratio": round(support_ratio, 4),
        "expected_ok": expected_ok,
    }


def audit_file(cases_path: Path, docs_dir: Path) -> dict:
    corpus = load_corpus(docs_dir)
    cases = [
        json.loads(line)
        for line in cases_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    details = []
    passed = 0
    for case in cases:
        result = audit_item(
            answer=case["answer"],
            citations=case.get("citations", []),
            corpus=corpus,
            expected=case.get("expected_doc"),
        )
        details.append({"id": case["id"], **result})
        passed += int(result["ok"])
    return {
        "passed": passed,
        "total": len(cases),
        "score": round(passed / len(cases), 4) if cases else 0.0,
        "details": details,
    }
