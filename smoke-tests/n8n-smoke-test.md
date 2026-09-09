# n8n Smoke Test

## 1. Title & Purpose

n8n is the HX workflow automation component on HX-14. This smoke test validates that the native n8n instance can create, execute, save, reopen, and delete one deterministic workflow without external credentials or services.

**Scope:** n8n core workflow/UI function only. n8n MCP is validated separately with `mcp-companion-smoke-test.md`.

## 2. Prerequisites

- n8n is installed natively and running on HX-14.
- The direct n8n LAN UI is reachable without NGINX.
- An authorized HX test user can create and delete a workflow.
- Use the accepted direct URL, for example:

```text
http://192.168.50.214:5678
```

- No external credential, webhook, database integration, production workflow, or container is required.

## 3. Test Steps

1. Open the direct HX-14 n8n UI.
2. Create a workflow named:

```text
HX-N8N-SMOKE-9271
```

3. Add a **Manual Trigger** node.
4. Connect it to an **Edit Fields (Set)** node.
5. In Edit Fields, set fixed values:

```text
token  = HX-N8N-SMOKE-9271
status = PASS
```

6. Execute the workflow manually.
7. Confirm the Edit Fields node output contains the exact two values.
8. Save the workflow.
9. Leave the workflow, reopen `HX-N8N-SMOKE-9271`, and execute it one more time.
10. Confirm the same deterministic output is returned.
11. Record n8n version, direct URL, workflow name, execution timestamp, and output evidence.
12. Delete the smoke-test workflow.

## 4. Sample Data

```json
{
  "token": "HX-N8N-SMOKE-9271",
  "status": "PASS"
}
```

No external input is required. The Manual Trigger starts the test and Edit Fields creates the known-answer payload.

## 5. Expected Output

The final node output must contain:

```json
{
  "token": "HX-N8N-SMOKE-9271",
  "status": "PASS"
}
```

Pass means:

- the direct n8n UI loads;
- the workflow can be created and manually executed;
- the expected output is produced;
- the workflow can be saved and reopened;
- a second execution produces the same result;
- the smoke workflow is deleted after evidence capture.

## 6. Cleanup / Teardown

Delete only the workflow named `HX-N8N-SMOKE-9271` and confirm it is no longer present.

Do not delete unrelated workflows, credentials, users, projects, or n8n configuration.

**No production integration and no container is created by this test.**
