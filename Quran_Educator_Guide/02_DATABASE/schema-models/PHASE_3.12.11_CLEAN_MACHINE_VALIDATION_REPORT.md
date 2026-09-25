# PHASE 3.12.11 CLEAN-MACHINE VALIDATION REPORT

## Decision

`CLEAN_MACHINE_VALIDATION = NOT AVAILABLE`.

لم تتوفر بيئة Windows منفصلة لا تحتوي على `D:\quran` أو Python المشروع أو `.venv` أو development tools. لذلك لم يتم الادعاء بأن الاختبار النظيف قد تم.

## Isolated-Package Smoke Test

تم نسخ one-folder package إلى:

`D:\quran\build\phase-3.12.11\smoke-test\Quran Package اختبار`

ثم شُغّل executable من ذلك المسار مع `LOCALAPPDATA` مستقل. نجح `--controlled-smoke` بخروج code 0 ونتيجة PASS، وأنشأ SQLite وتقرير PDF ونسخة backup واستعادة verified، مع `synthetic_only=true` و`offline_only=true`.

## What This Proves

يثبت الاختبار استقلال الحزمة عن working directory الأصلي، وفصل بيانات التشغيل عن package payload، ودعم المسارات التي تحتوي على مسافات ويونيكود، وتشغيل دورة اصطناعية محلية.

## What This Does Not Prove

لا يثبت الاختبار غياب Python وproject source و`.venv` من الجهاز المضيف، ولا يثبت التشغيل على Windows clean machine أو normal non-admin account. لذلك تبقى `CLEAN_MACHINE_VALIDATED = NO` بمعنى غير متحقق، ويُستخدم في التقرير الرسمي التصنيف الأدق `NOT AVAILABLE / NOT TESTED`.

## Normal User

`NORMAL_USER_VALIDATION = NOT TESTED`. تم إثبات writable user-data path عبر `LOCALAPPDATA` في بيئة الاختبار، لكن لم يتم اختبار حساب Windows غير إداري مستقل.
