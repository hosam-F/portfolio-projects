# خريطة الكود الفعلية

## نقطة التشغيل

`src/quran_educator/presentation/app.py` ينشئ QApplication، يعرض `WelcomeSplash`، ثم `ProductionEntryDialog` للمصادقة المحلية، ثم `MainWindow`.

## خريطة الملفات

| الوظيفة | الملف |
|---|---|
| نافذة التطبيق، الهوية، Splash، Login، routes | `src/quran_educator/presentation/app.py` |
| المتحكم الرقيق بين GUI والخدمات | `src/quran_educator/presentation/controller.py` |
| التنقل وQStackedWidget routes | `src/quran_educator/presentation/navigation.py` |
| الإطار المستقل للواجهات | `src/quran_educator/presentation/views/base.py` |
| خدمات المجال | `src/quran_educator/application/domain_services.py` |
| الاستعلام والبحث | `src/quran_educator/application/query_services.py` |
| سياسة الصلاحيات | `src/quran_educator/application/authorization.py` |
| نماذج المجال | `src/quran_educator/domain/models.py` |
| ORM والكيانات | `src/quran_educator/infrastructure/db.py` |
| إنشاء قاعدة البيانات والهجرات | `src/quran_educator/infrastructure/migrations.py` |
| المصادقة المحلية | `src/quran_educator/infrastructure/auth.py` |
| النسخ والاستعادة | `src/quran_educator/infrastructure/backup.py` |
| الهوية والتسجيل ومسارات runtime | `src/quran_educator/infrastructure/productization.py` |
| التقرير الاصطناعي | `src/quran_educator/presentation/reporting.py` |
