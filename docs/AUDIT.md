# Production readiness audit

## Summary

The repository contains a promising FastAPI/MLflow service, metrics, Docker assets, and synthetic
training pipeline, but it previously mixed two unrelated APIs, installed an unbounded full ML/UI
stack in production, accepted arbitrary feature dictionaries, exposed exception text, and treated
an unavailable MLflow registry as an acceptable test result.

## Findings

| Priority | Finding | Risk | Treatment |
|---|---|---|---|
| P0 | Prediction test allowed HTTP 500 | False production confidence | Reproducible local backend and exact 200 contract |
| P0 | Arbitrary records and unbounded batch | resource/schema abuse | strict finite f1/f2/f3 schema and 1,000-row bound |
| P0 | Raw exception returned | information disclosure | sanitized 503 |
| P1 | Root, oversized image | attack surface | minimal pinned runtime, UID 10001 |
| P1 | MLflow stage API is deprecated/ambiguous | unsafe promotion | explicit alias-based optional backend |
| P1 | CI mutates code with --fix | non-reproducible gate | check-only lint/format/security pipeline |
| P1 | Claims exceeded evidence | recruiter/user credibility | evidence-based README and artifact provenance |

## Strengths

Package layout, configuration, Prometheus metrics, synthetic seeded training, MLflow integration,
and existing tests provide a sound foundation.

## Residual risks

The repository has no durable production registry, authentication model, shared database, signed
trained artifact, or real labeled dataset. The reference model's RMSE/MAE/R2 describe seeded
synthetic regression only. Network load at 1–10,000 users requires staging infrastructure. GPU,
MAP, MRR, NDCG, and classification metrics are not applicable to the current regression contract.
