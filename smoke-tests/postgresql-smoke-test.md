# PostgreSQL Smoke Test

## 1. Title & Purpose

PostgreSQL is the HX relational database on HX-9. This smoke test validates that the accepted PostgreSQL instance is reachable and can create, write, read, and automatically remove a disposable temporary table.

**Scope:** PostgreSQL core database function only. PostgreSQL MCP is validated separately with `mcp-companion-smoke-test.md`.

## 2. Prerequisites

- PostgreSQL is installed natively and running on HX-9.
- The test runner can reach the accepted PostgreSQL listener.
- `psql` is installed on the test runner.
- An authorized smoke-test database/user is available.
- Supply connection settings using the accepted HX credential method. Do not print passwords in evidence.
- Example non-secret settings:

```bash
export PGHOST="192.168.50.209"
export PGPORT="5432"
export PGDATABASE="<accepted-test-database>"
export PGUSER="<authorized-test-user>"
```

- No Docker, Podman, Kubernetes, permanent schema, or production data is required.

## 3. Test Steps

1. Run the following in one `psql` session:

```bash
psql -v ON_ERROR_STOP=1 <<'SQL'
CREATE TEMP TABLE hx_smoke_postgresql (
    id integer PRIMARY KEY,
    token text NOT NULL
);

INSERT INTO hx_smoke_postgresql (id, token)
VALUES (1, 'HX-POSTGRES-SMOKE-9271');

DO $$
DECLARE
    v text;
BEGIN
    SELECT token INTO v
    FROM hx_smoke_postgresql
    WHERE id = 1;

    IF v <> 'HX-POSTGRES-SMOKE-9271' THEN
        RAISE EXCEPTION 'unexpected token: %', v;
    END IF;
END $$;

SELECT 'POSTGRES_SMOKE_PASS token=HX-POSTGRES-SMOKE-9271' AS result;
SQL
```

2. Open a new `psql` session and verify the temporary table no longer exists:

```bash
psql -v ON_ERROR_STOP=1 -Atc "SELECT to_regclass('pg_temp.hx_smoke_postgresql') IS NULL;"
```

3. Record PostgreSQL version, host/port, database name, execution timestamp, and console output. Do not capture credentials.

## 4. Sample Data

```text
Table: hx_smoke_postgresql
id: 1
token: HX-POSTGRES-SMOKE-9271
```

## 5. Expected Output

The first command returns a row containing:

```text
POSTGRES_SMOKE_PASS token=HX-POSTGRES-SMOKE-9271
```

The second command returns:

```text
t
```

Pass means the connection succeeds, the temporary table is created, the exact token is written and read, and the table disappears when the original session closes.

## 6. Cleanup / Teardown

No permanent table is created. PostgreSQL temporary tables are session-scoped and disappear when the session ends.

If the test session is still open, terminate it normally. Remove any disposable local test files after evidence capture.

**Do not create or drop persistent HX schemas/tables as part of this smoke test.**
