# Security policy

Use GitHub private vulnerability reporting; do not disclose vulnerabilities publicly. Include the
affected commit, reproduction, impact, and minimal proof of concept. Maintainers target
acknowledgement within five business days.

CI runs CodeQL, Bandit, dependency, secret, configuration, source, and image scans and emits an SPDX
SBOM. Internet deployments require TLS, authentication/authorization, and rate limiting at a
gateway. MLflow credentials and artifacts must be platform-injected and never committed.
