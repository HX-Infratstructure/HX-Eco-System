# Files

- [Change and Review Workflow](change-and-review-workflow.md)
- [Documentation Gates and Enforcement Tools](doc-gates.md) - The tools/hx-doc/ enforcement layer — what each gate checks, what it refuses, and what a failure means — plus the CI layer and the meta-gate that breaks every checker on purpose.
- [Proof Chain and Smoke Eligibility](proof-chain.md) - How the hx-proof.tsv proof DAG defines the smoke-test dependency chain, how step readiness is checked, and how hx-smoke-promote enforces cumulative proof with no bypass.
- [Server Records and Evidence Retention](server-records-and-evidence.md) - The one-file-per-server record pattern, the record-check gate, the inline vs run-bundle evidence models, and the invariants that keep retained proof honest.
