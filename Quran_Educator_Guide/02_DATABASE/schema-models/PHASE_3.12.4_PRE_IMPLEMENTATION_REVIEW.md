# PHASE 3.12.4 PRE-IMPLEMENTATION REVIEW

## Current State

توجد طبقة بيانات وخدمات نطاق مضبوطة، وDevelopment Gate مفتوحة للتطوير الاصطناعي فقط. الهدف الحالي هو Vertical Slice محلي من المؤسسة إلى التحقق بعد الاستعادة. Content Gate وRelease Gate مغلقتان.

## Required Extensions

تحتاج الشريحة إلى حالة المنهج، وتعيين الطالب إلى الوحدة، وحالة الحصة، وسجل التقدم metadata-only، وملاحظة المربي، مع قواعد انتقال وتدقيق ونسخ واستعادة.

## Existing Authorities

`DATA_MODEL_V1.md` و`DATA_DICTIONARY_V1.md` و`DOMAIN_SERVICES_DESIGN_NOTES_V1.md` و`PERMISSIONS_PRIVACY_V1.md` و`AUDIT_TRAIL_SPEC_V1.md` هي مراجع التصميم. لا يضاف Role جديد؛ الأدوار الحالية هي ADMIN وTEACHER وTRAINEE_TEACHER، ويظهر Mentor كمصطلح وظيفي لا Role جديدة.

## Workflow Scope

Organization → Circle → Group → Teacher → Student → Curriculum → CurriculumUnit → Assignment → Session → Attendance → Progress → Observation → Close → Audit → Backup → Restore → Verify.

## State Machines

Curriculum: `DRAFT → ACTIVE → ARCHIVED` فقط. Session: `DRAFT → OPEN → CLOSED` فقط. لا يسمح بالتعديل العادي بعد ARCHIVED أو CLOSED.

## Synthetic Data Boundary

كل identifiers تبدأ بـ `TEST-` أو `TEST_`. لا قرآن، لا آيات، لا تفسير، لا ترجمة، لا صوت، لا صور، ولا بيانات شخصية حقيقية.

## Test Plan

سيشمل اختبارًا عموديًا واحدًا كاملًا، واختبارات دورة المنهج والتعيين، وانتقالات الحالة، والحضور، والتقدم بقيم 0/25/50/75/100، وملاحظة المربي، ورفض التعديل بعد الإغلاق، وتفويض الأدوار، وAudit، وBackup/Restore/Verification.

## Risks and Blockers

الخطر الرئيسي هو إضافة قواعد غير موثقة أو خلط Mentor بـ Role. لذلك سيستخدم التنفيذ metadata وصفية فقط، وسيظل مصدر الحقيقة في Data Layer، وسيبقى حاجز القرآن مغلقًا.

## Gate Decision

لا يوجد مانع لتوسيع الشريحة الاصطناعية. لا تتغير `LEGACY_GLOBAL_GATE` أو `CONTENT_GATE` أو `RELEASE_GATE`. لا يجوز استنتاج اكتمال V1 أو جاهزية Production من نجاح Vertical Slice.
