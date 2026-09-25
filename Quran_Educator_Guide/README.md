# مستودع دليل المربي القرآني

هذا المستودع نسخة مؤمّنة ومنظمة من المشروع، أُنشئت بالنسخ دون حذف المصدر الأصلي.

## ابدأ من هنا

1. اقرأ `PROJECT_STATE_CURRENT.md` لمعرفة آخر حالة موثقة والقيود.
2. اقرأ `RESTORE_AND_CONTINUE.md` لفتح نسخة عمل من أي حساب Windows.
3. اقرأ `10_LEARNING/ARCHITECTURE_GUIDE.md` ثم `CODE_MAP.md` لفهم الطبقات ومسارات البيانات.
4. اقرأ `10_LEARNING/BUILD_AND_INSTALL_GUIDE.md` قبل البناء.
5. راجع `MANIFEST_ARCHIVE.json` قبل نقل أي artifact أو حذف أي ملف.

## التقسيم

- `00_MASTER`: النسخة المرجعية الكاملة.
- `01_SOURCE`: نسخة منظمة من presentation/domain/application/infrastructure/services/config.
- `02_DATABASE`: ملفات وقاعدة البيانات والوثائق المرتبطة بها.
- `03_PRESENTATION`: واجهات PySide6 والأصول والـthemes.
- `04_INTEGRATION`: المصادقة والصلاحيات والـruntime والخدمات.
- `05_TESTS`: اختبارات المشروع.
- `06_INSTALLER`: التغليف والـInstaller والبصمات.
- `07_DOCUMENTATION`: تقارير المراحل والسياسات والتتبعية.
- `08_EVIDENCE`: checkpoints وlogs وJSON ونتائج الاختبارات.
- `10_LEARNING`: أدلة التطوير المستخرجة من المشروع.
- `11_RELEASE`: حزم التسليم السابقة والـhandoff.
- `12_BACKUP`: النسخ الاحتياطية والمواد المرتبطة بها.

لا تُعدّل `00_MASTER` مباشرة قبل إنشاء checkpoint، ولا تستخدم بيانات حقيقية أو محتوى قرآني غير موثق.
