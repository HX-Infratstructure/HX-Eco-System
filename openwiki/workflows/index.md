# Files

- [Build-Day Flow](build-day-flow.md) - The six-step build-day flow every server follows, from preflight through reboot-persistence validation and record closure, including the dependency-driven build order and what stops you per host.
- [Runbook Delegation Pattern](runbook-delegation-pattern.md) - How per-host runbook wrappers delegate to the shared common/ library, the hx-app-lib.sh helpers, the pinned values in hx-base.env, and the host guard that prevents cross-host damage.
- [Smoke-Test Execution Workflow](smoke-test-execution.md) - The end-to-end smoke-test workflow — CentCom activation at A5, pre-CentCom operator-station runs, the hx-smoke-runner toolset, remote execution rules, proof-chain promotion, and cleanup/retention.
