# Performance guide

`python benchmarks/run_benchmark.py` records average, median, p95, p99, min/max latency,
requests/second, success rate, peak Python allocation, payload hash, runtime, platform, and UTC
time. It also regenerates seeded synthetic RMSE, MAE, and R2.

This is in-process application benchmarking, not a network capacity promise. Compare only matching
schema, parameters, payload hash, runtime, and hardware. Run k6/Locust against staging for
1/10/100/1,000/10,000-user tests. GPU, training-resource, disk, and registry-network measurements
require the corresponding production infrastructure and are intentionally not invented.
