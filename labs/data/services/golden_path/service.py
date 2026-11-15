"""A retrieval service on the Asas golden path (synthetic).

Its settings live in service.json, which the template writes from the team's answers. Every answer is
traced to traces.jsonl with a hash of the question, never its text.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
CFG = json.loads((HERE / "service.json").read_text(encoding="utf-8"))

STOP = {"a", "an", "the", "is", "are", "do", "does", "i", "my", "to", "of", "for", "what", "which", "how",
        "can", "it", "or", "not", "need", "needs", "on", "in", "must", "be", "by", "after", "and", "who", "when",
        "until", "many", "from", "with", "its", "has", "per", "that", "this", "at"}


def load_docs() -> dict[str, str]:
    return {p.stem: p.read_text(encoding="utf-8") for p in sorted((HERE / "docs").glob("*.md"))}


def words(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower())) - STOP


def retrieve(question: str, docs: dict[str, str], k: int) -> list[str]:
    q = words(question)
    return sorted(docs, key=lambda d: (-len(q & words(docs[d])), d))[:k]


def _trace(question: str, span: str, **fields) -> None:
    if not CFG.get("tracing"):
        return
    rec = {"service": CFG["service_name"], "team": CFG["team"], "level": CFG["classification"], "span": span,
           "question_sha256": hashlib.sha256(question.encode("utf-8")).hexdigest()[:16], **fields}
    with open(HERE / "traces.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")


def answer(question: str) -> dict:
    docs = load_docs()
    hits = retrieve(question, docs, CFG["top_k"])
    _trace(question, "retrieve", sources=hits)
    first = next(l for l in docs[hits[0]].splitlines() if l and not l.startswith("#"))
    # the model call goes to CFG["model_alias"] through the gateway; here a scripted stand-in
    _trace(question, "generate", model_alias=CFG["model_alias"])
    return {"answer": first.split(". ")[0].rstrip(".") + ".", "sources": hits}
