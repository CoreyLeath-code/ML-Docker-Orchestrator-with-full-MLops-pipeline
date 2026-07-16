# Benchmark report

Each CI run produces `latest.json` bound to the commit and runner. It contains the latency
distribution, throughput, success rate, peak Python allocation, synthetic regression RMSE/MAE/R2,
parameters, payload hash, environment, and timestamp. Hardware-dependent values are not copied into
this document. Compare artifacts only when schema and provenance are compatible.
