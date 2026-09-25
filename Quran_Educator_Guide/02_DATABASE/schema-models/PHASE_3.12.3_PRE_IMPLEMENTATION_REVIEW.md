# PHASE 3.12.3 PRE-IMPLEMENTATION REVIEW

## Current State

توجد طبقة بيانات محلية مضبوطة في Phase 3.12.2 تشمل كيانات V1 الأساسية، وDevelopment Gate يسمح بالتنفيذ ببيانات اصطناعية فقط. Content Gate وRelease Gate مغلقتان.

## Existing Domain Models

Student، Organization، Circle، Group، UserAccount، RoleAssignment، Session، Attendance، Curriculum، EducationalDomain، CurriculumUnit، Project، Source، Provenance، AuditEntry، BackupRecord، SchemaVersion.

## Existing Services

StudentService وExportService، وحاجز QuranContentFirewall، وManual Backup/Restore Foundation، وSynthetic Seed.

## Required Services

| Service | Scope |
|---|---|
| CircleService | إنشاء/تعديل/تعطيل الحلقة، إسناد المجموعة والمعلم، إضافة الطالب |
| StudentService | إنشاء/تعديل/نقل/تعطيل الطالب الاصطناعي |
| SessionService | إنشاء/فتح/إغلاق الحصة وتسجيل الحضور |
| CurriculumService | إنشاء/تعديل/تنشيط المجال والوحدة والإسناد |
| ProjectService | المشروع المحدود في V1 فقط |
| ProgressService | تجريد تقدم الحفظ والمراجعة بلا نص قرآن |
| TeacherService | الملف والإسناد والشاهد والتأمل والتقدم الوصفي |
| AuthorizationService | ADMIN/TEACHER/TRAINEE_TEACHER والحد الأدنى |
| AuditService | تسجيل العمليات الحساسة والرفض |

## Deferred Services

التفسير والترجمة والنص القرآني runtime، الاعتماد الشرعي، AI، إدارة المشاريع المتقدمة، Cloud، التقارير الكاملة، workflow المتعدد، والمراحل V2.

## Requirements Mapping

FR-001–009 وFR-013 وFR-019–021 وSEC-001/003/005 وBAK-001–005 وQUR-002–005 وMNT-001–005 ترتبط بالخدمات المختارة. لا يدعي هذا النطاق تنفيذ جميع متطلبات V1.

## Acceptance Criteria Mapping

ترتبط الخدمات بـ `TC-CIR-001` و`TC-STU-001` و`TC-ATT-001` و`TC-LESSON-001` و`TC-CUR-001` و`TC-MENT-001/002` و`TC-ROLE-001` و`TC-AUDIT-001` و`TC-QUR-001–004` مع حالات نجاح وفشل وصلاحيات.

## Test Plan

لكل خدمة: Happy Path وInvalid Input وUnauthorized Case، مع التحقق من الحالة والعلاقات والتكرار والتدقيق، وببيانات TEST فقط. يضاف اختبار منع تعديل الجلسة المغلقة ومنع TRAINEE_TEACHER من العمليات الحساسة.

## Risks

أهم المخاطر هي تضخم قواعد العمل، وخلط مرحلة المربي مع الدور، ومحاولة تمثيل نص القرآن بدل metadata، وتكرار Authorization/Audit داخل الخدمات. ستبقى القواعد في Application Services وحواجز المصدر مركزية.

## Historical Conflicts

تستخدم الخدمات `Student` و`Source` و`CurriculumUnit` و`EducationalDomain` وفق Current Authority. الأسماء التاريخية `Child/Resource/Unit/CurriculumDomain` تبقى `REPLACED_BY` ولا تنشأ لها خدمات أو كيانات مكررة.

## Gate Decision

لا يوجد مانع حاكم يمنع هذه الشريحة الاصطناعية. `DEVELOPMENT_GATE=GO — CONTROLLED / SYNTHETIC DATA ONLY`، و`CONTENT_GATE=NO-GO`، و`RELEASE_GATE=NO-GO`. لا تستخدم الخدمات نصًا قرآنيًا أو بيانات حقيقية.
