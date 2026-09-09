# Native Web UI Companion Smoke Test

## 1. Title & Purpose

Some HX components include a native Web UI as part of BASE PASS. This reusable smoke test validates that the direct application UI is not merely serving a page, but is connected to the accepted backend and can display live application state.

**Scope:** Companion native-UI proof only. Open WebUI and n8n have their own functional smoke tests. NGINX is not part of this path.

## 2. Prerequisites

- The parent component's core service is running and has passed its core smoke test far enough to expose live state.
- The direct native LAN URL is known and reachable from the test browser.
- An authorized test user/credential is available if the UI requires authentication.
- Identify one harmless live-state proof before execution, such as:
  - application/server version or health state;
  - collection/object listing;
  - a dedicated synthetic object named `HX-UI-SMOKE-9271`.
- No NGINX route, external proxy, production data, or container is required.

## 3. Test Steps

1. Open the application's **direct native LAN URL** in the browser.
2. Confirm the correct application identity is rendered.
3. Authenticate only if the accepted application configuration requires it.
4. Navigate to a screen that requires live backend data rather than static HTML.
5. Prove one live-state item:
   - preferred: display a disposable `HX-UI-SMOKE-9271` object created through the parent application's normal API/test flow; or
   - display an application version/health/object listing that proves the UI is reading the backend.
6. Refresh the page and confirm the live-state item remains visible for the duration of the test.
7. Capture the direct URL, application/version, live-state evidence, timestamp, and PASS/FAIL result.
8. Remove any disposable UI smoke object through the parent application's normal cleanup path.

## 4. Sample Data

Preferred disposable object name when the application supports safe test objects:

```text
HX-UI-SMOKE-9271
```

For read-only UIs, use the application's current version/health/listing as the known live-state proof instead.

## 5. Expected Output

Record:

```text
NATIVE_WEB_UI_SMOKE_PASS app=<application> url=<direct-native-url> live_state=<verified-item>
```

Pass means:

- the direct native UI loads;
- the expected application is shown;
- the UI successfully retrieves live backend state;
- the live-state proof remains valid after a refresh;
- any disposable test object is removed afterward.

A static page load by itself is **not** sufficient.

## 6. Cleanup / Teardown

- Delete only the disposable UI smoke object if one was created.
- Log out/close the test browser session as appropriate.
- Remove no permanent application configuration.
- Leave no temporary NGINX/proxy route because NGINX is not used by this test.

**Do not alter production data, network policy, UI branding, or permanent routing as part of this smoke test.**
