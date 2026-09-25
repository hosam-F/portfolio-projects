# دليل الواجهة

## التدفق

`WelcomeSplash` قصيرة، ثم `ProductionEntryDialog`، ثم `MainWindow`. الاسم المرئي الرسمي هو «دليل المربي القرآني» والهوية الفرعية «صُنّاع المربي والمفكر».

## المسارات الحالية

| route | العنوان الظاهر | View |
|---|---|---|
| dashboard | لوحة البداية | DashboardView |
| organization | المؤسسة والحلقة | OrganizationView |
| students | الطلاب | StudentsView |
| curriculum | المنهج | CurriculumView |
| attendance | الحضور (اليوم) | AttendanceView |
| progress_observation | التقدم والملاحظة | ProgressObservationView |
| reports | التقارير | ReportsView |
| audit | التدقيق | AuditView |
| backup_restore | النسخ والاستعادة | BackupRestoreView |

`ViewRouter` يربط route بـ`QStackedWidget`، و`PersistentNavigation` يربط أزرار Sidebar بالإشارة `routeSelected`. كل View تُبنى داخل إطار مستقل واتجاه RTL.

## قواعد العرض

الألوان والبطاقات والأزرار معرفة مركزيًا في `_apply_visual_identity` داخل `app.py`. عناصر الوصول تستخدم `AccessibleName` و`AccessibleDescription`. بيانات الفراغ يجب أن تشرح الإجراء التالي ولا تعرض بيانات حقيقية أو وهمية على أنها فعلية.
