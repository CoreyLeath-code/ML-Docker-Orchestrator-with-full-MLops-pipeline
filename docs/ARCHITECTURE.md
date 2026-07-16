# Architecture

```mermaid
flowchart LR
  C[Client] --> G[Gateway TLS identity rate limits]
  G --> A[FastAPI orchestrator]
  A --> V[Finite schema and batch validation]
  V --> D[Deterministic reference backend]
  V --> R[Optional MLflow alias backend]
  A --> P[Prometheus metrics and logs]
  T[Seeded training] --> M[MLflow tracking]
  M --> R
  A --> K[Docker and Kubernetes]
```

The deterministic backend makes development, CI, health checks, and rollback independently
reproducible. Production can opt into the MLflow alias backend after its registry, artifact,
credentials, network policy, and availability SLO are provisioned.
