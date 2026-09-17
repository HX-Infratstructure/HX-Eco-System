# HX-8 Current Runbook

**Host:** hx-8
**Expected IP:** `192.168.50.208`
**FQDN:** `hx-8.hx.local.arpa`
**Role:** Open WebUI, the human-facing chat interface
**Target release:** `0.11.3`, PyPI wheel into a native venv

## 1. HX authority and boundaries

This runbook executes the shared blocks. It does not redefine them. Where this
file and a control document disagree, the control document wins.

- Functional proof: D-008, ratified. One temporary connection to an
  already-proven Ollama endpoint, one prompt, one response rendered in the UI,
  evidence captured, then the connection removed.
- Proof obligation: step `G1` in [`hx-proof.tsv`](../../00-control/hx-proof.tsv).
- Proof procedure: [`open-webui-smoke-test.md`](../../../smoke-tests/open-webui-smoke-test.md).
- As-built record: [`HX-8.md`](../../02-server-records/HX-8.md).
- Implementation and pins: `../common/`, with pins in `../common/hx-base.env`.

HX-8 is the last server in the build order. It consumes the inference plane
rather than providing it, so it proves the planes beneath it already work.

## 2. Foundation — inherited, not duplicated

Layer 0/1 is established once, by the shared foundation block. Run it first:

```bash
../common/00-foundation.sh hx-8
```

`01-base-admin-network-updates.sh` opens with a gate that refuses to continue
without that state, and names what is missing:

| Exit | Meaning |
|---|---|
| 41 | the host cannot resolve its own FQDN |
| 42 | HX-1 is not the selected time source |
| 43 | the fleet key is absent |
| 44 | the fleet key is present with the wrong fingerprint |
| 45 | neither `ssh.service` nor `ssh.socket` is enabled |

Do not work around a foundation exit. Run `00-foundation.sh` and read what it
reports. Proof step `F0` must be satisfied before HX-8 can close.

## 3. Execution

Run from this directory. Each block refuses to run on any host other than
`hx-8`.

```bash
../common/00-foundation.sh hx-8     # foundation; no reboot
./01-base-admin-network-updates.sh  # reboots
./02-domain.sh                      # reboots
../common/10-open-webui.sh hx-8
```

The block does not accept or persist an administrator email or password. After
the service starts, open its LAN URL and create the first account manually; the
first account becomes the administrator. Its credentials are supplied through
the Open WebUI registration form and are never stored in this repository or
the systemd environment file.

## 4. Sequence

1. **Foundation.** Network validated and never written (D-026), identity, time
   authority against HX-1, admin account and NOPASSWD sudo, fleet key, SSH
   persistence.

2. **Base, admin, network, updates.** Foundation gate, then `apt update` and
   `apt upgrade`, then reboot.

3. **Domain join.** Join `hx.local.arpa`, validate SSSD and domain user
   resolution, then reboot. The block is shared and installs a driver only on
   the hosts that carry one. It installs nothing here.

4. **Open WebUI.** `../common/10-open-webui.sh hx-8` proves the dedicated
   volume, asserts the Python range, installs the pinned wheel into a venv,
   reads the installed version back, writes the session-secret file and the
   unit, and proves the service answers. Create the first account manually in
   the UI after the service starts.

5. **Proof.** Run [`open-webui-smoke-test.md`](../../../smoke-tests/open-webui-smoke-test.md)
   for proof step `G1` and D-008. Remove the temporary connection afterwards.

6. **Closure.** Section 8 below.

## 5. What the block enforces

Each of these stops the build rather than reporting a warning.

| Exit | Refuses |
|---|---|
| 34 | `/srv/openwebui` is not mounted, or is not writable by the service identity |
| 40 | the system `python3` is outside `>=3.11,<3.13` |
| 30 | the `open-webui` entry point is missing after install |
| 31 | the installed distribution metadata gave no usable version |
| 33 | the installed version is not the pin |
| 32 | the service never answered on its port |

Exit 33 exists because an installer's exit code is not proof of what landed.
HX-6 lost a build day to npm reporting success while silently dropping a
package, so the version is read back from the distribution metadata, through
the venv interpreter the unit executes. The CLI is not asked: `open-webui`
accepts no `--version` and exits 2 on it, observed on hx-8 against 0.11.3.

## 6. Storage

`/srv/openwebui` is a dedicated mounted volume, the same shape as HX-6 and
HX-7. Do not format, wipe, repartition or remount it. The block proves the
mount before anything is created, because everything Open WebUI keeps lives
under it:

```text
/srv/openwebui/venv             the virtual environment
/srv/openwebui/data             DATA_DIR: webui.db, uploads
/srv/openwebui/hf               HF_HOME: model cache
/srv/openwebui/open-webui.env   secrets, root:root 0600
```

**`DATA_DIR` is not an inert setting.** When it resolves differently from a
previous run, upstream moves the contents, archives the old directory and
removes it. Change that value deliberately or not at all.

## 7. Authentication and extras

**Authentication is on.** `WEBUI_AUTH=True`, which is upstream's own default.
An earlier version of the shared block set it to `False`, which removed the
login form entirely on a LAN-facing UI that D-008 then wires to a working
Ollama endpoint. The exposure there is the inference plane, not a web page.

`ENABLE_SIGNUP=False` ships with it, so no account exists until one is created
deliberately. The first account created becomes the administrator. Until then
nobody can sign in, which is the point: the window in which the UI is open is
one that somebody chooses.

The block does not bootstrap an owner account or persist account credentials.
Create the first account manually through the Open WebUI registration form.

**Extras are opt-in and currently empty.** `open-webui[all]` adds thirteen
packages, among them Azure Search, Pinecone, Oracle and Elasticsearch clients,
and Playwright. Installing a connector is not approving it, which is the line
D-010 draws for HX-6. Set `HX_OPEN_WEBUI_EXTRAS` in `hx-base.env` only when a
named HX capability needs one, and record which and why.

Playwright is worth naming separately: its Python package installs, but its
browser binaries need a separate step this block does not run, so anything
depending on it fails at use rather than at install.

## 8. HX-8 BASE PASS definition

| Requirement | Evidence |
|---|---|
| Foundation established | proof step `F0` satisfied |
| Every Foundation row filled | `tools/hx-doc/hx-record-check` passes for HX-8 |
| External key-only administration | `tools/hx-doc/hx-fleet-access hx-8` returns `hx-8` and `KEY+SUDO-PASS` |
| Domain join | `realm list` reports `configured: kerberos-member`; domain user resolves |
| Dedicated storage | `/srv/openwebui` mounted, proven by the block |
| Installed version | matches the pin, read back from distribution metadata |
| Service serving | `hx-open-webui` active and enabled, `/health` answering on the LAN address |
| Authentication | `WEBUI_AUTH=True`, admin account created, signup closed |
| Provenance recorded | section 6 of the record carries version, source, extras and Python |
| Reboot persistence | active, enabled and answering after an unattended reboot |
| Routing proof | step `G1` and D-008 run, evidence retained, temporary connection removed |

`systemctl is-active` alone is not proof. A service that crashes and restarts
reports `active` in the gaps between restarts, which is how HX4-F06 went
unseen. The HTTP response is what shows it is serving.

## 9. Record and fleet closure

1. Fill [`HX-8.md`](../../02-server-records/HX-8.md), including every Foundation
   row and section 6 provenance.
2. Set `state` and `gate` for `HX-8` in [`hx-fleet.tsv`](../../00-control/hx-fleet.tsv).
3. Set `G1` status in [`hx-proof.tsv`](../../00-control/hx-proof.tsv).
4. Run `tools/hx-doc/hx-fleet`, `tools/hx-doc/hx-record-check` and
   `tools/hx-doc/hx-render-html`.

## 10. Non-goals

- No Docker, Podman, Kubernetes or Snap. Native venv and systemd only.
- Do not enable extras to see what they do.
- Do not disable authentication.
- Do not leave the D-008 connection in place after the proof.
- Do not mount or wipe unrelated disks.
- Do not import prior application state.
