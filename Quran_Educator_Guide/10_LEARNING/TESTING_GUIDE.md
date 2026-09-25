# دليل الاختبار

## الاختبارات المثبتة

من جذر نسخة العمل:

```text
set PYTHONPATH=D:\مسار-نسخة-العمل\src
D:\مسار-نسخة-العمل\.venv\Scripts\python.exe -m unittest discover -s tests
```

آخر نتيجة موثقة في المصدر: **88 اختبارًا — OK**. فحص Smoke المصحح يستخدم `build/phase-3.13.41/run_smoke_corrected.ps1` ويعزل `LOCALAPPDATA` في `smoke-runtime-corrected`، ثم يتحقق من status وsession_id وreport_exists وsearch_count وbackup_restore_verified وsynthetic_only وoffline_only.

## حدود الدليل

نتائج المصدر وSmoke لا تثبت Clean VM أو Standard User أو Narrator أو دورة Upgrade/Repair/Uninstall. لا تستخدم نتيجة Smoke قديمة لإثبات artifact جديد.
