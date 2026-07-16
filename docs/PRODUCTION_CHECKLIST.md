# Production checklist

- [ ] Formatting, lint, static analysis, tests, and >=90% core coverage pass
- [ ] Benchmark is compatible with and reviewed against prior evidence
- [ ] CodeQL, dependency, secret, license, source, and image scans pass
- [ ] SPDX SBOM retained and immutable image signature verified
- [ ] Non-root/read-only runtime, limits, probes, API, and model load pass
- [ ] Environment variables, secrets, registry/database applicability validated
- [ ] Logs and metrics contain no secrets; alerts have owners
- [ ] Prior digest, rollback command, owner, and incident channel recorded
