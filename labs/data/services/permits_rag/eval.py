"""Retrieval hit rate on the permits team's evaluation set. Run by hand: python eval.py"""
import json
from service import HERE, TOP_K, load_docs, retrieve

rows = [json.loads(l) for l in (HERE / "eval_set.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
docs = load_docs()
hits = sum(r["expected"] in retrieve(r["question"], docs, TOP_K) for r in rows)
print(f"hit rate {hits / len(rows):.2f} on {len(rows)} questions")
