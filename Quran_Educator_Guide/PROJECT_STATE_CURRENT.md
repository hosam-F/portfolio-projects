# PROJECT_STATE_CURRENT — دليل المربي القرآني

**آخر حالة موثقة:** Phase 3.13.40، مع وجود Release Candidate مستقل Phase 3.13.41 مبني لاحقًا.  
**المالك:** م/ حسام الجرافي  
**المعمارية:** تطبيق Windows محلي Offline-first باستخدام Python وPySide6 وSQLite وSQLAlchemy وReportLab، بنمط Modular Monolith.  
**تاريخ إنشاء النسخة:** 2026-08-28T22:25:27.159265+00:00

## حالة المشروع

المصدر والاختبارات والوثائق وأدلة التتبع والـartifacts محفوظة في `00_MASTER`. توجد نسخة RC مستقلة في `11_RELEASE`، ونسخ التغليف في `06_INSTALLER`. تم الحفاظ على المعرف التقني الداخلي `QuranEducatorGuide.exe`، مع تعريب الهوية المرئية إلى «دليل المربي القرآني» و«صُنّاع المربي والمفكر» حيث أمكن.

اجتازت النسخة السابقة اختبارات المصدر الشاملة البالغة 88 اختبارًا، كما اجتاز Smoke الحالي الخاص بـPhase 3.13.41 بعد تصحيح أداة اكتشاف النتيجة. يبقى التحقق المرئي اليدوي وNarrator ودورة Installer/Upgrade/Repair/Uninstall من متطلبات الاعتماد الخارجي.

## القرارات المحفوظة

| المجال | القرار |
|---|---|
| البيانات | اصطناعية فقط حتى فتح Content Gate رسميًا |
| التشغيل | production-runtime منفصل عن controlled-runtime |
| المصادقة | حسابات محلية وكلمات مرور مجزأة، دون إرسال خارجي |
| الصلاحيات | AuthorizationPolicy وAuthorizationContext محفوظان |
| Schema / Domain / Relations | لا تغيير موثق في هذه الجولة |
| الحضور | العرض العربي يستخدم «الحضور (اليوم)»، مع بقاء المعرفات الداخلية التقنية |
| الأرشفة | النسخ الحالية غير تدميرية، ولا حذف تم في هذه العملية |

## البوابات

```text
CONTENT_GATE = LOCKED / NO-GO
RELEASE_GATE = LOCKED / NO-GO
PRODUCTION_READY = NO
RELEASE_READY = NO
```

## ما لم يثبت بعد

لا تثبت هذه النسخة نجاح Clean VM أو Standard User أو Upgrade أو Repair أو Uninstall أو Narrator. لا تثبت البصمة وحدها سلامة السلوك التشغيلي.
