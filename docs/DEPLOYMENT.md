# Deployment and rollback

Build and verify:

```bash
docker compose up --build
curl --fail http://127.0.0.1:8080/ready
kubectl apply -f network-policy.yaml -f deployment.yaml -f service.yaml
```

Promote only a scanned, signed immutable digest with retained SPDX SBOM and quality evidence.
Validate environment, secret references, model backend, registry connectivity when selected,
resources, logs, metrics, probes, API, and alert ownership in staging. No database is used by the
reference backend.

Rollback using `kubectl rollout undo deployment/ml-docker-orchestrator` or the prior digest, then
verify health, readiness, errors, p95 latency, and prediction success.
