# دليل التكامل

## السلسلة الفعلية

GUI → `ControlledAppController` → Application Service/Query Service → `initialize_database` factory → SQLAlchemy/SQLite.

المصادقة في `ProductionEntryDialog` تستخدم `LocalAuthService`، ثم تُنشأ `AuthorizationContext` وتُطبق `AuthorizationPolicy` قبل العمليات المدعومة. `productization.py` يحدد مسارات runtime والتسجيل، بينما `backup.py` يطبق النسخ والتحقق من الاستعادة.

## مثال إضافة طالب

زر «إضافة طالب اصطناعي» في `app.py` يستدعي `_add_student_from_ui`، الذي يقرأ المجموعة والمعرف والاسم، ثم يستدعي `controller.add_student_from_ui`. يتحقق المتحكم من بداية `TEST-` ومن الاسم، ثم يستدعي `StudentDomainService.add_student`، وبعد الحفظ يعاد تحديث نتائج العرض.

## مثال الحضور

مسار الواجهة يحمل معرف اليوم الداخلي `session` للتوافق، بينما النص الظاهر يستخدم «اليوم». يتولى `SessionService` إنشاء اليوم وفتحه وإغلاقه، ويتولى `record_attendance` حفظ حالة الطالب. هذا التعريب لا يغيّر أسماء الكيانات الداخلية.
