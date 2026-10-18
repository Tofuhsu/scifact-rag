"""Binary-relevance nDCG@k and Recall@k, same definitions as the original experiment.

DCG@k  = sum over the first k results of rel / log2(rank + 1)
IDCG@k = sum of 1 / log2(rank + 1) for rank 1..min(k, |R|)
Recall@k = distinct known positives in the first k / |R|
The aggregate is the unweighted mean over queries.
"""
from __future__ import annotations

import math


def ndcg_at_k(ranked_ids, relevant, k=10):
    if not relevant:
        raise ValueError("Query has no known positives")
    dcg = sum(1.0 / math.log2(rank + 2) for rank, did in enumerate(ranked_ids[:k]) if did in relevant)
    idcg = sum(1.0 / math.log2(rank + 2) for rank in range(min(k, len(relevant))))
    return dcg / idcg


def recall_at_k(ranked_ids, relevant, k=10):
    if not relevant:
        raise ValueError("Query has no known positives")
    return len(set(ranked_ids[:k]) & set(relevant)) / len(relevant)


def evaluate(qrels, run, k=10):
    """qrels: {qid: {doc_id: 1}}; run: {qid: [doc_id, ...]} ranked best-first."""
    if set(qrels) != set(run):
        raise ValueError("Run and qrels must cover exactly the same queries")
    per_query = {qid: {f"nDCG@{k}": ndcg_at_k(run[qid], qrels[qid], k),
                       f"Recall@{k}": recall_at_k(run[qid], qrels[qid], k)} for qid in sorted(qrels)}
    n = len(per_query)
    return {
        "queries": n,
        f"nDCG@{k}": math.fsum(m[f"nDCG@{k}"] for m in per_query.values()) / n,
        f"Recall@{k}": math.fsum(m[f"Recall@{k}"] for m in per_query.values()) / n,
        "per_query": per_query,
    }
