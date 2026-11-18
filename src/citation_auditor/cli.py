from __future__ import annotations

import argparse
import json
from pathlib import Path

from rich.console import Console
from rich.table import Table

from citation_auditor.auditor import audit_file

console = Console()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="citation-auditor")
    parser.add_argument("--cases", default="samples/cases.jsonl")
    parser.add_argument("--docs", default="samples/docs")
    parser.add_argument("--results", default="results")
    args = parser.parse_args(argv)

    report = audit_file(Path(args.cases), Path(args.docs))
    out = Path(args.results)
    out.mkdir(parents=True, exist_ok=True)
    (out / "citation_audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    table = Table(title="Citation Auditor")
    table.add_column("id")
    table.add_column("ok")
    table.add_column("support", justify="right")
    for item in report["details"]:
        table.add_row(item["id"], "yes" if item["ok"] else "no", f"{item['support_ratio']:.0%}")
    console.print(table)
    console.print(f"score: [bold]{report['score']:.0%}[/bold] ({report['passed']}/{report['total']})")
    return 0 if report["score"] >= 0.5 else 1


if __name__ == "__main__":
    raise SystemExit(main())
