# INSTALLER READINESS CHECKLIST

| Check | Status | Evidence / missing work |
|---|---|---|
| Supported entry point | PARTIAL | Python module entry exists; packaged executable absent |
| Runtime bundling | NOT TESTED | Python/Qt bundle not built |
| Works without Python | NOT TESTED | no package |
| Works without Git | NOT TESTED | no package |
| Works without `D:\quran` | NOT TESTED | runtime abstraction exists, package not tested |
| Clean installation | NOT STARTED | no installer |
| First-run directories | PASS controlled | RuntimeLayout synthetic test |
| Database bootstrap | PASS controlled | migration tests |
| Migration startup | PASS controlled synthetic | M-01..M-16 |
| Backup/Restore | PASS controlled synthetic | recovery suite |
| PDF reports | PASS controlled synthetic | reporting suite |
| Upgrade old version | PARTIAL | schema tests only; package upgrade not tested |
| Reinstall behavior | NOT STARTED | policy not implemented |
| Uninstall behavior | NOT STARTED | policy not implemented |
| Data retention | NOT STARTED | human/product policy required |
| Qt plugins/resources/fonts | NOT TESTED | packaging build absent |
| Code signing | BLOCKED | Release Gate |
| Installer QA | BLOCKED | Release Gate |
| Release approval | BLOCKED | Release Gate |

## Required Future Installer Acceptance

A future package must install to a non-writable program directory, place mutable data in an approved user data directory, initialize SQLite, run migrations with backup/recovery, create local reports, work without Python/Git/project root, and define uninstall/reinstall retention explicitly.
