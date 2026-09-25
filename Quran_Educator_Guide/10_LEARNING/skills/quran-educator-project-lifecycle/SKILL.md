---
name: quran-educator-project-lifecycle
description: "Evidence-preserving lifecycle management for the Quranic Educator Guide project: planning, synthetic-only implementation validation, Windows installer and clean-machine checks, checkpoints, gate control, traceability, readiness, and delivery documentation. Use when managing, validating, packaging, or documenting this project or a similar offline local educational Windows application."
---

# Quranic Educator Project Lifecycle

Use this skill to manage the project as an evidence-driven, offline-first Windows productization process. Read `references/project_validation_protocol.md` when executing a full validation, recovery, packaging, or delivery workflow.

## Identity and Non-Negotiable Boundaries

Preserve the following identity in every report:

- **Project:** دليل المربي القرآني / صُنّاع المربي والمفكر
- **Owner:** م/ حسام الجرافي
- **Architecture:** modular local Windows application with Python, PySide6, SQLite, SQLAlchemy, and ReportLab.

Keep `CONTENT_GATE = LOCKED / NO-GO` and `RELEASE_GATE = LOCKED / NO-GO` unless the owner explicitly authorizes a documented gate review and every prerequisite is satisfied. Use synthetic data only until the content gate is formally opened. Never infer ownership from tool usage; separate the owner, original works, licensed external material, contributions, development tools, and user-created data.

## Operating Workflow

1. Establish scope, current state, owner, gates, permitted directories, and safety constraints.
2. Read the nearest `AGENTS.md` before changing files. Preserve historical reports and append current status rather than rewriting old evidence.
3. Create a pre-change checkpoint. Include timestamp, intended action, current gates, known risks, and rollback boundary.
4. Review existing requirements, architecture, schema, curriculum, roles, UI/UX, security, reporting, backup, testing, roadmap, decisions, dictionary, and ownership documents before proposing changes.
5. Separate documentation-only work from implementation, database, packaging, OS, and VM operations. Ask before any system-level change, credential use, destructive recovery, or permission change.
6. For data and UI work, use fixtures explicitly marked `TEST DATA ONLY` and `NOT QURAN CONTENT`. Do not add real Quranic text, real student data, personal data, or cloud/API dependencies.
7. For installer validation, hash the host artifact; transfer through an isolated read-only path; hash the Guest copy; compare exact SHA-256 values; and launch only after a match.
8. Run lifecycle checks in order: `EX-01` Installer Launch, `EX-02` First Run/SQLite, `EX-03` Synthetic Controlled Workflow, `EX-04` Backup/Restore, `EX-05` Restart Persistence/Search, `EX-06` Standard User Operation, and `EX-07` Upgrade/Uninstall Data Safety.
9. Require a real Windows non-admin identity for EX-06. `BUILTIN\Administrators` shown as membership or deny-only is not valid Standard User evidence. Do not change account membership to make the test pass.
10. Require an independent, verified backup before EX-07. Never treat an upgrade artifact as proof that upgrade passed, and never treat an uninstall artifact as proof of data safety.
11. Treat a hash mismatch as a hard stop. Treat `INACCESSIBLE_BOOT_DEVICE`, failed VM resume, or missing Guest namespace as an environment blocker, not an application failure. Preserve VMDK, VMEM, VMSS, VMSN, snapshots, and checkpoints; do not repair, delete, or change controllers blindly.
12. Treat an Audit screen as `NOT EVIDENCED / BLOCKED` unless readable audit events are directly visible and traceable.
13. When a test is blocked, record the exact blocker and continue only with safe work independent of that environment: evidence reconciliation, synthetic-data review, schema/source inventory, documentation, matrices, and delivery inventory.
14. Reconcile `STATUS`, `DECISIONS`, `ROADMAP`, `TRACEABILITY`, and `V1_PRODUCTION_READINESS_GAP_MATRIX`. Preserve historical states and append an authoritative current section.
15. Produce a final matrix and delivery inventory that distinguish `PASS`, `FAIL`, `BLOCKED`, `NOT EVIDENCED`, `NOT RUN`, `PRESENT`, `HASHED`, and `ARTIFACT ONLY`.
16. Create a checkpoint and session-log entry after each significant test group and before/after risky operations.

## Required Evidence Record

For each test or claim, record the test ID, expected behavior, exact evidence file or screenshot, timestamp, environment/account, synthetic-data boundary, and what the result does not prove. Do not promote an artifact-only observation to a behavioral pass.

## Recovery Rules

When a VM fails, first inventory non-destructively. Look for a documented bootable checkpoint or snapshot, but do not assume a `.vmem`/`.vmss` is bootable. Do not select destructive recovery options without explicit owner approval. If no safe bootable state is confirmed, classify the external test as `BLOCKED — ENVIRONMENT BOOT FAILURE` and move to documentation and delivery work.

## Delivery Outputs

For a completion run, create or update `PROJECT_PERMANENT_STATE.md`, `EXECUTION_SESSION_LOG.md`, `docs/DECISIONS.md`, `docs/ROADMAP.md`, `docs/TRACEABILITY_V1.md`, `docs/V1_PRODUCTION_READINESS_GAP_MATRIX.md`, a phase execution summary, a release-readiness report, `docs/MASTER_VALIDATION_MATRIX_FINAL.md`, and `docs/RELEASE_DELIVERY_INVENTORY.md`.

The final summary must state what is complete, what is documented, what is tested, what is not tested, what is blocked, what requires human approval, the exact Installer hash, and the unchanged gate status.

## Reusable Status Template

```text
Project: دليل المربي القرآني / صُنّاع المربي والمفكر
Owner: م/ حسام الجرافي
CONTENT_GATE = LOCKED / NO-GO
RELEASE_GATE = LOCKED / NO-GO

EX-01 = PASS | evidence: ...
EX-02 = PASS | evidence: ...
EX-03 = PASS | evidence: ...
EX-04 = PASS | evidence: ...
EX-05 = PASS | evidence: ...
EX-06 = BLOCKED / NOT RUN | reason: ... | evidence: ...
EX-07 = NOT RUN | reason: ...
AUDIT EVENTS = NOT EVIDENCED / BLOCKED | evidence: ...

Next safe action: ...
```
