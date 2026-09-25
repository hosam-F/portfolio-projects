# الحالة الحالية للمشروع — دليل المربي القرآني

**المالك:** م/ حسام الجرافي  
**تاريخ الحالة:** 2026-08-26  
**الهوية:** صُنّاع المربي والمفكر

## الخلاصة التنفيذية

المشروع أصبح تطبيق Windows محليًا قابلًا للتغليف، وقد اجتازت النسخة المثبتة تحت الحساب القياسي `quran_test` تحققًا اصطناعيًا مستقلًا شمل التثبيت وFirst Run وSQLite وcontrolled-smoke والبحث والنسخ والاستعادة. ما يزال التحقق الخارجي على Clean VM محجوبًا؛ فالـVM القديمة وصلت إلى `INACCESSIBLE_BOOT_DEVICE`، وتم إنشاء VM جديدة مستقلة لها دون حذف القديمة أو تعديلها.

## مصفوفة الحالة

| المجال | الحالة | الدليل أو الملاحظة |
|---|---|---|
| التطبيق المحلي | مكتمل وظيفيًا ضمن النطاق المثبت | نتائج Standard User موثقة |
| Installer | PASS في Standard User | SHA-256 موثق في تقرير 3.13.13 |
| First Run | PASS | ظهرت هوية التطبيق العربية |
| SQLite | PASS | قاعدة user-local موجودة بحجم موثق |
| Controlled Smoke | PASS | نتيجة جديدة بقيم Session/Report/Search/Backup/Restore |
| Standard User | PASS | `quran_test` في Users فقط |
| Clean VM القديمة | BLOCKED | `INACCESSIBLE_BOOT_DEVICE` |
| VM الجديدة | PREPARED / NOT INSTALLED | VMDK 32 GB وVMX مستقلان |
| ISO | PRESENT / HASH PENDING | `Win10_22H2_Arabic_x64.iso` موجود محليًا |
| Guest identity/transfer | NOT RUN | يتطلب Guest قابلًا للإقلاع |
| Audit events | NOT EVIDENCED / BLOCKED | لا توجد أدلة مباشرة كافية |
| Upgrade/Repair | NOT RUN | خارج الاختبارات المكتملة |

## القرار الحالي

القرار الأعلى قيمة والأقل مخاطرة هو إكمال تمكين VM الجديدة بالترتيب التالي: التحقق من ISO وبصمته، ثم تثبيت Windows داخل VM الجديدة فقط، ثم تثبيت VMware Tools، ثم إثبات هوية Guest والنقل الاصطناعي ومطابقة SHA-256. يجب إبقاء الـVM القديمة كأثر تشخيصي وعدم حذفها أو إصلاحها عشوائيًا.

لا يبدأ Installer أو التطبيق داخل Guest قبل نجاح الإقلاع والهوية والنقل. ولا يتغير الكود أو Schema أو Domain أو GUI ضمن هذا المسار.

## البوابات

```text
CONTENT_GATE = LOCKED / NO-GO
RELEASE_GATE = LOCKED / NO-GO
PRODUCTION_READY = NO
RELEASE_READY = NO
```

## حدود البيانات

كل الاختبارات التطبيقية المنفذة استخدمت بيانات اصطناعية وآفلة فقط. لا يوجد محتوى قرآني حقيقي أو بيانات شخصية حقيقية ضمن هذا المسار.


## تحديث تنفيذي — 2026-08-26

بناءً على قرار المالك وضيق الوقت، أُوقف اختبار البيئة الوهمية مؤقتًا ولا يُعد شرطًا فوريًا. لقطة VMware للـVM الجديدة أظهرت `SYSTEM THREAD EXCEPTION NOT HANDLED` ورسالة أن نظام الضيف غير مثبت؛ لذلك تبقى `CLEAN_VM = BLOCKED / DEFERRED`، و`GUEST_IDENTITY = NOT RUN`، و`TRANSFER = NOT RUN`. لم يُشغّل Installer أو التطبيق داخل Guest، ولم تُجرَ محاولة إصلاح أو تغيير للإعدادات الجوهرية.

النتيجة العملية الحالية هي اعتماد تحقق Standard User المثبت الموثق كدليل بيئي/تشغيلي محدود للتطبيق فقط، مع عدم فتح بوابات المحتوى أو الإصدار. يمكن لاحقًا استئناف Clean VM بقرار مستقل، لكن ذلك ليس جزءًا من المسار الحالي.


## تحديث QEDS — 2026-08-26

بعد تجميد Artifact المرجعي، بدأ تطبيق QEDS على `presentation/app.py` في نطاق العرض وتجربة الاستخدام فقط. أضيفت tokens بصرية، وتحسينات focus/hover/pressed، صفحات تبويب قابلة للتمرير، أسماء وصول، بطاقات مؤشرات موحدة، وتشغيل البحث عبر Enter، مع تصحيح آمن لخطأ اختيار المؤسسة داخل إنشاء الحلقة. اجتازت ملفات العرض وSmoke orchestration `py_compile`، ونجح UI offscreen smoke في التحقق من العنوان وRTL ووجود 9 تبويبات قابلة للتمرير و7 بطاقات مؤشرات.

الحالة الحالية: `QEDS_SOURCE_PASS = PASS`، `WINDOWS_VISUAL_VERIFICATION = PENDING`، `PACKAGED_REBUILD = NOT RUN`، و`INSTALLER_REBUILD = NOT RUN`. تم الحفاظ على Artifact المجمد السابق، ولم تتغير Schema أو Domain Model أو Database Design أو العلاقات. بقيت Clean VM `BLOCKED / DEFERRED`، وCONTENT_GATE وRELEASE_GATE `LOCKED / NO-GO`، وPRODUCTION_READY وRELEASE_READY = NO.
