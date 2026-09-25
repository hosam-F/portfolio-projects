# DATA MODEL IMPLEMENTATION NOTES V1

## Current Authority

تم تنفيذ طبقة البيانات وفق `DATA_MODEL_V1.md` و`DATA_DICTIONARY_V1.md` ضمن نطاق Phase 3.12.2 المضبوط. لم تنشأ نسخ مزدوجة من الأسماء التاريخية.

| Historical Name | Current Authority | Status |
|---|---|---|
| Child | Student | `REPLACED_BY`؛ Child تصنيف خصوصية لا كيان بديل |
| Resource | Source | `REPLACED_BY` |
| Unit | CurriculumUnit | `REPLACED_BY` |
| CurriculumDomain | EducationalDomain | `REPLACED_BY` في التنفيذ الحالي |
| Project Workflow | Project المحدود | Workflow المتقدم مؤجل V2 |

## Implemented Entities

Organization، Circle، Group، UserAccount، RoleAssignment، Student، Session، Attendance، Curriculum، EducationalDomain، CurriculumUnit، Project، Source، Provenance، AuditEntry، BackupRecord، SchemaVersion.

## Constraints

فعّلت SQLite Foreign Keys، وUnique identifiers، وCheck constraints للأدوار والحضور وحالة المشروع وحالة المصدر وحالة النسخ، وفهارس للمفاتيح الشائعة. جميع fixtures اصطناعية.

## Limitations

هذا نموذج تنفيذ تأسيسي وليس schema إنتاجيًا نهائيًا. لم تنفذ migrations ترقية متعددة؛ يوجد Migration Foundation لإعادة البناء من الصفر وتسجيل version. لم يطبق النص القرآني runtime ولم يضف محتوى خارجي.
