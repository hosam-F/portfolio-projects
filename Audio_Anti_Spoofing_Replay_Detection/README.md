# Audio Anti-Spoofing — Replay Detection

مشروع أكاديمي صغير لاكتشاف التسجيلات المعاد تشغيلها من ملفات WAV. خط المعالجة هو:

`WAV → preprocessing → MFCC → StandardScaler → SVM → GENUINE / REPLAY`

## البيانات

يستخدم التنفيذ المحلي **ASVspoof 2017 Version 2 — Development Set** الموجود داخل `data/raw/`. تم استخدام الـProtocol الرسمي الموجود في:

`data/metadata/protocol_official/extracted/protocol_V2/ASVspoof2017_V2_dev.trl.txt`

لم يتم استخدام ASVspoof 2019 أو Dataset خارجية.

## Structure

- `app/`: واجهة Tkinter.
- `src/`: المعالجة الصوتية، MFCC، التدريب، التقييم، والتنبؤ.
- `data/raw/`: ملفات WAV الأصلية المحلية.
- `data/metadata/`: Protocol الرسمي المستخدم.
- `models/`: النموذج المحفوظ.
- `results/`: المقاييس والتنبؤات والرسم النهائي.
- `notebooks/`: Notebook التعليمي.
- `docs/`: وثائق المشروع.

## الخصائص والنموذج

يُحوّل كل ملف صوتي إلى 80 خاصية: متوسط وانحراف MFCC، ومتوسط وانحراف Delta MFCC. معدل العينة 16 kHz، و`n_mfcc=20`، و`n_fft=512`، و`hop_length=256`، مع صوت mono وتطبيع deterministic. النموذج هو SVM بنواة RBF مع `StandardScaler` و`class_weight=balanced` و`random_state=42`.

النموذج المحفوظ: `models/svm_mfcc.joblib`

## التقييم الفعلي

تم استخدام 1710 ملفًا معنونة رسميًا، مع تقسيم stratified ثابت بنسبة 80/20:

| العنصر | القيمة |
|---|---:|
| عينات التدريب | 1368 |
| عينات الاختبار | 342 |
| Genuine في الاختبار | 152 |
| Replay في الاختبار | 190 |
| Accuracy | 0.979532 |
| Precision لـ Replay | 0.969231 |
| Recall لـ Replay | 0.994737 |
| F1 لـ Replay | 0.981818 |

مصفوفة الالتباس بترتيب `[GENUINE, REPLAY]`:

`[[146, 6], [1, 189]]`

النتائج التفصيلية في `results/metrics/metrics.json` والتنبؤات في `results/predictions/predictions.csv`.

## تشغيل الواجهة على Windows

انقر مرتين على:

`run.bat`

يتحقق الملف أولًا من وجود بيئة محلية داخل المشروع، ثم يبحث عن Python متوافق من PATH أو من مواقع Python المحلية الشائعة. يرفض الإصدارات الأقدم من Python 3.10 ولا يحتاج إلى `conda activate`.

يمكن أيضًا التشغيل من Terminal من داخل مجلد المشروع بعد تثبيت Python 3.12 والاعتماديات:

```text
python app\demo.py
```

ثم اختر ملف WAV صالحًا واضغط **اختيار ملف صوتي**. الواجهة تنفذ Prediction حقيقيًا باستخدام النموذج المحفوظ ولا تعيد التدريب عند فتحها.

## حدود المشروع

النتيجة تخص Replay Spoofing Detection وليست Speaker Verification كاملًا. الأداء المقاس على Development Set ولا يضمن الأداء على تسجيلات أو أجهزة تسجيل جديدة. يمكن لاحقًا دراسة ASVspoof 2019 PA، وخصائص صوتية إضافية، ونماذج أعمق، لكن هذه العناصر خارج التنفيذ الحالي.
