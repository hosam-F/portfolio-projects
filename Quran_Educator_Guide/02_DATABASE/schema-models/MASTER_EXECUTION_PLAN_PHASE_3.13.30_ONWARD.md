# Master Execution Plan — Continuation from Phase 3.13.29

**Project:** دليل المربي القرآني / صُنّاع المربي والمفكر  
**Owner:** م/ حسام الجرافي  
**Baseline:** Phase 3.13.29 = PARTIAL / BLOCKED at VM-04 transfer boundary  
**Operating boundary:** Offline-only, synthetic TEST DATA ONLY, no real Quran content, no real personal data.

## Execution order

| Order | Workstream | Exit evidence | Stop condition |
|---|---|---|---|
| 1 | Resolve VM-04 transfer safely | VMX/Guest identity, artifact transfer, exact Host/Guest SHA-256 | No safe channel, credential ambiguity, or destructive VM action |
| 2 | Qualify Clean Guest | Windows/build/arch/user/groups/Tools/runtime readiness | Guest cannot be independently identified or accessed |
| 3 | Guest artifact validation | Install, First Run, SQLite, Smoke, GUI, restart, backup/restore | Any app failure is recorded before any fix; no stale result |
| 4 | Functional V1 regression | Direct evidence for supported routes/workflows | Unsupported capability is NOT EVIDENCED, not simulated |
| 5 | Final GUI/UX/accessibility pass | Matrix for all views: layout, RTL, typography, dialogs, tables, DPI, keyboard, screen reader | Real defect requires Change Control and rebuild/retest |
| 6 | Standard User validation | Identity, Users-only membership, install/write/runtime/backup/restore | No Administrator/runas/elevation workaround |
| 7 | Audit/restart/data safety | Direct visible events, persistence and data-preservation evidence | Missing direct proof remains NOT EVIDENCED |
| 8 | Upgrade/Repair/Uninstall/Reinstall | Independent backup, old-to-new, repair, uninstall/reinstall preservation | Any data loss or unisolated operation blocks release |
| 9 | Final consolidation | Report, manifest, evidence index, traceability, delivery inventory | Any critical unresolved blocker keeps gates closed |

## Build and change discipline

No historical artifact, evidence, VM, VMDK, snapshot, source file, or database is deleted or overwritten. Any source change must follow Diagnose → Change Proposal → Minimal Fix → Source Test → Build → Hash → Install → Validate → Evidence. Schema, Database Design, Domain Model, Relations, Business Rules, content/licensing policy, data retention, backup policy, and export policy remain unchanged unless a documented Human Decision is required.

## Current authoritative status

`SOURCE_POST_FIX = PASS`  
`ONE_FOLDER_SMOKE = PASS`  
`HOST_INSTALLER_SMOKE = PASS`  
`VM04_TRANSFER = BLOCKED`  
`VM04_INSTALLER = NOT RUN`  
`STANDARD_USER = NOT RUN`  
`UPGRADE = NOT RUN`  
`REPAIR = NOT RUN`  
`AUDIT = NOT EVIDENCED / BLOCKED`  
`CONTENT_GATE = LOCKED / NO-GO`  
`RELEASE_GATE = LOCKED / NO-GO`  
`PRODUCTION_READY = NO`  
`RELEASE_READY = NO`

## Immediate next action

Perform non-destructive VM-04 and transfer-channel diagnosis only. Prefer an already authenticated VMware Tools/Guest channel or a user-provided Guest credential through the secure interaction path; do not guess credentials. Do not execute the Installer until the Guest copy exists and its SHA-256 exactly matches the Host artifact.
