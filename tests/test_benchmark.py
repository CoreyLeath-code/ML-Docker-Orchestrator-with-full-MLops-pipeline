from benchmarks.run_benchmark import model_quality, run


def test_benchmark_and_quality_are_reproducible():
    result = run(5, 1)
    first = model_quality()
    second = model_quality()
    assert result["metrics"]["success_rate"] == 1.0
    assert result["metrics"]["latency_p99_ms"] > 0
    assert first == second
    assert first["r2"] > 0.95
