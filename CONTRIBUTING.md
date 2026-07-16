# Contributing

Install `requirements-dev.txt`, then run `ruff format --check src benchmarks tests`,
`ruff check src benchmarks tests`, `bandit -q -r src/orchestrator`,
`pip-audit -r requirements-runtime.txt`, `pytest`, and the benchmark. Add positive, negative,
edge, integration, and regression tests. Performance/model claims require their generating command,
seed, dataset/artifact identity, and environment provenance.
