# Evidence

Store current validation evidence by server/application.

## Standard naming

`YYYYMMDDTHHMMSSZ_<server>_<component>_<gate>_<description>.<ext>`

## Standard retained bundle

```text
docs/05-evidence/<server>/<component>/<run-id>/
├── manifest.md
├── result.txt
├── cleanup.txt
└── supporting captures as required
```

Every retained run must identify:
- runner host;
- system under test;
- component/version or revision;
- smoke-test authority file;
- repository commit used;
- known-answer input;
- PASS/FAIL determination;
- cleanup result and cleanup verification;
- reboot-persistence result when applicable.

Failed evidence is not overwritten by a later PASS. A retry receives a new run ID.

Secret values must not appear in retained evidence. If command output accidentally includes a token, password, private key, PAT, or other credential, redact that credential before promotion while preserving the functional result.

HX-5 CentCom is the standard remote smoke-test execution station after its activation gate. Detailed procedure: `../04-application-standards/HX-5-SMOKE-TEST-PROCESS-AND-PROCEDURES.md`.

Evidence supports current state but does not independently override explicit owner decisions.
