# NGINX Smoke Test

## 1. Title & Purpose

NGINX on HX-7 is an HX development/test UI rendering utility. This smoke test validates that NGINX can proxy one temporary development endpoint to a separate private-IP upstream and return the exact upstream content.

**Scope:** HX-7 development proxy function only. This does not establish NGINX as the HX Eco-System front door.

## 2. Prerequisites

- NGINX is installed natively and running on HX-7.
- `nginx -t` passes before the test.
- A temporary test runner other than HX-7 can host a simple upstream on a private HX network IP.
- Set that private IP on HX-7:

```bash
export UPSTREAM_IP="<approved-test-runner-private-ip>"
```

- TCP port `18080` on the temporary upstream and `18017` on HX-7 are unused for the test.
- Do not use `127.0.0.1` or `localhost` as the NGINX `proxy_pass` target.
- No firewall or network-policy changes are part of this smoke test.

## 3. Test Steps

1. On the temporary test runner, save as `nginx_smoke_upstream.py`:

```python
from http.server import BaseHTTPRequestHandler, HTTPServer

TOKEN = b"HX-NGINX-SMOKE-9271\n"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/hx-smoke":
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(TOKEN)))
        self.end_headers()
        self.wfile.write(TOKEN)

    def log_message(self, format, *args):
        pass

HTTPServer(("0.0.0.0", 18080), Handler).serve_forever()
```

2. Start it:

```bash
python3 nginx_smoke_upstream.py
```

3. From HX-7, prove the upstream directly:

```bash
curl -fsS "http://${UPSTREAM_IP}:18080/hx-smoke"
```

Expected: `HX-NGINX-SMOKE-9271`.

4. On HX-7, create a temporary NGINX config:

```bash
: "${UPSTREAM_IP:?set UPSTREAM_IP first}"

sudo tee /etc/nginx/conf.d/hx-smoke.conf >/dev/null <<EOF
server {
    listen 18017;
    server_name _;

    location /hx-smoke {
        proxy_pass http://${UPSTREAM_IP}:18080/hx-smoke;
    }
}
EOF

sudo nginx -t
sudo systemctl reload nginx
```

5. Call NGINX:

```bash
curl -fsS "http://192.168.50.207:18017/hx-smoke"
```

6. Confirm the exact known-answer token is returned and record the upstream IP, NGINX version, configuration test result, and direct-vs-proxied output.

## 4. Sample Data

```text
Upstream path: /hx-smoke
Known answer:  HX-NGINX-SMOKE-9271
NGINX port:    18017
Upstream port: 18080
```

## 5. Expected Output

Both direct upstream and NGINX-proxied requests return:

```text
HX-NGINX-SMOKE-9271
```

`nginx -t` must also report successful configuration syntax.

Pass means HX-7 receives the request, proxies it to the separate private-IP upstream, and returns the unchanged known-answer payload.

## 6. Cleanup / Teardown

On HX-7:

```bash
sudo rm -f /etc/nginx/conf.d/hx-smoke.conf
sudo nginx -t
sudo systemctl reload nginx
```

On the temporary test runner, stop `nginx_smoke_upstream.py` and remove the disposable test file/workspace.

Confirm HX-7 port `18017` and the temporary upstream port are no longer part of the smoke test.

**Do not add permanent ecosystem routes, DNS changes, firewall restrictions, TLS configuration, or localhost proxy targets as part of this test.**

## Evidence

Retain the run through the standard bundle described in
`docs/05-evidence/README.md`: manifest, result, cleanup proof, and the
supporting capture of the temporary development proxy response.

Record the NGINX version, the temporary server block used, the private
upstream it proxied, the known-answer response, and the confirmation that the
temporary configuration was removed and NGINX reloaded cleanly afterwards.
