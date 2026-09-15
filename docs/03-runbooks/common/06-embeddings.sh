#!/usr/bin/env bash
# Install the HX-4 shared embedding plane into the Ollama installed by block 3.
#
# D-005: BGE-M3 is the primary/default HX embedding model, Nomic Embed Text
# v1.5 is the alternate/benchmark. Never mix embedding identities in one Qdrant
# collection; a model change means a new collection and re-embedding.
#
# Runtime : Ollama, already present. Only the cross-encoder reranker needs
#           Infinity, because Ollama does not serve cross-encoders.
#
# Usage: ./06-embeddings.sh hx-4
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./hx-base.env
. "$SCRIPT_DIR/hx-base.env"

[ $# -eq 1 ] || { echo "Usage: ${0##*/} <hx-host>   (hx-4)" >&2; exit 2; }
hx_require_host "$1"

for v in HX_EMBED_PRIMARY_MODEL HX_EMBED_ALT_MODEL; do
  [ -n "${!v:-}" ] || {
    echo "STOP: $v is not set in hx-base.env." >&2
    echo "      Record the verified upstream reference before build day." >&2
    exit 30
  }
done

systemctl is-active ollama >/dev/null || {
  echo "STOP: ollama is not active. Run 03-storage-ollama.sh first." >&2
  exit 23
}

# Pull a model, alias it, and prove its embedding identity by dimension.
# D-005 turns on embedding identity, so the dimension is the known answer: a
# wrong model answers with a vector of the wrong length, and that is the one
# failure a health check would never catch.
hx_embed_install() {
  local ref="$1" alias="$2" want_dim="$3" label="$4"
  echo "=== $label ==="
  echo "  source $ref"
  echo "  alias  $alias"
  ollama pull "$ref"
  ollama cp "$ref" "$alias"
  hx_ollama_provenance "$alias" "$ref"

  local dim
  dim="$(curl -fsS "http://127.0.0.1:11434/api/embed" \
          -d "{\"model\":\"${alias}\",\"input\":\"hx embedding identity probe\"}" \
        | python3 -c 'import json,sys; print(len(json.load(sys.stdin)["embeddings"][0]))')"

  [ "$dim" = "$want_dim" ] || {
    echo "STOP: $alias returned $dim dimensions, expected $want_dim." >&2
    echo "      The pinned reference does not identify the model D-005 names." >&2
    exit 25
  }
  echo "  dimensions $dim — matches the D-005 identity"
}

hx_embed_install "$HX_EMBED_PRIMARY_MODEL" "$HX_EMBED_PRIMARY_ALIAS" \
                 "$HX_EMBED_PRIMARY_DIM" "primary embedding model (BGE-M3)"
hx_embed_install "$HX_EMBED_ALT_MODEL" "$HX_EMBED_ALT_ALIAS" \
                 "$HX_EMBED_ALT_DIM" "alternate embedding model (Nomic v1.5)"

echo "--- LAN API ---"
curl -fsS "http://${HX_IP}:11434/api/tags" >/dev/null

cat <<SUMMARY

Shared embedding plane installed on $HX_HOST.
  endpoint  http://${HX_IP}:11434/api/embed
  primary   $HX_EMBED_PRIMARY_ALIAS  (${HX_EMBED_PRIMARY_DIM}d) — $HX_EMBED_PRIMARY_MODEL
  alternate $HX_EMBED_ALT_ALIAS  (${HX_EMBED_ALT_DIM}d) — $HX_EMBED_ALT_MODEL

Reboot-persistence check (run after the host comes back):
  systemctl is-active ollama && ollama list | grep hx-embed

D-005 reminder: one embedding identity per Qdrant collection. Changing the
model means a new collection and re-embedding, never a mixed collection.

Then record both models in docs/02-server-records/HX-4.md, template section 6,
all five fields each. Capture the resolved blob hashes now:
  ollama show --modelfile $HX_EMBED_PRIMARY_ALIAS
  ollama show --modelfile $HX_EMBED_ALT_ALIAS
SUMMARY
