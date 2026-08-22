# L6 Engineering Audit — ML Docker Orchestrator

**Repository:** `CoreyLeath-code/ML-Docker-Orchestrator-with-full-MLops-pipeline`  
**Audit type:** evidence-first staff-level promotion review  
**Audit date:** 2026-08-22  
**Primary rule:** implementation and reproducible evidence outrank architecture breadth or marketing language.

## Executive assessment

The repository has meaningful MLOps breadth: a FastAPI serving path, MLflow model loading and training, Prometheus instrumentation, Docker and Compose assets, Kubernetes manifests, Terraform/Ansible foundations, CI quality checks, security scanning, semantic release automation, GHCR publication, and a Streamlit systems demonstration.

The current codebase is best described as a **production-shaped MLOps reference platform**. It does not yet provide the evidence required to call itself a production-grade distributed orchestrator or an L6-complete system.

The largest issue is not lack of technology. It is **claim-to-code alignment**. Several visible claims previously described live orchestration, high availability, chaos recovery, throughput, scheduler latency, and replica counts that are not produced by the implementation. The Streamlit dashboard generates or stores those values locally in session state and should therefore be treated as a simulation surface.

### Promotion verdict

| Area | Current status | L6 interpretation |
|---|---|---|
| API contract | solid foundation | bounded inputs and sanitized failures are real |
| Model lifecycle | partial | MLflow integration exists; promotion/governance is incomplete |
| Testing | partial | focused unit/API tests exist; integration/system evidence is thin |
| Observability | partial | Prometheus metrics exist; no measured SLO/benchmark evidence |
| Containerization | partial | functional image/Compose assets; runtime hardening remains |
| Kubernetes | architecture-complete, validation-light | manifests exist; live-cluster CI evidence does not |
| Security | useful baseline | Trivy/CodeQL/dependency controls exist; supply-chain policy is incomplete |
| Release engineering | partial | semantic release + GHCR tag build exist as separate flows |
| Reproducibility | partial | synthetic training is seeded; evidence artifacts are not persisted |
| Orchestration | major gap | no real Docker/Kubernetes reconciliation controller is implemented |
| Failure recovery | major gap | dashboard failure actions are simulated, not runtime fault injection |
| Model evaluation/governance | major gap | evaluation module is explicitly a placeholder |

---

## 1. Critical regret analysis

### 1.1 The repository name and prior README overstate orchestration semantics

There is no controller loop that watches desired state, compares it with observed Docker/Kubernetes state, and performs reconciliation through a Docker Engine or Kubernetes API. The canonical `src/orchestrator` package is primarily an ML inference service and model-loading layer.

**Risk:** a senior reviewer can interpret the gap as architecture inflation rather than ambitious scaffolding.

**Required correction:** describe the current system as an MLOps reference platform unless a real reconciliation controller is implemented and tested.

### 1.2 The Streamlit control plane is a simulation

`platform_monitor.py` stores worker state in `st.session_state`, mutates CPU/memory with random values, displays a hard-coded throughput value and replica count, and changes node status when buttons are pressed. The "kill" and "re-provision" paths do not call Docker, Kubernetes, Ansible, or a live telemetry backend.

**Do not claim:**

- measured scheduler latency;
- 84.2k events/sec telemetry throughput;
- 12 active containers;
- live Prometheus scrape state;
- real SIGKILL injection;
- real Ansible/IaC convergence;
- validated automatic cluster recovery.

**Defensible claim:** the UI demonstrates how an operator-facing control plane could visualize pipeline and failure states.

### 1.3 The canonical and legacy serving paths diverge

The repository has both:

- `src/orchestrator/api.py`, which loads an MLflow `pyfunc` model; and
- `app/main.py`, which recreates a PyTorch network and loads `model/model.pth`.

These paths have different model assumptions, request schemas, artifact locations, and operational behavior.

**L6 concern:** two serving contracts create architecture drift, duplicated ownership, and unclear release semantics.

**Promotion requirement:** choose a canonical serving path and either delete, archive, or explicitly label the other as legacy/demo-only.

### 1.4 Training evidence is reproducible but not decision-grade

The canonical training path uses a fixed RNG seed, 500 synthetic observations, three features, a fixed 80/20 split, linear regression, and RMSE logging. That is useful deterministic scaffolding.

It does **not** establish:

- real-world model quality;
- robustness under distribution shift;
- calibration;
- subgroup/fairness behavior;
- drift tolerance;
- production promotion criteria.

`src/orchestrator/pipeline/evaluate.py` explicitly remains a placeholder.

### 1.5 Coverage policy is stronger than the published evidence

`pyproject.toml` configures `fail_under = 80`, and CI runs `pytest --cov=src`. That is a real policy control.

The repository does not currently commit a coverage artifact or exact measured percentage tied to a commit. A static `80% coverage` badge can therefore be misread as a measured result instead of a threshold.

**Recommended wording:** "coverage gate ≥80%" until CI publishes a measured report.

### 1.6 CI is useful but not full-repository quality proof

CI runs Ruff only against changed Python files, then Mypy and Pytest. This is a pragmatic change gate, not proof that all existing Python source is always Ruff-clean.

Mypy is not configured in strict mode.

**Promotion requirement:** add a periodic/full-repository quality workflow or make the primary gate cover the entire supported package.

### 1.7 Deployment manifests are stronger than deployment evidence

The Kubernetes surface includes replicas, health probes, resource limits, HPA, NetworkPolicy, Service, ConfigMap, Secret example, and ServiceMonitor. That is useful architecture evidence.

However:

- the Deployment still contains a placeholder image reference;
- no ephemeral Kubernetes cluster is provisioned in CI;
- there is no rollout/rollback test;
- no pod-disruption or dependency-failure scenario is exercised.

### 1.8 Container hardening is incomplete

The canonical Dockerfile uses a slim Python base and a focused runtime command, but it currently:

- runs as root;
- has no Docker `HEALTHCHECK`;
- installs floating lower-bounded dependencies rather than a reproducible lock;
- does not emit or verify an image SBOM/provenance record in the tag-publish workflow.

### 1.9 Security controls exist, but the release boundary is incomplete

Positive controls include Trivy, CodeQL, dependency review, and Dependabot.

Remaining concerns:

- Trivy action is referenced by `@master` rather than an immutable version/SHA;
- security workflow execution is not the same as an explicit remediation SLA;
- release images are not tied to signed attestations in the current CD path;
- no release SBOM is retained as a release artifact;
- duplicate CodeQL execution should be reviewed for intentionality.

### 1.10 Release automation is split across two contracts

`release.yml` performs semantic release on `main`, while `cd.yml` publishes a GHCR image only after a semantic tag is pushed.

That can work, but L6 release evidence should make one immutable version traceable across:

- Git tag;
- source commit;
- release notes;
- source archive/checksum;
- container digest;
- SBOM/provenance;
- deployment manifest version.

---

## 2. Verified implementation strengths

### API and failure boundaries

The canonical API provides `/health`, `/metrics`, and `/predict`. Prediction batches are bounded to 1–1,000 records. Model/backend errors are logged internally and returned to clients as a sanitized `503` response.

The test suite includes explicit coverage for sanitized backend failures and rejection of empty batches.

### Model loading

The canonical runtime uses `mlflow.pyfunc.load_model()` and caches the loaded model. The model URI is built from configured registry name and stage.

This is a real model-serving integration boundary, even though live Registry integration tests are still missing.

### Training reproducibility

The canonical training module fixes both data generation and split randomness at seed `42`, logs RMSE to MLflow, logs the model artifact, and registers the model.

This is a good foundation for a stronger evidence pipeline.

### Observability

The canonical API exports a labeled request counter and request-latency histogram through Prometheus exposition format.

The metrics are implementation evidence; latency claims must still come from a controlled benchmark.

### Deployment shape

The repository demonstrates multiple production-oriented deployment concepts:

- Docker API image;
- local MLflow + API Compose topology;
- Kubernetes probes and resource controls;
- HPA and NetworkPolicy;
- Prometheus ServiceMonitor;
- Terraform and Ansible foundations.

### Security and maintenance

Automated security/dependency controls materially improve the repository over a typical portfolio demo. Dependabot, dependency review, Trivy, and CodeQL show maintenance discipline even though release hardening remains incomplete.

---

## 3. Evidence classification

### Tier A — directly implemented and inspectable

- FastAPI health/metrics/predict routes
- bounded batch validation
- sanitized 503 failure contract
- Prometheus request/latency metrics
- cached MLflow model load
- seeded synthetic training
- RMSE logging
- Docker image definition
- Docker Compose MLflow/API topology
- Kubernetes manifests
- CI, Trivy, CodeQL, dependency-review workflows
- semantic-release workflow
- GHCR tag-build workflow

### Tier B — architecture/scaffolding, not operational proof

- Terraform provisioning intent
- Ansible provisioning intent
- Grafana/Prometheus configuration assets
- HPA behavior
- network isolation effectiveness
- model Registry promotion process
- rollback readiness

### Tier C — simulation/demo only

- Streamlit worker health state
- Streamlit CPU/memory telemetry
- Streamlit scheduler latency
- Streamlit throughput number
- Streamlit replica count
- Streamlit kill-container action
- Streamlit cluster re-provision action
- Streamlit pipeline state transitions

### Tier D — not yet implemented

- evaluation/drift/fairness gates
- real control-loop reconciliation
- live chaos/fault injection
- measured API benchmark artifact
- load/soak test evidence
- live Kubernetes integration tests
- tested rollback
- model/data card tied to immutable artifacts
- release SBOM/provenance/signature chain

---

## 4. Reproducibility contract

A credible L6 evidence run should record at least:

```text
commit_sha
python_version
os / runner image
cpu architecture
container image digest
random seeds
dataset or generator fingerprint
training configuration
model artifact URI + digest
test count + pass/fail
coverage percentage
benchmark warmup count
benchmark sample count
concurrency
P50/P95/P99 latency
throughput
peak memory / container resources
security scanner versions
release tag
```

### Current deterministic training protocol

```text
RNG seed:        42
Rows:            500
Features:        3
Test fraction:   0.20
Split seed:      42
Estimator:       sklearn LinearRegression
Metric:          RMSE
Tracker:         MLflow
Registry target: MODEL_NAME setting
```

This protocol should be retained as a smoke/reproducibility baseline even after real data is added.

---

## 5. L6 promotion plan

### Phase 1 — claim and architecture alignment

- Treat `src/orchestrator` as the canonical runtime.
- Label or remove the legacy `app/` and `model/` path.
- Keep the Streamlit control plane explicitly labeled as simulated.
- Remove unmeasured performance/SLO language from docs and UI.
- Consolidate duplicate project-structure and changelog files.

**Exit criterion:** every README capability maps to a concrete file, test, workflow, or explicitly labeled demo/scaffold.

### Phase 2 — integration evidence

Add automated tests that start real dependencies and verify:

- MLflow tracking and model registration;
- model loading from the configured Registry reference;
- successful `/predict` response from a registered model;
- failure behavior when MLflow is unavailable;
- Docker image health after build;
- Docker Compose MLflow/API communication.

**Exit criterion:** the model-serving path is proven end to end without mocks.

### Phase 3 — real orchestration or narrower product contract

Choose one:

**A. Implement orchestration:**

- define desired-state resource schema;
- read real Docker/Kubernetes state;
- implement reconciliation loop;
- add idempotency tests;
- persist operation state;
- implement retries/backoff/timeouts;
- expose controller metrics;
- test partial failure and convergence.

**B. Keep the current platform scope:**

Rename/describe the system as an MLOps deployment reference platform rather than a custom orchestrator.

**Exit criterion:** the repository name/story no longer implies capabilities that the runtime does not provide.

### Phase 4 — model governance

- add a versioned public or real dataset;
- record dataset hash and split metadata;
- add baseline comparison;
- implement evaluation gates;
- add drift and schema validation;
- define promotion/rejection thresholds;
- create a model card tied to exact MLflow artifacts;
- use model aliases or another explicit immutable promotion mechanism.

**Exit criterion:** a reviewer can reproduce why one model version was promoted over another.

### Phase 5 — reliability and performance

- build a deterministic API benchmark harness;
- report P50/P95/P99 and throughput;
- add concurrency and soak tests;
- measure cold/warm model-load behavior;
- test corrupt artifacts and registry outages;
- separate liveness from readiness;
- test graceful shutdown and rollout behavior.

**Exit criterion:** published runtime numbers are generated by committed tooling and tied to a commit/environment.

### Phase 6 — supply chain and deployment proof

- run containers as non-root;
- add Docker health check;
- pin GitHub Actions to trusted immutable versions/SHAs where practical;
- generate CycloneDX/SPDX SBOM;
- emit provenance attestations;
- publish immutable image digests;
- validate manifests on an ephemeral cluster;
- test rollout and rollback;
- define severity-based vulnerability policy and remediation SLAs.

**Exit criterion:** one release tag has traceable source, tests, security evidence, artifact digest, SBOM/provenance, and deploy/rollback evidence.

---

## 6. Recommended benchmark design

Do not add latency badges until this protocol exists in the repository.

Suggested API benchmark:

1. Build the release image.
2. Start local MLflow with a fixed registered test model.
3. Warm the API with at least 50 prediction calls.
4. Execute at least 1,000 measured calls at fixed payload sizes.
5. Repeat across several concurrency levels.
6. Record P50/P95/P99 latency, throughput, error rate, CPU, RSS/container memory, runner metadata, model URI, image digest, and commit SHA.
7. Save results as versioned JSON.
8. Validate JSON schema in CI before publishing README metrics.

Suggested reliability matrix:

| Fault | Expected behavior |
|---|---|
| MLflow unavailable at cold load | readiness fails or prediction returns bounded 503 |
| model artifact corrupt | no process crash; bounded error + metric/log |
| invalid payload | deterministic 422 |
| empty batch | deterministic 422 |
| oversized batch | deterministic 422 |
| pod termination | graceful shutdown within configured deadline |
| rolling update | readiness prevents early traffic |
| dependency recovery | service returns to ready without manual restart where designed |

---

## 7. Staff-level acceptance checklist

A future claim of L6-level implementation should be supported by all of the following:

- [ ] README contains no unmeasured performance or availability claims.
- [ ] One canonical serving architecture exists.
- [ ] Real MLflow integration is tested in CI.
- [ ] Docker image is built and health-tested in CI.
- [ ] Kubernetes manifests are validated against a live ephemeral cluster.
- [ ] Liveness and readiness semantics are explicit.
- [ ] Performance evidence is committed as machine-readable data.
- [ ] Model dataset/split/artifact hashes are recorded.
- [ ] Evaluation and promotion gates are implemented.
- [ ] Failure scenarios and recovery expectations are tested.
- [ ] Release artifacts include immutable digests and SBOM/provenance.
- [ ] Vulnerability policy distinguishes report-only from blocking findings.
- [ ] Rollback is exercised, not only documented.
- [ ] If "orchestrator" remains a product claim, a real reconciliation controller is implemented and tested.

---

## Bottom line

The repository has enough real engineering surface to be a strong portfolio project without inflated language. Its most compelling current story is:

> **A container-first MLOps reference platform with MLflow-backed model serving, observable FastAPI inference, Kubernetes deployment assets, CI/security automation, and a simulated operator control-plane demo.**

Moving from that foundation to an L6-caliber system is primarily an **evidence, integration, reliability, and control-plane correctness** problem—not a need to add more buzzwords or more unrelated technologies.
