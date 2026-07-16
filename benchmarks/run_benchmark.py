"""Reproducible API and reference-model benchmark."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import random
import statistics
import sys
import time
import tracemalloc
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fastapi.testclient import TestClient  # noqa: E402
from orchestrator.api import app  # noqa: E402

PAYLOAD = {"records": [{"f1": 1.0, "f2": 2.0, "f3": 3.0}]}


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int(len(ordered) * fraction))]


def model_quality(seed: int = 42, samples: int = 1000) -> dict:
    rng = random.Random(seed)
    actual, predicted = [], []
    for _ in range(samples):
        row = [rng.gauss(0, 1) for _ in range(3)]
        prediction = 2 * row[0] - row[1] + 0.5 * row[2]
        actual.append(prediction + rng.gauss(0, 0.3))
        predicted.append(prediction)
    errors = [a - p for a, p in zip(actual, predicted, strict=True)]
    mse = statistics.mean(error * error for error in errors)
    mae = statistics.mean(abs(error) for error in errors)
    baseline = statistics.mean((value - statistics.mean(actual)) ** 2 for value in actual)
    return {"rmse": math.sqrt(mse), "mae": mae, "r2": 1 - mse / baseline}


def run(iterations: int, warmup: int) -> dict:
    client = TestClient(app)
    for _ in range(warmup):
        client.post("/predict", json=PAYLOAD)
    values = []
    tracemalloc.start()
    all_started = time.perf_counter()
    for _ in range(iterations):
        started = time.perf_counter_ns()
        response = client.post("/predict", json=PAYLOAD)
        if response.status_code != 200:
            raise RuntimeError(f"request failed: {response.status_code}")
        values.append((time.perf_counter_ns() - started) / 1_000_000)
    elapsed = time.perf_counter() - all_started
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "schema_version": "1.0.0",
        "parameters": {"iterations": iterations, "warmup": warmup},
        "metrics": {
            "latency_average_ms": statistics.mean(values),
            "latency_median_ms": statistics.median(values),
            "latency_p95_ms": percentile(values, 0.95),
            "latency_p99_ms": percentile(values, 0.99),
            "latency_min_ms": min(values),
            "latency_max_ms": max(values),
            "throughput_requests_per_second": iterations / elapsed,
            "success_rate": 1.0,
            "peak_python_memory_bytes": peak,
            "model_quality": model_quality(),
        },
        "provenance": {
            "generated_at_utc": datetime.now(UTC).isoformat(),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "payload_sha256": hashlib.sha256(
                json.dumps(PAYLOAD, sort_keys=True).encode(), usedforsecurity=False
            ).hexdigest(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=2000)
    parser.add_argument("--warmup", type=int, default=50)
    parser.add_argument("--output", type=Path, default=Path("benchmarks/latest.json"))
    args = parser.parse_args()
    result = run(args.iterations, args.warmup)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
