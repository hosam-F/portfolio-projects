# مراجعة اتساق التصميم V1

## النتيجة العامة

التصميم متسق في المبادئ الأساسية: Offline-first، القرآن مرجع تأسيسي، provenance، النص القرآني غير قابل للتعديل، الفصل بين مرحلة المربي والدور، وعدم جعل البيانات المشتقة مصدر حقيقة. توجد نقاط تاريخية أو تسمية تحتاج متابعة، وقد سجلت هنا دون محو الوثائق السابقة.

## الملاحظات

| ID | الموضوع | الحالة | المعالجة التوثيقية |
|---|---|---|---|
| CONS-001 | `Resource` مقابل `Source` | تكرار مفاهيمي جزئي | يعتمد `Source` و`SourceEdition` و`ContentProvenance` كسجل موحد، وتبقى `Resource` تسمية قديمة تحتاج ترقية أثناء التنفيذ. |
| CONS-002 | `CurriculumDomain` مقابل `EducationalDomain` | اختلاف تسمية | يستخدم التصميم الجديد `EducationalDomain` كقاموس المجال، مع اعتبار `CurriculumDomain` الاسم التاريخي في الوثائق القديمة. يحتاج ADR تسمية قبل الكود. |
| CONS-003 | `Unit` مقابل `CurriculumUnit` | اختلاف تسمية | يستخدم `CurriculumUnit` في التصميم التفصيلي، و`Unit` اختصار عرضي لا كيان ثانٍ. |
| CONS-004 | `Assessment` مقابل `AssessmentCycle` | ليس تكرارًا | الأول سجل نتيجة/شاهد، والثاني إطار زمني ونوع دورة. |
| CONS-005 | `User Role` مقابل `MentorPathStage` | تعارض محتمل | فصل صريح؛ `TRAINEE_TEACHER` دور تقني ومرحلة النمو مستقلة. |
| CONS-006 | `Dashboard` و`TodayQueue` | مصدر حقيقة مكرر محتمل | كلاهما مشتق من سجلات أصلية ولا يحفظ حقيقة مستقلة. |
| CONS-007 | Approval بلا Reviewer | فجوة حوكمة | تمنع السياسة حالة `APPROVED` بلا مراجع وسبب وتاريخ. |
| CONS-008 | Source بلا License | فجوة حقوق | يمنع النشر أو الاعتماد عند غياب الترخيص أو حالة `PENDING_REVIEW`. |
| CONS-009 | Quran بلا Provenance | فجوة سلامة | لا تعرض آية معتمدة بلا إصدار ومصدر وبصمة وفحص. |
| CONS-010 | Student بلا Privacy Classification | فجوة خصوصية | يضاف مستوى خصوصية لكل سجل طفل وحقول تواصل وملاحظات. |
| CONS-011 | تخزين القرآن الكامل | تعارض تاريخي | المتطلب القديم FR-012 تحفظ صيغته التاريخية، لكن ADR-021 وV1-QUR-003 يعتمدان التخزين الكامل بعد الاعتماد. |
| CONS-012 | المشاريع في V1 | نطاق متباين | الكيان موجود، والمسار المتقدم مؤجل؛ المشروع الأساسي اختياري وفق DEC-3.8-009. |

## مصادر الحقيقة المعتمدة

النص القرآني المصدر هو `QuranTextVersion`/ملف الأصل، والسجلات التعليمية الأصلية هي جلسات وحضور وأداء وتقييم وشواهد، والمحتوى المنشور هو `ContentVersion`، وقرارات المراجعة هي `SourceVerification` و`ContentReview`. التقارير واللوحات والقائمة اليومية قراءات مشتقة.

## ما لم يُصلح

لم تُدمج الأسماء المتعارضة بصمت، ولم تُحذف الكيانات القديمة أو المتطلبات التاريخية، ولم يتحول `PARTIAL` إلى `COVERED`. أي توحيد أسماء في الكود يحتاج ADR وتنفيذ ترحيل مستقل.


## Phase 3.11 — تدقيق الاتساق النهائي

| Conflict | Historical Source | Current Authority | Resolution | Reason | Impact |
|---|---|---|---|---|---|
| مراجع القرآن `HUMAN_REVIEWER_REQUIRED` مقابل مراجع V1 المحدد | مقاطع Phase 3.8 ونسخ سابقة من البوابة | ADR-029 وOPEN-001 النهائي | `SUPERSEDED` للمقطع القديم؛ الحالي م/ حسام الجرافي لـ V1 وتأجيل V2 | قرار صاحب المشروع الأحدث | لا يمنع القرار نفسه، لكن يلزم تنظيف الإحالة القديمة |
| TEACHER_GUIDE_REVIEW_POLICY تقول HUMAN_REVIEWER_REQUIRED | صياغة ما قبل ADR-030 | ADR-030 وTEACHER_GUIDE_REVIEW_POLICY المحدثة | `REPLACED_BY` اعتماد صاحب المشروع للمصنفات الأصلية في V1 | منع تضارب جهة الاعتماد | يلزم اعتبار النص القديم تاريخيًا |
| Source/Resource | DATABASE_DESIGN وSOURCE_REGISTRY | DATA_MODEL_V1 وIP registers | `SUPERSEDED` مفاهيميًا لصالح Source/SourceEdition/Provenance؛ Resource اسم تاريخي | سجل مصدر موحد | يحتاج ADR تسمية قبل التنفيذ |
| CurriculumDomain/EducationalDomain | وثائق قديمة | DATA_MODEL_V1 وCURRICULUM_DESIGN_V1 | `HISTORICAL CONFLICT` مع اعتماد EducationalDomain في التصميم التفصيلي | منع كيانين للمعنى نفسه | يحتاج توحيدًا برمجيًا لاحقًا |
| Unit/CurriculumUnit | وثائق قديمة | DATA_MODEL_V1 | `REPLACED_BY` في التصميم؛ Unit اختصار عرضي | منع تكرار الكيان | أثر على schema المستقبلية |
| Mentor Stage/User Role | وثائق الأدوار القديمة | ADR-024 وTRAINEE_TEACHER_ROLE_SPEC | فصل صريح | منع منح صلاحية من مرحلة النمو | لا تعارض حالي |
| Student/Child | REQUIREMENTS تستخدم Student، وبعض سياسات الخصوصية تستخدم Child | DATA_MODEL_V1 وPERMISSIONS_PRIVACY | Student ككيان تربوي، Child كتصنيف خصوصية لا كيان إضافي | حماية النموذج من التكرار | يجب استخدام Privacy Classification |
| Project/Project Workflow | متطلب FR-019 واسع | ADR-036 وV1_FINAL_SCOPE_AUDIT | `SUPERSEDED` للنطاق المتقدم؛ Project محدود في V1 وworkflow متقدم V2 | عدم تضخيم V1 | بعض التقارير المتقدمة مؤجلة |
| Quran text storage | FR-012 القديم لا تخزين كامل افتراضيًا | ADR-021 وQURAN_SOURCE_POLICY | `SUPERSEDED` بعد اعتماد المصدر؛ التخزين الكامل مشروط ببوابة المصدر | القرار الأحدث أكثر تحديدًا | لا تنفيذ قبل الشروط |
| Backup | وثائق قديمة تترك التلقائي مفتوحًا | ADR-026 وRECOVERY_DRILL_PLAN | Manual + Verified Restore V1؛ التلقائي V2 | اتساق النطاق | Target غير مقاس |
| Export | وثائق قديمة تعرض خيارات عامة | ADR-037 وEXPORT_POLICY | Local-only، مقيد، مؤكد، Audit؛ Cloud Export خارج V1 | الخصوصية وOffline | لا تنفيذ بعد |
| AI | معمارية قديمة تذكر AI Services مستقبلية | ADR-022، AI_ASSISTANCE_POLICY | خارج V1؛ لا اعتماد ولا تعديل ولا إرسال حساس | الحوكمة | واجهات مستقبلية فقط |
| Ownership | صيغ قديمة لا تسمي المالك | ADR-028 وOWNERSHIP_REGISTER | م/ حسام الجرافي صاحب المشروع؛ لا ادعاء قانوني مطلق | تثبيت الحوكمة | التسجيل الرسمي خارج النطاق |
| Licensing | مصدر القرآن قد يبدو كأنه يغطي غيره | ADR-034 وCONTENT_LICENSING_POLICY | كل تفسير/ترجمة/وسيط بسجل وترخيص مستقل | منع انتقال الترخيص بالتخمين | مواد مجهولة BLOCKED |

## الحكم

التعارضات السابقة موثقة ولم تصلح بصمت. المقاطع القديمة تبقى تاريخًا، لكن عند التنفيذ تعتمد أحدث ADR والوثائق المسماة Current Authority. لا يزال توحيد بعض الأسماء يحتاج ADR تنفيذية قبل إنشاء schema.
