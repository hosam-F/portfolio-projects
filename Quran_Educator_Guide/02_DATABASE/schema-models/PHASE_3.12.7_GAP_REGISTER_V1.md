# PHASE 3.12.7 — GAP REGISTER V1

| Gap ID | المجال | المتطلب | الحالة الحالية | المطلوب | الأولوية | الاختبار |
|---|---|---|---|---|---|---|
| GAP-001 | Curriculum | التحقق من ترتيب الوحدات والمعرفات المستقرة ومنع التكرار | الوحدات موجودة، لكن لا يوجد حقل ترتيب صريح ولا اختبار شامل للترتيب | إضافة ترتيب اصطناعي واختبارات العلاقات والتكرار | High | `test_v1_completion.py` |
| GAP-002 | Curriculum | دورة الطالب/الوحدة/التعيين وحالات المنهج | التعيين يعمل ويمنع Archived، لكن تغطية الحالات السلبية غير مكتملة | توسيع اختبارات missing/duplicate/unauthorized/archived | High | `test_v1_completion.py` |
| GAP-003 | Mentor/Session | منع التعديل الحساس بعد الإغلاق وتغطية المسار الكامل | بعض الحدود مختبرة، لكن Progress وAttendance وObservation تحتاج اختبارًا موحدًا | إضافة اختبار workflow موحد بعد الإغلاق | High | `test_v1_completion.py` |
| GAP-004 | Roles | تغطية ADMIN وTEACHER وTRAINEE_TEACHER | توجد اختبارات صلاحيات جزئية، ولا توجد مصفوفة حالات موحدة لكل دور | إضافة اختبارات Allowed/Denied/Denied+Audit دون Role جديدة | High | `test_security_regression.py` |
| GAP-005 | Audit | timestamp وعمليات Backup/Restore | Audit الحالي لا يحتوي timestamp صريحًا، وBackup/Restore لا يكتبان Audit | توثيق timestamp واعتبار الإضافات خارج نطاق آمن إن احتاجت migration؛ عدم الادعاء باكتمالها | Medium | مراجعة كود + اختبار regression |
| GAP-006 | Reporting | Empty/Normal/Large Synthetic Dataset | التقارير الأساسية تعمل، واختبار empty محدود، ولا يوجد large baseline | إضافة اختبارات normal/large اصطناعية وتوثيق القياس | Medium | `test_performance_baseline.py` |
| GAP-007 | Search/Filtering | البحث والتصفية والتنقل | لا توجد خدمة بحث/تصفية مستقلة في البنية الحالية | تنفيذ بحث محلي محدود فقط إذا كانت واجهة البيانات الحالية تدعمه؛ وإلا تسجيله Deferred | Medium | `test_v1_completion.py` أو Deferred |
| GAP-008 | Recovery | missing backup وwrong hash | tamper وmissing manifest مختبران، لكن missing backup وwrong hash منفصلان غير موثقين | إضافة اختبارين سلبيين | High | `test_recovery_full.py` |
| GAP-009 | Performance | baseline لبيانات أكبر | لا توجد قياسات Phase 3.12.6 | إنشاء synthetic dataset محدود وقياس فعلي دون حد مصطنع | Medium | `test_performance_baseline.py` |
| GAP-010 | Windows/Dependencies | تحقق البيئة وتدقيق الاعتماديات | البيئة سبق التحقق منها، لكن Phase 3.12.7 يحتاج سجلًا محدثًا دون تثبيت جديد | تسجيل الإصدارات وrequirements وعدم إضافة حزم | Low | `test_v1_completion.py` |
| GAP-011 | Content/Release | دمج المحتوى والإصدار | محجوبان عمدًا | عدم التنفيذ | N/A | Gate review |
| GAP-012 | Production migration | ترقية متعددة الإصدارات | غير مطلوبة ضمن V1 controlled foundation | إبقاء Production migration = DEFERRED | N/A | Documentation |

## Scope Decision

الفجوات القابلة للإغلاق بأمان في هذه المرحلة هي GAP-001 و002 و003 و004 و006 و008 و009 و010. يبقى GAP-005 جزئيًا لأن تغيير نموذج Audit إلى timestamp قد يتطلب قرار migration صريحًا. يبقى GAP-007 مؤجلًا ما لم تدعم البنية الحالية إضافة محلية صغيرة دون إعادة تصميم UI. أما GAP-011 و012 فهما خارج النطاق أو محجوبان.
