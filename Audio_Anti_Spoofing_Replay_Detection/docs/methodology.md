# Methodology

## Scope

المهمة هي **Replay Spoofing Detection**: تصنيف ملف WAV إلى `GENUINE` أو `REPLAY`. لا ينفذ المشروع Speaker Verification ولا يستخدم Deep Learning أو خدمات خارجية.

## Pipeline

يُقرأ الصوت mono ويُعاد أخذ عيناته إلى 16 kHz، ثم يُطبّع. تُستخرج 20 MFCC مع `n_fft=512` و`hop_length=256`. تُستخدم المتوسطات والانحرافات المعيارية لـ MFCC وDelta MFCC، فينتج متجه من 80 قيمة. بعد ذلك يُطبّق `StandardScaler` ثم SVM بنواة RBF مع موازنة الفئات.

## Reproducibility

استخدمت التجربة Protocol الرسمي لـ ASVspoof 2017 V2 Development Set، وتقسيمًا stratified بنسبة 80/20 وبقيمة `random_state=42`. أُعيد حفظ النموذج في `models/svm_mfcc.joblib`، وتستخدم الواجهة نفس دالة MFCC ونفس النموذج المحفوظ.

## Limitations

التقييم محلي وعلى Development Set؛ لذلك لا يمثل ضمانًا لتسجيلات أو أجهزة جديدة. لم تُستخدم ASVspoof 2019 أو تقنيات مستقبلية ضمن التنفيذ الحالي.
