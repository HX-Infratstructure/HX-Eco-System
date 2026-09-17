# HX-7 — NGINX dev/test only Server Configuration

**Build state:** IN PROGRESS
**Gate:** C4_DEFERRED
**IP:** `192.168.50.207`
**FQDN:** `hx-7.hx.local.arpa`
**Record updated:** 2026-09-17

Built 2026-09-17, 00:21 to 00:33 UTC. Layer 0/1 and the application are proven
and the host survives a reboot. The state is IN PROGRESS rather than PASS
because `C4` is HX-7's functional gate and it has not run, and
`docs/00-control/BUILD-STATE.md` makes the functional gate part of what PASS
means. Section 7 says why it is deferred.

## Foundation

Established by `docs/03-runbooks/common/00-foundation.sh` before Block 1, and
gated by `01-base-admin-network-updates.sh`, which refuses to proceed without
it. Proven from the operator workstation, which is not this host.

| Control | Evidence | State |
|---|---|---|
| `hostname -f` | `hx-7.hx.local.arpa` | PASS |
| AD DNS A record | `192.168.50.207`, read from HX-1 directly rather than through this host's resolver | PASS |
| Time authority | `chronyc sources` selects `^* 192.168.50.200`, offset -150us; tracking reference `C0A832C8 (192.168.50.200)` | PASS |
| Fleet key | `SHA256:fpIJEHjkhRYRqnhvRhtgSqggOAjkTU90vSGWbh0vsPk`, comment `hx-fleet-20260810`, in `/home/hxsa/.ssh/authorized_keys` | PASS |
| NOPASSWD sudo | `sudo -k -n true` succeeds, so a cached credential is not what proves it | PASS |
| SSH persistence | `ssh.socket` enabled; `ssh.service` disabled, which is correct on Ubuntu | PASS |
| External key-only login | `tools/hx-doc/hx-fleet-access hx-7` returns `hx-7` and `KEY+SUDO-PASS`, run from the operator workstation | PASS |
| SSH host key | ed25519 `SHA256:vujtx9f0GPBlEQA9gF2SS2uSf3aTzmAlBpFXrdSX6x4`<br>rsa `SHA256:+HlJXtdsTdL+mPsz2aUAPIZkjsRjhePczKiOYxX7O04` | PASS |
| SPNs in AD | `host/HX-7`, `host/hx-7.hx.local.arpa`, `RestrictedKrbHost/HX-7`, `RestrictedKrbHost/hx-7.hx.local.arpa`; `dNSHostName` is `hx-7.hx.local.arpa` | PASS |

The SPN row was read from the directory on HX-1, not from this host's keytab.
HX5-F12 established that the keytab lists only what was issued to the host and
`kvno` reports only what a KDC will serve, so neither settles what AD stores.
HX-7 arrived with all four forms and an FQDN `dNSHostName`, which is the state
HX-2, HX-3 and HX-4 had to be corrected into.

## 1. Identity and Network

- Hostname: `hx-7`
- FQDN: `hx-7.hx.local.arpa`
- IP: `192.168.50.207/24`
- Interface: `enp2s0`
- Realm: `HX.LOCAL.ARPA`
- DNS: `192.168.50.200` (HX-1)

Domain join, after the Block 2 reboot:

```text
$ realm list | grep configured:
  configured: kerberos-member

$ systemctl is-active sssd
active

$ id jarvisr@hx.local.arpa
uid=218001148(jarvisr@hx.local.arpa) gid=218000513(domain users@hx.local.arpa) groups=218000513(domain users@hx.local.arpa)
```

`/etc/hosts` carries `127.0.1.1 hx-7.hx.local.arpa hx-7`, which is the Ubuntu
default and is present on HX-5 identically. It means `getent hosts` answers
from the file rather than from AD, so the DNS row above was verified by querying
HX-1 directly instead.

**Domain join gate: PASS**

## 2. Operating System

| Item | Value |
|---|---|
| Distribution / release | Ubuntu 24.04.5 LTS |
| Kernel | `6.8.0-139-generic` |
| Firmware version | `UNRESOLVED` — no firmware change was made during this build |
| sudo policy | `hxsa ALL=(ALL:ALL) NOPASSWD: ALL` in `/etc/sudoers.d/90-hx-admin` |

`apt update` and `apt upgrade` ran in Block 1. Four packages remain upgradable
as of 2026-09-17, all one source package held back by Ubuntu's phased rollout:

```text
libnetplan1        1.1.2-8ubuntu1~24.04.1 -> ~24.04.3
netplan-generator  1.1.2-8ubuntu1~24.04.1 -> ~24.04.3
netplan.io         1.1.2-8ubuntu1~24.04.1 -> ~24.04.3
python3-netplan    1.1.2-8ubuntu1~24.04.1 -> ~24.04.3
```

They are phased, not held by this build, and no `apt-mark hold` is set on this
host. D-026 makes network configuration something this process validates and
never writes, so a netplan upgrade is a deliberate act rather than something a
block should take on its own.

## 3. GPU Configuration

**HX-7 has no GPU.** No driver was installed and none is expected.

```text
$ dpkg -l 'nvidia-driver-*' 'nvidia-dkms-*' 'nvidia-kernel-*' | grep '^ii'
(no driver packages)

$ command -v nvidia-smi
(absent)
```

One package matches the name and is not a driver:

```text
ii  linux-firmware-nvidia-graphics  20240318.git3b128b60-0ubuntu3.1  all  Firmware for Nvidia graphics
```

That ships with Ubuntu's `linux-firmware` and was present before this build. It
does not match the D-028 hold pattern, which is scoped to the pinned branch, so
Block 1 correctly reported nothing to hold.

Block 2 confirmed the expectation against the hardware rather than trusting the
host list:

```text
hx-7 carries no GPU, so Block 2 is domain join only here.
```

**GPU gate: N/A — no GPU fitted**

## 4. Storage Layout

| Device | Size | FS | Mount |
|---|---|---|---|
| `nvme0n1p1` | 1G | vfat | `/boot/efi` |
| `nvme0n1p2` | 120G | ext4 | `/` |
| `nvme0n1p3` | 117.4G | ext4 | `/srv/nginx` |

`/srv/nginx` is a dedicated partition, mounted by UUID
`9b334181-272c-4b0a-8d15-caab0997848f` from `/etc/fstab`, provisioned by the
installer. It was mounted and empty apart from `lost+found` before the NGINX
block ran, at 24K used. No disk was partitioned, formatted or mounted during
this build.

`/srv` itself is a directory on `/`, not a mount. That does not matter, because
the dedicated volume is mounted one level deeper at exactly the prefix the
build writes to.

Dedicated application path: `/srv/nginx`, which holds the configuration, the
`conf.d` drop-in directory and both logs. Logs therefore land on the dedicated
volume rather than on `/`.

**Storage gate: PASS**

## 5. Runtime

| Item | Value |
|---|---|
| Source | upstream source tarball from `nginx.org`, built natively |
| Installed version | `nginx/1.30.4` |
| Service unit | `hx-nginx.service` |
| Binary | `/usr/local/sbin/nginx` |
| Configuration | `/srv/nginx/nginx.conf`, with `include /srv/nginx/conf.d/*.conf` |
| Listener | `0.0.0.0:80` |
| Optional modules | `compat`, `http_ssl`, `http_v2`, `http_realip`, `http_stub_status`, `http_sub` |

```text
$ ss -ltn | grep :80
LISTEN 0      511          0.0.0.0:80        0.0.0.0:*
```

Not Snap and not the Ubuntu archive, per D-021.

nginx compiles about thirty modules by default, including `proxy`, `rewrite`,
`gzip` and the upstream balancers, so the proxy role needs nothing added for
it. The six above are default-off. `compat` is the structural one: without it
nginx refuses to load any third-party dynamic module, and adding one later
would mean another build rather than a configuration change.

## 6. Model / Application Provenance

```text
HX alias:              hx-nginx
Upstream identity:     NGINX 1.30.4
Source URI:            https://nginx.org/download/nginx-1.30.4.tar.gz
Artifact SHA-256:      4261dc90e9e47c1c4041276e9aaa3d48ebe2e664f728e14fa95ae6c67d57a08b
Import method:         build from source
```

The source tarball was verified against its recorded pin before the build. The
binary that build produced:

```text
Binary path:      /usr/local/sbin/nginx
Binary SHA-256:   1aaea115232e297901414a82033992a52d0217bfce258382718ac7815aeaa151
Build arguments:  --prefix=/srv/nginx --sbin-path=/usr/local/sbin/nginx
                  --conf-path=/srv/nginx/nginx.conf --pid-path=/run/nginx.pid
                  --error-log-path=/srv/nginx/logs/error.log
                  --http-log-path=/srv/nginx/logs/access.log
                  --with-compat --with-http_ssl_module --with-http_v2_module
                  --with-http_realip_module --with-http_stub_status_module
                  --with-http_sub_module
```

Rebuilt on 2026-09-17 at 01:27 UTC to add four modules, so this digest replaces
the one from the first build, `b595c64f...`. The source tarball is the same
artifact and its digest is unchanged; only the configure arguments differ.

The running process was checked against the file rather than assumed:

```text
$ sudo sha256sum /proc/$(cat /run/nginx.pid)/exe
1aaea115232e297901414a82033992a52d0217bfce258382718ac7815aeaa151
```

That check exists because `systemctl enable --now` does nothing to a unit that
is already running. Before the block gained an explicit restart, a rebuild
replaced the file on disk and left the previous binary serving, and the block's
own health check would have passed against it.

Both digests are recorded because the tarball hash proves what was compiled and
the binary hash proves what is running. A version string establishes neither.

## 7. Functional Validation

Evidence model 2 applies to HX-7, but no run bundle exists yet, because the
only smoke test assigned to this server is proof step `C4` and that step is
deferred. The install and persistence proof below is inline. See section 9.

### Service state

```text
$ systemctl is-active hx-nginx
active
$ systemctl is-enabled hx-nginx
enabled
$ nginx -t
nginx: the configuration file /srv/nginx/nginx.conf syntax is ok
nginx: configuration file /srv/nginx/nginx.conf test is successful
```

### LAN proof, issued from off-host

```text
$ curl -fsS -o /dev/null -w '%{http_code}\n' http://192.168.50.207/
200
```

Issued from the operator workstation, not from HX-7. The block's own health
check runs against `127.0.0.1`, which cannot prove the service is reachable on
the LAN.

### Reboot persistence

The host was rebooted after the application was installed, then re-checked
without intervention.

```text
$ uptime -s
2026-09-17 00:33:08

$ systemctl is-active hx-nginx
active
$ systemctl is-enabled hx-nginx
enabled

$ findmnt -no SOURCE,TARGET,FSTYPE /srv/nginx
/dev/nvme0n1p3 /srv/nginx ext4

$ chronyc sources | grep '\^\*'
^* 192.168.50.200                3   6    17     5    +17us[  +46us] +/-   73ms

$ curl -fsS -o /dev/null -w '%{http_code}\n' http://192.168.50.207/
200
```

Serving, enabled, dedicated volume still mounted, and still tracking HX-1.

That reboot proved the first binary. The rebuild at 01:27 UTC replaced it, so
the host was rebooted a second time and re-checked without intervention.

```text
$ uptime -s
2026-09-17 01:39:07

$ sudo sha256sum /proc/$(cat /run/nginx.pid)/exe
1aaea115232e297901414a82033992a52d0217bfce258382718ac7815aeaa151

$ nginx -V 2>&1 | grep -o -- '--with-[a-z_0-9]*'
--with-compat --with-http_ssl_module --with-http_v2_module
--with-http_realip_module --with-http_stub_status_module --with-http_sub_module

$ systemctl is-active hx-nginx
active
$ systemctl is-enabled hx-nginx
enabled

$ findmnt -no SOURCE,TARGET,FSTYPE /srv/nginx
/dev/nvme0n1p3 /srv/nginx ext4

$ chronyc sources | grep '\^\*'
^* 192.168.50.200                3   6    37    31  -2878ns[  +26us] +/-   76ms

$ curl -fsS -o /dev/null -w '%{http_code}\n' http://192.168.50.207/
200
```

The digest read from `/proc` after the reboot is the rebuilt binary, so this
row is evidence for the artifact the record names, not only for the unit.

### Known failed units

```text
$ systemctl --failed
● sssd-nss.socket      loaded failed failed SSSD NSS Service responder socket
● sssd-pam-priv.socket loaded failed failed SSSD PAM Service responder private socket
```

This is HX4-F02, open and deferred fleet-wide. `/etc/sssd/sssd.conf` carries
`services = nss, pam`, so the responders start under `sssd.service` while their
socket units also attempt activation. Domain identity resolution is unaffected
and is shown in section 1. HX-4 exhibited three failed sockets; HX-7 has two.

### One host event, recorded rather than tidied away

The first attempt at the rebuild stopped when `apt` crashed:

```text
apt[1782]: segfault at 71dceee34100 ip 000071d7722fe705 sp 00007fffa7e32f58
           error 4 in libapt-pkg.so.6.0.0
```

The host was healthy at the time: 14Gi memory free, no OOM kill, `dpkg --audit`
clean, and all four build dependencies already installed, so the line that
crashed had nothing to do. Re-running the same command immediately afterwards
returned `rc=0`, and the build then completed. Recorded because a segmentation
fault inside `libapt-pkg` on a newly built host is worth recognising if it
happens again, not because anything is known to be wrong.

### Deferred: proof step C4

`C4` requires one temporary private-IP HTTP upstream hosted on HX-5, and HX-5
is not available for this purpose. The step stays `NOT_RUN` in
`docs/00-control/hx-proof.tsv` and the gate on this record is `C4_DEFERRED`
rather than `CLOSED`, so the obligation stays visible instead of being quietly
dropped.

## 8. Final State

| Gate | Result |
|---|---|
| Clean base build | PASS |
| Domain join / SSSD | PASS |
| GPU driver and visibility | N/A — no GPU fitted |
| Dedicated storage | PASS |
| Runtime version | PASS — `nginx/1.30.4` |
| Service active / enabled | PASS |
| Model / application loaded | PASS — both digests recorded |
| Known-answer functional proof | DEFERRED — proof step `C4` |
| Reboot persistence | PASS — twice, the second against the current binary |

## 9. Evidence References

Evidence model 2 applies, and no bundle is retained yet. The only smoke test
assigned to HX-7 is `smoke-tests/nginx-smoke-test.md`, run as proof step `C4`,
and that step is deferred for the reason in section 7. A retained bundle under
`docs/05-evidence/hx-7/nginx/<run-id>/` follows when `C4` runs.

Until then the proof is inline in section 7, with the exact commands and the
exact responses.
