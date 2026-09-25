# Change Proposal 3.13.39 — المصادقة والبيانات الإنتاجية المحلية

## النطاق

ينفذ هذا الاقتراح حسابات محلية باسم مستخدم وكلمة مرور، وصلاحيات دورية ونطاقية، وسجل جلسات، وإدارة قفل الحساب، وواجهة دخول عربية، ووضع `LOCAL_PRODUCTION` منفصلًا عن `CONTROLLED_SYNTHETIC`، ومعالج استيراد حقيقي قابل للمعاينة والتراجع. لا يشمل هذا الاقتراح اتصالًا شبكيًا أو خدمة سحابية أو تكامل ذكاء اصطناعي أو حذفًا للبيانات التاريخية.

## التغييرات المتوقعة

| الطبقة | التغيير |
|---|---|
| Infrastructure | جداول أو أعمدة الحساب والجلسة والتدقيق وسجل الاستيراد، مع Migration صريحة |
| Domain | عقود Account وRole وPermission وSession وImportResult، دون ربط بـQt |
| Application | AuthService وPermissionService وImportService وAuditService |
| Presentation | LoginView وAccountAdminView وPermission-aware navigation وImportPreviewView |
| Reporting | قاموس عربي موحد وهوية المستخدم والنطاق وحالة الوضع |
| Backup | نسخة قبل Migration والاستيراد مع تحقق واستعادة |

## شروط البدء

يلزم اعتماد خوارزمية تجزئة كلمة المرور، الأدوار والنطاقات، سياسة القفل، سياسة الاحتفاظ والخصوصية، صيغة الاستيراد، ومكان قاعدة الإنتاج. يلزم أيضًا Backup مستقل مثبت hash، ونسخة اختبار منفصلة، وcheckpoint قبل Migration.

## معايير القبول

ينجح التصميم عند إثبات إنشاء الحساب دون كلمة مرور صريحة، نجاح وفشل الدخول، قفل الحساب وإلغاء القفل، تغيير كلمة المرور، تسجيل الخروج، منع الصلاحية غير المسموحة، ظهور Audit Event، معاينة استيراد صحيحة، رفض صف غير صالح، rollback، backup/restore، وفصل تقارير الإنتاج عن Fixtures الاصطناعية.

## Stop Conditions

توقف التنفيذ عند غياب Backup، أو غموض مصدر البيانات، أو محاولة تسجيل كلمة مرور، أو خلط قاعدة الإنتاج مع قاعدة Smoke، أو ظهور حاجة لتغيير علاقات غير معتمد، أو فشل rollback. لا تُعالج المشكلة بحذف الجداول أو تعطيل القيود.

## الحالة

`PROPOSAL_STATUS = READY FOR OWNER FIELD-LEVEL REVIEW`  
`IMPLEMENTATION = NOT STARTED`  
`REAL_DATA_IMPORT = NOT STARTED`  
`CONTENT_GATE = LOCKED / NO-GO`  
`RELEASE_GATE = LOCKED / NO-GO`
