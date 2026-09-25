# MASTER VALIDATION MATRIX — FINAL

**Project:** دليل المربي القرآني / صُنّاع المربي والمفكر  
**Owner:** م/ حسام الجرافي  
**Baseline:** Phase 3.12.12 controlled external validation  
**Date:** 2026-08-24  
**CONTENT_GATE:** `LOCKED / NO-GO`  
**RELEASE_GATE:** `LOCKED / NO-GO`

## Status Definitions

`PASS` تعني أن دليلًا فعليًا قابلًا للتتبع موجود. `BLOCKED` تعني أن التنفيذ توقف بسبب عائق محدد دون نسبة العائق إلى التطبيق. `NOT EVIDENCED` تعني أن الشاشة أو المسار وُجد، لكن الدليل المطلوب غير ظاهر. `NOT RUN` تعني أن الاختبار لم يبدأ عمدًا.

## Validation Matrix

| ID | Capability / Test | Expected | Result | Actual Evidence | Boundary / Note |
|---|---|---|---|---|---|
| EX-01 | Installer launch | Controlled installer launches in Clean VM after hash verification | PASS | Guest `certutil` screenshot `بصمة.png`; SHA matches host `B81DAD92...6019F52`; app launch screenshot `واجهة.png` | One controlled RC installer; no rerun permitted |
| EX-02 | First run / SQLite initialization | App initializes local runtime and SQLite | PASS | `تهيئة بيانات الاختبار الاصطناعية` result in `اهيئة.png`; synthetic organization/circle/group/student/curriculum/unit created | Synthetic only |
| EX-03 | Controlled vertical slice | Synthetic workflow completes | PASS | `تشغيل.png`: `PASS — UI vertical slice completed. Session=1` | Synthetic only |
| EX-04 | Backup / Restore | Local synthetic backup/report verifies and restores | PASS | `نسخواستعادة.png`: local report path and `PASS — Backup/Restore verification` | No production data |
| EX-05 | Restart persistence / search | App reopens and synthetic record remains searchable | PASS | `تجربة2.png`: `TEST DATA ONLY | TEST-STUDENT-UI-001` visible after relaunch | Synthetic only |
| EX-06 | Standard User operation | Workflow runs as non-admin Windows account without UAC | BLOCKED | `حساب3.png`: `vm1` listed under local Administrators; `8.png`: `INACCESSIBLE_BOOT_DEVICE` | Environment/account blocker; not an application FAIL |
| EX-06.1 | Windows non-admin identity | Account is absent from local Administrators | BLOCKED | `net localgroup Administrators` lists `vm1` | No membership changes made |
| EX-06.2 | Clean VM boot | Guest boots normally | BLOCKED | VMware resume/start failure and Windows stop code screenshot | No disk/controller repair performed |
| EX-06.3 | Standard User read/search/edit/report/save | All permitted actions work | NOT RUN | No valid non-admin session after boot failure | Must be retested only with a pre-existing Standard User |
| EX-06.4 | UAC absence during normal operation | No UAC prompt | NOT RUN | No valid EX-06 workflow | Not inferred from prior admin session |
| EX-07 | Upgrade / Uninstall data safety | Independent backup and package lifecycle preserve data | NOT RUN | No external lifecycle evidence accepted | Explicitly deferred |
| AUD-01 | Audit event visibility | Readable events appear in Audit screen | NOT EVIDENCED / BLOCKED | `تجربة4.png`: Audit screen opens but displays connection message without readable events | Independent GAP; not converted to PASS |
| TR-01 | Host→Guest transport | Synthetic fixture copies with matching SHA | PASS | B.4 checkpoint/report; host SHA `678076C5...F3BBDA` and guest match | Read-only share |
| PKG-01 | Installer host artifact | Installer exists and is hash documented | PASS | `build/phase-3.12.12/dist/QuranEducatorGuide-3.12.12-controlled-rc.exe`; manifest and host hash | No execution in this matrix |
| PKG-02 | Upgrade package artifact | Upgrade installer exists and is hash documented | PASS — artifact only | Manifest and host hash `FF23F27A...9563D8` | Does not mean upgrade test passed |
| DATA-01 | Schema foundation | Local entities and constraints exist | IMPLEMENTED / TESTED within code scope | `src/quran_educator/infrastructure/db.py` | Not a production database acceptance claim |
| DATA-02 | Synthetic seed | Seed creates controlled entities without real content | IMPLEMENTED / TESTED within code scope | `src/quran_educator/application/seed.py`, `data/synthetic/fixtures.json` | Synthetic markers required |
| DATA-03 | Runtime database artifacts | Synthetic SQLite and verified restore artifacts exist | PRESENT | `build/phase-3.12.12/smoke-test/UserData/...` database and backup files | Artifact inventory, not new execution |

## Overall Decision

التحقق الخارجي الجزئي ناجح من EX-01 إلى EX-05 ضمن حدود البيانات الاصطناعية، لكنه لا يثبت جاهزية الإنتاج أو الإصدار. EX-06 محجوب بعطل بيئة الإقلاع وبحساب إداري، وEX-07 غير منفذ، وAudit غير مثبت.

## Gates

| Gate | Final Status |
|---|---|
| CONTENT_GATE | LOCKED / NO-GO |
| RELEASE_GATE | LOCKED / NO-GO |
| PRODUCTION_READY | NO |
| RELEASE_READY | NO |
