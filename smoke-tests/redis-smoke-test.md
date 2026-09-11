# Redis Smoke Test

## 1. Title & Purpose

Redis is the HX in-memory/state service on HX-9. This smoke test validates that Redis is reachable and can complete a deterministic PING, SET, GET, DELETE, and cleanup cycle.

**Scope:** Redis core function only. Redis MCP is validated separately with `mcp-companion-smoke-test.md`.

## 2. Prerequisites

- Redis is installed natively and running on HX-9.
- `redis-cli` is installed on the test runner.
- The accepted Redis endpoint is reachable.
- Set the connection URL using the accepted HX credential method. Example without embedded credentials:

```bash
export REDIS_URL="redis://192.168.50.209:6379"
```

- If authentication is required, supply it through the accepted environment/credential mechanism; do not expose it in evidence.
- The key `hx:smoke:redis:9271` must not be used by permanent application data.
- No Docker, Podman, Kubernetes, or persistent test dataset is required.

## 3. Test Steps

Run:

```bash
set -euo pipefail

: "${REDIS_URL:=redis://192.168.50.209:6379}"
KEY="hx:smoke:redis:9271"
VALUE="HX-REDIS-SMOKE-9271"

[ "$(redis-cli -u "$REDIS_URL" --raw PING)" = "PONG" ]
[ "$(redis-cli -u "$REDIS_URL" --raw SET "$KEY" "$VALUE" EX 120)" = "OK" ]
[ "$(redis-cli -u "$REDIS_URL" --raw GET "$KEY")" = "$VALUE" ]
[ "$(redis-cli -u "$REDIS_URL" --raw DEL "$KEY")" = "1" ]
[ "$(redis-cli -u "$REDIS_URL" --raw EXISTS "$KEY")" = "0" ]

echo "REDIS_SMOKE_PASS token=$VALUE"
echo "REDIS_SMOKE_CLEANUP_PASS"
```

Record Redis version, target endpoint, execution timestamp, and console
output. Do not capture credentials.

## 4. Sample Data

```text
Key:   hx:smoke:redis:9271
Value: HX-REDIS-SMOKE-9271
TTL:   120 seconds safety expiration
```

## 5. Expected Output

A passing run ends with:

```text
REDIS_SMOKE_PASS token=HX-REDIS-SMOKE-9271
REDIS_SMOKE_CLEANUP_PASS
```

Pass means Redis returns `PONG`, accepts the key, returns the exact value, deletes the key, and confirms the key no longer exists.

## 6. Cleanup / Teardown

The script deletes the smoke-test key. The 120-second TTL is a second safety mechanism if execution is interrupted.

Manual cleanup if required:

```bash
redis-cli -u "$REDIS_URL" DEL "hx:smoke:redis:9271"
```

Confirm cleanup:

```bash
redis-cli -u "$REDIS_URL" EXISTS "hx:smoke:redis:9271"
```

Expected result: `0`.

**Do not run FLUSHDB, FLUSHALL, or delete unrelated HX keys.**

## Evidence

Retain the run through the standard bundle described in
`docs/05-evidence/README.md`: manifest, result, cleanup proof, and the
supporting capture of the `REDIS_SMOKE_PASS` and `REDIS_SMOKE_CLEANUP_PASS` lines.

Record the Redis version, the endpoint used, the `PONG` reply, the known-answer token `HX-REDIS-SMOKE-9271` as written and read back, and confirmation that `hx:smoke:redis:9271` no longer exists.
