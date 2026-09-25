# قاموس البيانات المنطقي لـ V1

> هذا قاموس تصميمي غير تنفيذي. لا ينشئ مخطط SQLite.

## الحقول المشتركة

| Entity | Field | المعنى | النوع المنطقي | الإلزام | الخصوصية | مشتق؟ | قابل للتعديل |
|---|---|---|---|---|---|---|---|
| جميع السجلات | id | معرف ثابت | Identifier | نعم | داخلي | لا | لا |
| جميع السجلات | created_at | وقت الإنشاء | DateTime | نعم | داخلي | لا | لا |
| جميع السجلات | updated_at | آخر تعديل | DateTime | نعم | داخلي | لا | نعم عبر سجل |
| جميع السجلات | status | حالة دورة الحياة | Enum | نعم | داخلي | لا | بصلاحية |
| جميع السجلات | archived_at | وقت الأرشفة | DateTime | لا | داخلي | لا | بصلاحية |
| السجلات التعليمية | event_date | تاريخ الحدث التربوي | Date | حسب السجل | داخلي | لا | لا بعد النشر إلا بتدقيق |
| السجلات الحساسة | author_id | منشئ السجل | Identifier | نعم | حساس | لا | لا |
| السجلات المصدرية | provenance_id | سلسلة الأصل | Identifier | حسب المصدر | حساس | لا | لا بعد الاعتماد |

## هوية الحلقة والطالب

| Entity | Field | المعنى | النوع المنطقي | الإلزام | القيمة الافتراضية | التحقق | الخصوصية | مشتق؟ | التعديل |
|---|---|---|---|---|---|---|---|---|---|
| Organization | display_name | اسم النطاق المحلي | Text | نعم | — | غير فارغ | داخلي | لا | نعم |
| Circle | organization_id | مالك الحلقة | Identifier | نعم | — | نطاق موجود | داخلي | لا | لا |
| Circle | name | اسم الحلقة | Text | نعم | — | غير فارغ | داخلي | لا | نعم |
| Group | circle_id | الحلقة | Identifier | نعم | — | موجودة | داخلي | لا | لا |
| Group | name | اسم المجموعة | Text | نعم | — | غير فارغ | داخلي | لا | نعم |
| Person | display_name | الاسم المعروض | Text | نعم | — | أقل بيانات | شخصي | لا | بصلاحية |
| Student | person_id | الشخص المرتبط | Identifier | نعم | — | Person موجود | شخصي | لا | لا |
| Student | age_stage_id | المرحلة العمرية | Identifier | لا | UNKNOWN | قاموس معتمد | تربوي | لا | نعم |
| GuardianLink | student_id | الطالب | Identifier | نعم | — | طالب موجود | حساس | لا | بصلاحية |
| GuardianLink | contact_value | وسيلة تواصل عند الحاجة | Text | لا | — | موافقة/حاجة | حساس جدًا | لا | بصلاحية |

## القرآن والمصدر

| Entity | Field | المعنى | النوع المنطقي | الإلزام | التحقق | الخصوصية | مشتق؟ | التعديل |
|---|---|---|---|---|---|---|---|---|
| QuranTextVersion | provider | مزود النص | Text | نعم | Tanzil في V1 | عام/حقوق | لا | لا بعد الاعتماد |
| QuranTextVersion | text_type | نوع النص | Enum | نعم | Uthmani | عام | لا | لا |
| QuranTextVersion | version | إصدار المصدر | Text | نعم | 1.1 في V1 | عام | لا | لا |
| QuranTextVersion | source_url | رابط المصدر | URL | نعم | HTTPS/مصدر رسمي | عام | لا | لا |
| QuranTextVersion | license | الترخيص | Text | نعم | سجل منفصل | حقوق | لا | لا بعد الاعتماد |
| QuranTextVersion | download_date | تاريخ التنزيل | DateTime | نعم عند التنزيل | تاريخ صحيح | داخلي | لا | لا |
| QuranTextVersion | original_sha256 | بصمة الملف الأصلي | Hash | نعم | SHA-256 | سلامة | لا | لا |
| QuranTextVersion | review_status | حالة المراجعة | Enum | نعم | PROPOSED/PENDING_REVIEW/APPROVED | سلامة | لا | بمراجع |
| QuranTextVersion | human_reviewer_id | المراجع البشري | Identifier | عند الاعتماد | مراجع مخول | حساس | لا | لا |
| QuranVerse | text | النص القرآني | Immutable Text | نعم | قراءة فقط، لا تصحيح صامت | ديني/حقوق | لا | لا |
| QuranVerse | surah_number | رقم السورة | Integer | نعم | نطاق معروف | عام | لا | لا |
| QuranVerse | ayah_number | رقم الآية | Integer | نعم | موجب وفريد ضمن السورة | عام | لا | لا |
| QuranIntegrityCheck | result | نتيجة الفحص | Enum | نعم | PASS/FAIL | سلامة | لا | لا |
| Source | title | عنوان المصدر | Text | نعم | غير فارغ | عام | لا | نعم قبل الاعتماد |
| Source | source_level | عائلة المصدر | Enum | نعم | شرعي/تراثي/حديث | عام | لا | بمراجعة |
| Source | trust_level | موقع الاستخدام 0–5 | Integer | لا | 0..5 | عام | لا | بمراجعة |
| SourceVerification | decision_reason | سبب قرار المراجعة | Text | نعم عند القرار | غير فارغ | حساس | لا | لا بعد الإغلاق |

## المنهج والنشاط

| Entity | Field | المعنى | النوع المنطقي | الإلزام | المصدر | الخصوصية | مشتق؟ | التعديل |
|---|---|---|---|---|---|---|---|---|
| CurriculumVersion | version_label | اسم الإصدار | Text | نعم | قرار نشر | عام | لا | لا بعد النشر |
| AgeStage | name | اسم المرحلة | Text | نعم | Seed/قرار | عام | لا | نعم بإصدار |
| EducationalDomain | name | اسم المجال | Text | نعم | Taxonomy | عام | لا | نعم بإصدار |
| EducationalDomain | aspect | الجانب الأعلى | Enum | نعم | Taxonomy | عام | لا | نعم بإصدار |
| CurriculumUnit | title | عنوان الوحدة | Text | نعم | محتوى معتمد | عام | لا | عبر إصدار |
| Objective | statement | صياغة الهدف | Text | نعم | محتوى | عام | لا | عبر إصدار |
| Activity | duration_minutes | المدة | Integer | لا | تصميم النشاط | عام | لا | نعم |
| Activity | difficulty | الصعوبة | Enum | لا | Seed/مراجعة | عام | لا | نعم |
| Activity | expected_output | الناتج المتوقع | Text | نعم | تصميم النشاط | عام | لا | نعم بإصدار |
| Activity | status | دورة النشاط | Enum | نعم | Draft/Review/Approved/Retired | عام | لا | بمراجعة |
| AssessmentCycle | cycle_type | نوع الدورة | Enum | نعم | Seed | عام | لا | نعم |
| Assessment | evidence | الشاهد | Text/Reference | لا | الملاحظة/العمل | حساس | لا | بصلاحية |

## المتابعة ومسار المربي

| Entity | Field | المعنى | النوع المنطقي | الإلزام | الخصوصية | مشتق؟ | التعديل |
|---|---|---|---|---|---|---|---|
| LessonSession | planned_content_id | محتوى الخطة | Identifier | لا | داخلي | لا | لا بعد الإغلاق |
| LessonSession | completed_summary | ما تم | Text | لا | داخلي | لا | نعم قبل الإغلاق |
| LessonSession | next_step | المتابعة التالية | Text | لا | داخلي | لا | نعم |
| TeacherReflection | what_worked | ما نجح | Text | لا | حساس | لا | نعم |
| TeacherReflection | proposed_change | التغيير المقترح | Text | لا | حساس | لا | نعم |
| MentorPathStage | code | رمز مرحلة النمو | Text | نعم | عام | لا | عبر إصدار |
| TeacherTrainingUnit | completion_status | حالة الإتمام | Enum | نعم | داخلي | لا | بصلاحية |
| TeacherTrainingUnit | human_review_status | حالة المراجعة البشرية | Enum | نعم | حساس | لا | بمراجع |
| PortfolioArtifact | artifact_type | نوع الشاهد | Enum | نعم | تربوي | لا | نعم |
| PortfolioArtifact | privacy_level | مستوى الخصوصية | Enum | نعم | حساس | لا | بصلاحية |
| PortfolioArtifact | reviewed_by | المراجع | Identifier | لا | حساس | لا | لا بعد المراجعة |

## البيانات المشتقة

| الكيان/الحقل | مصدر الاشتقاق | قاعدة العرض |
|---|---|---|
| TodayQueue | ReviewSchedule + LessonSession + Goals | قراءة يومية، لا تحفظ كحقيقة أصلية. |
| Dashboard indicators | سجلات الحضور والتقدم والشواهد | يظهر المصدر والفترة وحدود التفسير. |
| Student progress summary | Memorization/Review/Assessment/Attendance | لا ينتج «مؤشرًا دينيًا شاملًا». |
| Report totals | سجلات أصلية ضمن فترة | يوضح نطاق البيانات والاستبعادات. |

## حقول ممنوعة افتراضيًا

لا تخزن المنظومة افتراضيًا بيانات صحية، معرفات رسمية، صورًا أو تسجيلات للأطفال، بيانات موقع، كلمات مرور صريحة، أسرارًا أو مفاتيح API، أو ملاحظات أسرية غير لازمة. أي استثناء يحتاج قرارًا مؤسسيًا مستقلًا.
