# NGINX Smoke Test

## 1. Title & Purpose

NGINX on HX-7 is an HX development/test UI rendering utility. This smoke test validates that NGINX can proxy one temporary development endpoint to a separate private-IP upstream and return the exact upstream content.

**Scope:** HX-7 development proxy function only. This does not establish NGINX as the HX Eco-System front door.

## 2. Prerequisites

- NGINX is installed natively and running on HX-7 as unit `hx-nginx`.
- `nginx -t` passes before the test.
- The upstream is an **already-proven HX endpoint**, not a service created for
  this test. Use HX-4's Ollama, which proof step `A1` has already passed:

```bash
export UPSTREAM_HOST="hx-4"
export UPSTREAM_IP="192.168.50.204"
export UPSTREAM_PORT="11434"
```

- Record the host, IP and port actually used in the evidence, so the proof is
  reproducible against a named endpoint rather than a disposable one.
- TCP port `18017` on HX-7 is unused for the test.
- Do not use `127.0.0.1` or `localhost` as the NGINX `proxy_pass` target.
- No firewall or network-policy changes are part of this smoke test.
- No new upstream service is started, so nothing has to be torn down off HX-7.

## 3. Test Steps

1. From the runner, prove the upstream answers directly:

```bash
curl -fsS "http://${UPSTREAM_IP}:${UPSTREAM_PORT}/api/version"
```

Expected: `{"version":"0.34.0"}`, which is `HX_OLLAMA_VERSION` as pinned in
`docs/03-runbooks/common/hx-base.env` and proven on HX-4 by step `A1`.

2. On HX-7, create a temporary server block. The configuration directory and
the unit are the ones this host was built with, `--prefix=/srv/nginx` and
`hx-nginx`, not the distribution defaults:

```bash
: "${UPSTREAM_IP:?set UPSTREAM_IP first}"
: "${UPSTREAM_PORT:?set UPSTREAM_PORT first}"

sudo tee /srv/nginx/conf.d/hx-smoke.conf >/dev/null <<EOF
server {
    listen 18017;
    server_name _;

    location /hx-smoke {
        proxy_pass http://${UPSTREAM_IP}:${UPSTREAM_PORT}/api/version;
    }
}
EOF

sudo nginx -t
sudo systemctl reload hx-nginx
```

3. Call NGINX from the runner, which is not HX-7:

```bash
curl -fsS "http://192.168.50.207:18017/hx-smoke"
```

4. Confirm the routed response is byte-identical to the direct one, and record
the upstream host, IP and port, the NGINX version, the configuration test
result, and both the direct and the proxied output.

## 4. Sample Data

```text
Upstream:      hx-4  192.168.50.204:11434  /api/version   (proven by A1)
Known answer:  {"version":"0.34.0"}
NGINX port:    18017
NGINX path:    /hx-smoke
```

## 5. Expected Output

Both the direct upstream request and the NGINX-proxied request return:

```text
{"version":"0.34.0"}
```

`nginx -t` must also report successful configuration syntax.

Pass means HX-7 receives the request, proxies it to a separate private-IP host,
and returns the payload unchanged. The two responses must be byte-identical; a
routed response that merely looks similar is not a pass.

## 6. Cleanup / Teardown

On HX-7:

```bash
sudo rm -f /srv/nginx/conf.d/hx-smoke.conf
sudo nginx -t
sudo systemctl reload hx-nginx
```

Nothing is torn down anywhere else. The upstream is an existing proven service
and is left exactly as it was found; the test starts no service off HX-7.

Confirm HX-7 port `18017` no longer answers.

**Do not add permanent ecosystem routes, DNS changes, firewall restrictions, TLS configuration, or localhost proxy targets as part of this test.**

## Evidence

Retain the run through the standard bundle described in
`docs/05-evidence/README.md`: manifest, result, cleanup proof, and the
supporting capture of the temporary development proxy response.

Record the NGINX version, the temporary server block used, the upstream host,
IP and port it proxied, both the direct and routed responses, and the
confirmation that the temporary configuration was removed and `hx-nginx`
reloaded cleanly afterwards.
