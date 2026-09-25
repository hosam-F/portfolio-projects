# PHASE 3.12.2 PRE-IMPLEMENTATION REVIEW

## Current State

تمتلك Phase 3.12.1 أساسًا تنفيذيًا محدودًا يشمل SQLite/SQLAlchemy وSyntheticStudent وAuditEntry وحاجز القرآن والنسخ والاستعادة والتصدير المحلي. البوابات هي: `DEVELOPMENT_GATE=GO — CONTROLLED / SYNTHETIC DATA ONLY`، و`CONTENT_GATE=NO-GO`، و`RELEASE_GATE=NO-GO`.

## Data Entities Selected

| Entity | Reason/Traceability |
|---|---|
| Organization | FR-001، DATA_MODEL_V1 |
| Circle | FR-001–003 |
| Group | FR-002–003 |
| UserAccount / RoleAssignment | SEC-003، TRAINEE_TEACHER_ROLE_SPEC_V1 |
| Student | FR-004، SEC-001؛ Child تصنيف خصوصية لا كيان بديل |
| Session / Attendance | FR-006، FR-003 |
| Curriculum / CurriculumUnit / EducationalDomain | FR-009، TAX-001–007 |
| Project | FR-019–020، ADR-036 بنطاق محدود |
| Source / Provenance | SRC-001–008، QUR-004؛ Source هو Current Authority بدل Resource |
| AuditEntry | SEC-005، AUDIT_TRAIL_SPEC_V1 |
| BackupRecord | BAK-001–005 |

## Entities Deferred

التفاسير والترجمات والنص القرآني runtime، المراحل المتقدمة للمشاريع، Workflow متعدد المراحل، المحافظ، المزامنة السحابية، بيانات صحية/رسمية/صور/تسجيلات، AI models، والتحليلات المتقدمة مؤجلة أو محظورة وفق V1 scope.

## Source Documents

`DATA_MODEL_V1.md`، `DATA_DICTIONARY_V1.md`، `MODULE_BOUNDARIES_V1.md`، `TRACEABILITY_V1.md`، `REQUIREMENTS.md`، `REQUIREMENT_COVERAGE_MATRIX_V1.md`، `DEVELOPMENT_GATE_V1.md`، `SYNTHETIC_DATA_POLICY_V1.md`، `QURAN_CONTENT_FIREWALL_V1.md`، `AUDIT_TRAIL_SPEC_V1.md`، `PERMISSIONS_PRIVACY_V1.md`.

## Historical Conflicts

يعتمد التنفيذ الحالي `Student` بدل `Child`، و`Source` بدل `Resource`، و`CurriculumUnit` بدل `Unit`، و`EducationalDomain` بدل `CurriculumDomain`. تسجل الأسماء البديلة التاريخية بوصفها `REPLACED_BY` في `DESIGN_CONSISTENCY_REVIEW.md` ولا تنشأ نسخ مزدوجة.

## Risks

الخطر الرئيسي هو اتساع النموذج قبل تثبيت كل العلاقات التنفيذية. لذلك ستنفذ النواة المحلية فقط، مع قيود مفاتيح خارجية وUnique وCheck، ودون محتوى قرآن أو بيانات حقيقية أو ميزات V2. لا يوجد مانع حرج يمنع Data Layer المضبوطة؛ Content وRelease Gates تبقيان مغلقتين.

## Test Plan

اختبارات إنشاء Fresh Database، schema integrity، Foreign Keys، Unique/Check constraints، CRUD والعلاقات، الصلاحيات للأدوار الأساسية، Audit Trail، Synthetic validation، Quran Firewall، Backup/Restore، Offline وعدم وجود شبكة، وإعادة البناء من الصفر.

## Synthetic Data Plan

تستخدم المعرفات `TEST_ORG_001` و`TEST_CIRCLE_001` و`TEST_GROUP_001` و`TEST-STUDENT-001` و`TEST-TEACHER-001` و`TEST-TRAINEE-001` و`TEST-SESSION-001` و`TEST-CURRICULUM-001` و`TEST-PROJECT-001`. كل سجل يحمل دلالة اختبارية ولا يحتوي بيانات شخصية حقيقية أو نصًا قرآنيًا.

## Gate Decision

يسمح بالتوسعة داخل `DEVELOPMENT_GATE` فقط. لا يتغير `CONTENT_GATE` أو `RELEASE_GATE`، ولا يعني نجاح الاختبارات جاهزية إنتاجية.
