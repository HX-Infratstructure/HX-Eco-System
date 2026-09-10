#!/usr/bin/env bash
set -u

REDIS_HOST="${REDIS_HOST:-127.0.0.1}"
REDIS_PORT="${REDIS_PORT:-6379}"

section() {
  printf '\n===== %s =====\n' "$1"
}

run() {
  printf '\n$ %s\n' "$*"
  "$@" 2>&1 || true
}

rcli() {
  redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" "$@"
}

section "HX REDIS READ-ONLY AUDIT"
printf 'timestamp_utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
printf 'redis_host=%s\n' "$REDIS_HOST"
printf 'redis_port=%s\n' "$REDIS_PORT"

section "HOST"
run hostnamectl
run hostname -f
run ip -br addr
run ip route
run findmnt /srv/data
run df -hT / /srv/data
run free -h

section "SYSTEMD"
run systemctl --failed --no-pager
run systemctl is-enabled redis-server
run systemctl is-active redis-server
run systemctl status redis-server --no-pager -l

section "PACKAGES AND BINARIES"
run command -v redis-server
run command -v redis-cli
run redis-server --version
run redis-cli --version
run apt-cache policy redis redis-server redis-tools

if ! command -v redis-cli >/dev/null 2>&1; then
  section "REDIS CLIENT UNAVAILABLE"
  printf 'redis-cli not found; runtime checks skipped.\n'
  exit 0
fi

section "CONNECTIVITY AND IDENTITY"
run rcli PING
run rcli ACL WHOAMI
run rcli ACL USERS

section "SERVER"
run rcli INFO server
run rcli INFO clients
run rcli INFO memory
run rcli INFO stats
run rcli INFO persistence
run rcli INFO keyspace
run rcli INFO replication

section "MODULES AND COMMAND CAPABILITY"
run rcli MODULE LIST
run rcli COMMAND INFO BACKUP
run rcli COMMAND INFO HIMPORT
run rcli COMMAND INFO LMOVEM
run rcli COMMAND INFO SUNIONCARD
run rcli COMMAND INFO INCREX
run rcli COMMAND INFO XNACK
run rcli COMMAND INFO FT.ALIASLIST

section "DIAGNOSTICS"
run rcli SLOWLOG LEN
run rcli LATENCY LATEST
run rcli DBSIZE

section "LISTENERS"
run ss -lntp

section "AUDIT COMPLETE"
printf 'No Redis mutation commands are issued by this script.\n'
