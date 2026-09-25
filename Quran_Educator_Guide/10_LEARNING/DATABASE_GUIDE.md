# دليل قاعدة البيانات

**الملفات الفعلية:** `src/quran_educator/infrastructure/db.py` و`migrations.py` و`backup.py`.  
**قاعدة البيانات:** SQLite محلية، ويُنشئ `initialize_database(database_path)` factory اتصال SQLAlchemy.

## الكيانات الظاهرة في المتحكم

`Organization` للمؤسسة، `Circle` للحلقة، `Group` للمجموعة، `Student` للطالب، `Curriculum` للمنهج، `EducationalDomain` للمجال، `CurriculumUnit` للوحدة، `StudentAssignment` للإسناد، `Session` لليوم/السجل الداخلي، `Attendance` للحضور، `ProgressRecord` للتقدم، `MentorObservation` للملاحظة، `AuditEntry` للتدقيق، و`UserAccount` للحساب المحلي.

## التسلسل التشغيلي

المؤسسة تحتوي مراكز/حلقات بحسب النموذج الحالي، والحلقة ترتبط بالمجموعات والطلاب عبر الخدمات. لا تُنشأ صفوف واجهة وهمية؛ `list_records` و`student_options` يقرآن من SQLite. بيانات Smoke موسومة بمعرفات `TEST-*` و`is_synthetic=True`.

## النسخ الاحتياطي

مسار النسخ والاستعادة يمر عبر `infrastructure/backup.py`، وتتحقق اختبارات Smoke من `backup_restore_verified`. لا تنسخ production-runtime إلى controlled-runtime.
