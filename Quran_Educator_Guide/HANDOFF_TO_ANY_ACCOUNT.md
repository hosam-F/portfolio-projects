# HANDOFF_TO_ANY_ACCOUNT — دليل المربي القرآني

## المسار

انسخ المجلد الكامل `D:\دليل المربي القرآني` إلى قرص تتوفر فيه مساحة كافية. النسخة المرجعية داخل `00_MASTER`، والمصدر الأصلي المحفوظ هو `D:\quran`.

## خطوات البدء من حساب Windows آخر

1. انسخ المجلد كاملًا، ولا تنقل ملفات منفردة.
2. افتح `PROJECT_KNOWLEDGE_BASE.md` ثم `PROJECT_STATE_CURRENT.md`.
3. تحقق من `MANIFEST_ARCHIVE.json` ومن SHA-256 للـOne-Folder والـInstaller قبل النقل.
4. انسخ `00_MASTER` إلى مجلد عمل منفصل، ولا تعدل النسخة المرجعية مباشرة.
5. تحقق من Python 3.12 وبيئة `.venv`، ثم عيّن `PYTHONPATH` إلى `src`.
6. شغّل اختبارات `tests` قبل أي تعديل.
7. استخدم `controlled-runtime` للبيانات الاصطناعية فقط، ولا تخلطها مع `production-runtime`.
8. أنشئ checkpoint وسجل قرار عند أي تغيير معماري أو في قاعدة البيانات.

## قاعدة الأمان

لا تضع كلمات المرور داخل الملفات أو الأوامر، ولا تستخدم Administrator لإثبات Standard User. لا تستورد بيانات حقيقية أو محتوى قرآني غير موثق. لا تحذف VM أو قاعدة بيانات أو artifact قبل مراجعة Manifest وموافقة مستقلة.

## أول قراءة

`PROJECT_KNOWLEDGE_BASE.md` ← `CURRENT_WORK_ORDER.md` ← `10_LEARNING/ARCHITECTURE_GUIDE.md` ← `10_LEARNING/CODE_MAP.md` ← `RESTORE_AND_CONTINUE.md`.
