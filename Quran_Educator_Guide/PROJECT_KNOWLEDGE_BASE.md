# PROJECT_KNOWLEDGE_BASE — دليل المربي القرآني

**المالك:** م/ حسام الجرافي  
**الرؤية:** نظام مكتبي عربي محلي يساعد المؤسسة والمراكز والحلقات والمربين على إدارة الطلاب والحضور والتقدم والمنهج والتقارير بصورة واضحة قابلة للتوسع نحو التحليل الذكي في V2.  
**آخر تحديث:** 2026-08-29T00:22:13.430197+00:00

## النطاق V1

يشمل V1 إدارة المؤسسة والحلقة والمجموعة والطالب والمنهج والحضور (اليوم) والتقدم والملاحظات والتقارير والنسخ الاحتياطي والتدقيق، مع مصادقة محلية وصلاحيات حسب الدور وتشغيل Offline-first. البيانات الحالية للاختبارات فقط وموسومة `TEST DATA ONLY` و`NOT QURAN CONTENT`.

## المعمارية

التطبيق Modular Monolith محلي: `presentation` للواجهات PySide6، `application` للخدمات وحالات الاستخدام والاستعلامات والصلاحيات، `domain` لنماذج المجال وقواعده، و`infrastructure` لـSQLite/SQLAlchemy والمصادقة والهجرات والنسخ والتسجيل والـruntime. نقطة الدخول `src/quran_educator/presentation/app.py`، والمحول `presentation/controller.py`.

## قرارات التصميم

تم الحفاظ على RTL والهوية العربية الملكية، Splash قصيرة ثم Login ثم MainWindow، وواجهات مستقلة داخل QStackedWidget. العرض يستخدم «الحضور (اليوم)» بينما يمكن أن تبقى المعرفات الداخلية التقنية باسم `session`. لا تُعرض بيانات وهمية على أنها فعلية، ولا يُستبدل الـDomain أو Schema بتحسينات شكلية.

## سياسات Quran / Content / Data

لا يُستخدم محتوى قرآني حقيقي أو بيانات طلاب حقيقية في التطوير والاختبارات الحالية. يفتح Content Gate فقط بعد مصدر معتمد وسجل ترخيص/منشأ ومراجعة. البيانات الاصطناعية منفصلة عن production-runtime ولا تُنقل بين البيئتين.

## Domain Model وDatabase Design

الكيانات التي تظهر في `infrastructure/db.py` تشمل Organization وCircle وGroup وStudent وCurriculum وEducationalDomain وCurriculumUnit وStudentAssignment وSession وAttendance وProgressRecord وMentorObservation وAuditEntry وUserAccount وSource. الإنشاء يتم عبر `migrations.initialize_database`، والحفظ عبر SQLAlchemy/SQLite. لا تغيير Schema أو Relations معتمد في هذه الحالة.

## الصلاحيات Authorization

`application/authorization.py` يحتوي `AuthorizationPolicy` و`AuthorizationContext`. الأدوار المحفوظة هي Admin وSupervisor وTeacher وViewer، وتُفحص القدرة قبل العمليات. لا تغيّر semantics المصادقة أو الصلاحيات دون Change Control واختبارات قبل/بعد.

## مسارات التشغيل

`production-runtime` هو مسار التشغيل المحلي الفعلي، و`controlled-runtime` لمسارات Smoke الاصطناعية. يجب ألا تشارك البيئتان قاعدة بيانات أو بيانات. عمليات النسخ والاستعادة في `infrastructure/backup.py`.

## الاختبارات والنتائج

الاختبارات الشاملة السابقة: **88 اختبارًا — PASS**. Smoke Phase 3.13.41 المصحح حقق `status=PASS` و`session_id=1` و`report_exists=true` و`search_count=1` و`backup_restore_verified=true` و`synthetic_only=true` و`offline_only=true`. لم يثبت ذلك Clean VM أو Narrator أو Standard User أو دورة Upgrade/Repair/Uninstall.

## تاريخ المراحل

مراحل 3.12 بنت طبقات البيانات والمجال والتكامل. مراحل 3.13.12–3.13.27 غطت Smoke والتغليف وقيود VM. مراحل 3.13.34–3.13.40 حسنت RTL والهوية والمصادقة والصلاحيات والواجهات. Phase 3.13.41 أنشأت RC مستقلًا مع تعريب الهوية وتحسين Login وSidebar وملف الطالب.

## المشاكل التي حُلّت

تم إصلاح تكرار seed الاصطناعي، توحيد مسار runtime، إضافة المصادقة المحلية scrypt، ربط الجلسة بالصلاحيات، تحسين RTL والتصغير والتكبير، وتوحيد تسمية الحضور إلى «اليوم». كما تم إنشاء نسخة مؤمّنة وتصنيفها وتنظيف caches القابلة لإعادة البناء فقط.

## المشاكل المفتوحة

المراجعة المرئية اليدوية الكاملة وNarrator، اختبار القياسات فعليًا على Windows، Standard User، Clean VM، Upgrade/Repair/Uninstall، واستيراد البيانات الحقيقية بعد اعتماد ملفها ما زالت تتطلب أدلة مستقلة. كما أن شاشة النظام تحتاج لاحقًا إلى تبسيط تدفق البيانات وفق نموذج الاستخدام المرجعي قبل اعتماد V1 النهائي.

## البوابات

```text
CONTENT_GATE = LOCKED / NO-GO
RELEASE_GATE = LOCKED / NO-GO
PRODUCTION_READY = NO
RELEASE_READY = NO
```

## آخر artifacts وSHA-256

| Artifact | SHA-256 |
|---|---|
| One-Folder Phase 3.13.41 | `12b132cf80dd315663b1f4f0c1fa4ba832c1cab6e887fb6311a15420a502d260` |
| Installer Phase 3.13.41 | `b8dde797e43561d99c14535d5fd72f1f312e21bdd201294ab3edb5fb1b86f59c` |

## استئناف العمل

ابدأ من `D:\دليل المربي القرآني`، اقرأ هذا الملف ثم `HANDOFF_TO_ANY_ACCOUNT.md` و`CURRENT_WORK_ORDER.md` و`RESTORE_AND_CONTINUE.md`. أنشئ checkpoint قبل التعديل، واستخدم نسخة عمل مشتقة من `00_MASTER`، ثم شغّل الاختبارات من جذر النسخة مع `PYTHONPATH=...\src`.

## ما لا يُغيّر دون Change Control

Schema، Database Design، Domain Model، Relations، Business Rules، Authentication semantics، Authorization semantics، عزل production-runtime وcontrolled-runtime، حدود Offline-first، ومحتوى Quran/Content وبيانات المستخدمين. كما لا تُستبدل artifacts التاريخية ولا تُفتح البوابات بمجرد نجاح UI أو Smoke.
