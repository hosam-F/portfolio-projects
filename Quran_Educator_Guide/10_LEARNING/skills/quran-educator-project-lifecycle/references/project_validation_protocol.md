# Project Validation Protocol

## Project Identity

Use these defaults when the skill is invoked for this project:

- Project: دليل المربي القرآني / صُنّاع المربي والمفكر
- Owner: م/ حسام الجرافي
- Architecture intent: modular local Windows application using Python, PySide6, SQLite, SQLAlchemy, and ReportLab
- Operating principle: offline-first, synthetic-data-first, evidence-preserving

## Gate Model

Never open `CONTENT_GATE` or `RELEASE_GATE` implicitly. Keep the following states explicit:

- `CONTENT_GATE = LOCKED / NO-GO` until an approved human Quranic source, licensing/provenance record, and review evidence exist.
- `RELEASE_GATE = LOCKED / NO-GO` until critical acceptance evidence, external lifecycle evidence, and owner approval exist.
- `PRODUCTION_READY = NO` and `RELEASE_READY = NO` whenever a critical acceptance item is blocked or not run.

## Evidence Vocabulary

Use only these result labels:

- `PASS`: direct evidence exists and satisfies the criterion.
- `FAIL`: the tested subject violated the criterion; do not use for an environment outage.
- `BLOCKED`: execution could not proceed because of a named environment, access, or dependency blocker.
- `NOT EVIDENCED`: an interface or claim was observed but the required proof was not visible.
- `NOT RUN`: intentionally not executed.
- `PRESENT / ARTIFACT ONLY`: a file exists, but its existence is not proof that the behavior passed.

Record the exact evidence path, timestamp, scope, and boundary for every result.

## Sequential Workflow

1. Identify the owner, scope, gates, allowed directories, and prohibited data.
2. Inspect the current project state and read nearest `AGENTS.md` before editing.
3. Create a pre-change checkpoint containing the current state, intended action, and rollback boundary.
4. Separate design/documentation work from code, database, installer, and environment work.
5. Use synthetic fixtures only for development and external validation. Mark them `TEST DATA ONLY` and `NOT QURAN CONTENT`.
6. For installer validation, hash the host artifact, transfer through an isolated read-only path where possible, hash the Guest copy, hash-compare exact SHA-256 values, and start only after a match.
7. Execute lifecycle tests in order: installer launch, first run/SQLite, synthetic workflow, backup/restore, restart persistence, Standard User operation, then upgrade/uninstall only after independent backup confirmation.
8. Treat audit visibility as unproven unless readable events are directly visible.
9. If a VM or transport problem appears, preserve evidence and avoid destructive recovery. Do not delete VMDK, VMEM, VMSN, snapshots, or checkpoints without explicit approval.
10. When a requested test is blocked, record the blocker and continue with safe documentation and inventory work that does not depend on the blocked environment.
11. Reconcile status documents, decision records, roadmap, gap matrix, and traceability matrix. Do not rewrite historical evidence; append a current authoritative status section.
12. Create one final validation matrix, one delivery inventory, one execution summary, and one release-readiness report.
13. Validate the skill and deliver its `SKILL.md` path. Preserve a project-local copy when requested.

## Safety Stop Conditions

Stop and ask for a decision when a hash mismatches, a destructive recovery option is presented, a user-data or real-content boundary could be crossed, a credential must be guessed or exposed, a system-level permission or registry change is required, or a test could delete/replace application data.

## Documentation Pattern

Each phase report should state: scope, owner, date, gates, evidence register, acceptance matrix, executed tests, blocked/not-run tests, risks, decisions, next safe action, and a clear statement of what the evidence does not prove.

## Delivery Review

Before declaring a package deliverable, inventory source, tests, requirements, synthetic fixtures, runtime database artifacts, backups, installer, hash manifest, reports, checkpoints, permanent state, and execution log. Mark each item as `PRESENT`, `HASHED`, `TESTED`, `ARTIFACT ONLY`, `BLOCKED`, `NOT RUN`, or `MISSING`. Separate production blockers from optional future work.
