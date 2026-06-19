# Changelog

All notable changes to this project will be documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-06-18

### Added
- Integrated automated semantic-release execution workflows into the primary CI runner.
- Implemented Prometheus metrics endpoint exporter (`/metrics`) to track worker container CPU consumption under load.

### Changed
- Refactored Docker-Compose multi-stage image orchestration layers to leverage native cached mounts, cutting down pipeline compilation overhead by 35%.

### Fixed
- Resolved a race condition on thread initialization where synchronous API health validation checks caused occasional container target container timeouts.

## [1.0.0] - 2026-01-15

### Added
- Baseline end-to-end MLOps pipeline infrastructure with multi-stage Docker orchestration.
- Automated vulnerability scanning using Trivy and automated SBOM tree generation.
