"""Prove the fleet can administer a host, from outside that host.

Every other Layer 0/1 control can be checked over an SSH session that has
already authenticated. This one cannot, which is exactly why it is the control
that failed unnoticed: the 2026-09-16 audit found HX-2 and HX-3 reporting
`systemctl is-active ssh` as active the whole time the fleet could not log in
to either of them.

The test is a key-only login from the operator workstation. Passwords are
refused, the host key must already be trusted, and the session must prove both
halves of administration - it is on the right host, and it can act as root
without a password.

Required output:

  hx-N
  KEY+SUDO-PASS

Usage:
  hx-fleet-access hx-5                 # resolve the IP from hx-fleet.tsv
  hx-fleet-access hx-5 --ip 1.2.3.4    # or say it, for a host not yet recorded
  HX_FLEET_KEY=/path/to/key hx-fleet-access hx-5

Exit status:
  0   the host is administrable by the fleet key
  2   usage
  46  the private key is missing or unusable before ssh is even attempted
  47  the login itself failed
  48  the login succeeded but did not prove what it must
"""
import os
import re
import stat
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
FLEET = REPO / "docs" / "00-control" / "hx-fleet.tsv"
MARKER = "KEY+SUDO-PASS"


def remote_probe(marker: str = MARKER) -> str:
    """The command the session runs to prove it can administer the host.

    `sudo -k` first, because `sudo -n true` alone can be satisfied by a cached
    credential timestamp - `timestamp_type=global` makes one session's password
    entry serve another. A host whose NOPASSWD policy is missing would then emit
    the marker anyway, which is a false PASS on the one control this tool exists
    to prove. With a command, -k makes sudo ignore the cache for that command.
    """
    return "hostname; sudo -k -n true && echo " + marker
DEFAULT_KEY = Path.home() / ".ssh" / "hx_fleet_ed25519"


def fleet_ip(host: str) -> str | None:
    """The recorded address for a host, or None. Accepts hx-5 or HX-5."""
    if not FLEET.is_file():
        return None
    want = host.strip().lower()
    for line in FLEET.read_text(encoding="utf-8").splitlines()[1:]:
        cells = line.split("\t")
        if len(cells) >= 2 and cells[0].strip().lower() == want:
            return cells[1].strip()
    return None


def key_permission_problem(path: str, mode: int) -> str | None:
    """Why a key with this path and mode is unusable to ssh.

    Pure: no filesystem, so tools/hx-doc/hx-gate-tests can exercise the Windows
    mount case on a runner that has no /mnt at all.
    """
    if os.name == "nt":
        return None
    if not mode & (stat.S_IRWXG | stat.S_IRWXO):
        return None
    # A DrvFs mount presents every file as world-readable whatever Windows
    # thinks, so ssh declines to offer it. The key is fine; the path is not.
    if path.startswith("/mnt/"):
        return (
            path + " is on a Windows mount, which presents as world-readable,\n"
            "      so ssh refuses it with 'bad permissions' and then reports a\n"
            "      misleading 'Permission denied'. Run this from Git Bash on the\n"
            "      workstation, where the key's real permissions apply."
        )
    return path + " is group- or world-readable. chmod 600 it."


def key_problem(key: Path) -> str | None:
    """Why this key cannot be used, before ssh is asked to try it.

    ssh reports an unusable key as `Permission denied (publickey,password)`,
    which reads as the server rejecting the key when in fact ssh never offered
    it. Saying so here saves the reader from debugging the wrong end.
    """
    if not key.is_file():
        return str(key) + " does not exist. Set HX_FLEET_KEY to the fleet private key."
    try:
        mode = key.stat().st_mode
        # Permission bits alone miss mode 000: no group or other bits set, so
        # the check below passes, and then ssh cannot load the key. That failure
        # surfaces as exit 47 "the login failed" when the truth is exit 46, the
        # key was never usable. Read a byte and find out.
        with key.open("rb") as fh:
            fh.read(1)
    except OSError as exc:
        return "%s cannot be read: %s" % (key, exc)
    return key_permission_problem(str(key), mode)


def exit_for_session(returncode: int, stdout: str) -> int | None:
    """The status a finished ssh session earns, before its output is read.

    A non-zero return with no output means the login never happened. A non-zero
    return that still printed something means the session ran and then failed,
    which is a proof failure rather than an access failure - and must not be
    allowed to reach a PASS on the strength of the output alone.
    """
    if returncode == 0:
        return None
    return 47 if not stdout.strip() else 48


def verdict(output: str, host: str) -> list[str]:
    """What the login failed to prove. Empty list means it proved everything.

    The probe prints the hostname and then the marker, so both must be present
    as whole lines and in that order. A substring test would accept the marker
    embedded in unrelated output - a login banner quoting this document, say -
    and a set test would accept them in either order, which no real run
    produces.

    Kept apart from the ssh call so tools/hx-doc/hx-gate-tests can exercise
    every refusal without a network or a server.
    """
    problems: list[str] = []
    lines = [ln.strip() for ln in output.splitlines() if ln.strip()]
    short = host.strip().lower()

    host_at = next((i for i, ln in enumerate(lines) if ln.lower() == short), None)
    mark_at = next((i for i, ln in enumerate(lines) if ln == MARKER), None)

    if host_at is None:
        problems.append(
            f"the session did not report hostname '{short}' on a line of its own. "
            f"Saw: {lines[:3] if lines else 'nothing'}"
        )
    if mark_at is None:
        problems.append(
            f"'{MARKER}' absent as a line of its own, so `sudo -k -n true` did "
            "not succeed. The key works but the account has no NOPASSWD policy "
            "- a cached credential does not count."
        )
    if host_at is not None and mark_at is not None and mark_at < host_at:
        problems.append(
            f"'{MARKER}' appeared before the hostname. The probe prints the "
            "hostname first, so this is not the output of the probe."
        )
    return problems


def main() -> int:
    args = [a for a in sys.argv[1:]]
    ip = None
    if "--ip" in args:
        i = args.index("--ip")
        if i + 1 >= len(args):
            print("ERROR: --ip needs an address", file=sys.stderr)
            return 2
        ip = args[i + 1]
        del args[i:i + 2]
    if len(args) != 1:
        print(__doc__.strip().splitlines()[0], file=sys.stderr)
        print("Usage: hx-fleet-access <hx-host> [--ip ADDRESS]", file=sys.stderr)
        return 2

    host = args[0].strip().lower()
    if not re.fullmatch(r"hx-\d+", host):
        print(f"ERROR: '{args[0]}' is not a host name like hx-5", file=sys.stderr)
        return 2

    if ip is None:
        ip = fleet_ip(host)
        if ip is None:
            print(
                f"ERROR: no address recorded for {host} in "
                f"{FLEET.relative_to(REPO).as_posix()}; pass --ip",
                file=sys.stderr,
            )
            return 2

    key = Path(os.environ.get("HX_FLEET_KEY") or DEFAULT_KEY)
    problem = key_problem(key)
    if problem:
        print(f"STOP: {problem}", file=sys.stderr)
        return 46

    user = os.environ.get("HX_ADMIN_USER", "hxsa")
    cmd = [
        "ssh",
        "-o", "PasswordAuthentication=no",
        "-o", "PreferredAuthentications=publickey",
        "-o", "BatchMode=yes",
        "-o", "StrictHostKeyChecking=yes",
        "-o", "ConnectTimeout=10",
        "-o", "IdentitiesOnly=yes",
        "-i", str(key),
        f"{user}@{ip}",
        remote_probe(),
    ]

    print(f"--- external key-only administration proof: {host} ({ip}) ---")
    print(f"key:  {key}")
    print(f"user: {user}")
    print()
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=45)
    except subprocess.TimeoutExpired:
        print(f"STOP: no response from {ip} within 45s.", file=sys.stderr)
        return 47
    except OSError as exc:
        print(f"STOP: could not run ssh: {exc}", file=sys.stderr)
        return 46

    out = r.stdout or ""
    err = (r.stderr or "").strip()
    if out.strip():
        print(out.rstrip())
    if err:
        print(err, file=sys.stderr)

    session = exit_for_session(r.returncode, out)
    if session == 47:
        print(f"\nSTOP: key-only login to {user}@{ip} failed.", file=sys.stderr)
        if "Host key verification failed" in err:
            print("      The host key is not the one on record. Verify it on the "
                  "server\n      itself before trusting it; do not bypass the check.",
                  file=sys.stderr)
        else:
            print("      The fleet key is not accepted for this account. Run\n"
                  "      docs/03-runbooks/common/00-foundation.sh on the host.",
                  file=sys.stderr)
        return 47
    if session == 48:
        print(f"\nSTOP: the session on {user}@{ip} exited {r.returncode}.",
              file=sys.stderr)
        print("      It printed output, so the login worked, but the probe did "
              "not\n      finish cleanly. Output alone is not the proof.",
              file=sys.stderr)
        return 48

    problems = verdict(out, host)
    if problems:
        print(f"\nSTOP: {user}@{ip} answered, but did not prove administration.",
              file=sys.stderr)
        for p in problems:
            print(f"      - {p}", file=sys.stderr)
        return 48

    print(f"\nPASS  {host} is administrable by the fleet key, proven externally.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
