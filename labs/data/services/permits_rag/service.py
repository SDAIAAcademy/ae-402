"""Muyassir's retrieval service, as the permits team wrote it for itself (synthetic).

Everything another team would change is hard-coded below. Evaluation is a script someone may run; nothing
checks the classification of the model, and nothing is traced.
"""
from __future__ import annotations

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SERVICE = "permits-rag"
TEAM = "T01"
LEVEL = "Restricted"
MODEL = "ksa-general-m"
TOP_K = 3

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


def answer(question: str) -> dict:
    docs = load_docs()
    hits = retrieve(question, docs, TOP_K)
    first = next(l for l in docs[hits[0]].splitlines() if l and not l.startswith("#"))
    # the model call (MODEL, through the gateway) is a scripted stand-in: the first sentence of the top source
    return {"answer": first.split(". ")[0].rstrip(".") + ".", "sources": hits}
