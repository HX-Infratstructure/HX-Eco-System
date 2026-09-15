#!/usr/bin/env bash
# Install the HX-4 Meta-X generation model into the Ollama installed by block 3.
#
# Runtime : Ollama, already present from 03-storage-ollama.sh. No new runtime.
# Model   : pinned in hx-base.env. The block refuses an unpinned install for
#           the same reason block 3 does: "whatever was current that day" is
#           not a baseline a server record can state.
#
# Usage: ./05-gpt-oss.sh hx-4
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./hx-base.env
. "$SCRIPT_DIR/hx-base.env"

[ $# -eq 1 ] || { echo "Usage: ${0##*/} <hx-host>   (hx-4)" >&2; exit 2; }
hx_require_host "$1"

hx_require_pinned_ref HX_GPT_OSS_MODEL

# Ollama must already be serving; this block adds a model, it does not install
# a runtime.
systemctl is-active ollama >/dev/null || {
  echo "STOP: ollama is not active. Run 03-storage-ollama.sh first." >&2
  exit 23
}

echo "Model : $HX_GPT_OSS_MODEL"
echo "Alias : $HX_GPT_OSS_ALIAS"

ollama pull "$HX_GPT_OSS_MODEL"
ollama cp "$HX_GPT_OSS_MODEL" "$HX_GPT_OSS_ALIAS"
hx_ollama_provenance "$HX_GPT_OSS_ALIAS" "$HX_GPT_OSS_MODEL"

# Known-answer test, not a health check. The service being up proves nothing
# about the model.
echo "--- CLI inference ---"
ollama run "$HX_GPT_OSS_ALIAS" "Reply with exactly: HX-4 META-X PASS"

echo "--- LAN API ---"
curl -fsS "http://${HX_IP}:11434/api/version"; echo
# Capture before matching. `curl | grep -q` lets grep close the pipe at its
# first match; curl is killed by SIGPIPE at 141, and pipefail takes 141 as the
# pipeline's status, so a model that is listed reports exit 24. That is
# HX4-F01, fixed fleet-wide in the base block and not reintroduced here.
TAGS="$(curl -fsS "http://${HX_IP}:11434/api/tags")"
grep -q "${HX_GPT_OSS_ALIAS%%:*}" <<<"$TAGS" || {
  echo "STOP: $HX_GPT_OSS_ALIAS is not listed by the LAN API" >&2
  exit 24
}

cat <<SUMMARY

Meta-X generation model installed on $HX_HOST.
  endpoint  http://${HX_IP}:11434
  alias     $HX_GPT_OSS_ALIAS
  source    $HX_GPT_OSS_MODEL

Reboot-persistence check (run after the host comes back):
  systemctl is-active ollama && ollama list | grep ${HX_GPT_OSS_ALIAS%%:*}

Then record in docs/02-server-records/HX-4.md, template section 6, all five
fields. Capture the resolved blob hash now, while the pull transcript is still
on screen:
  ollama show --modelfile $HX_GPT_OSS_ALIAS
A hash alone does not establish origin, and an origin alone does not establish
what is running. An unknown value is recorded as UNRESOLVED, never omitted.
SUMMARY
