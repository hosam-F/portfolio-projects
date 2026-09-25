# دليل معمارية النظام

**المصدر:** مستخرج من `00_MASTER/src/quran_educator` وملفات الاختبارات والتغليف.  
**آخر تحديث:** 2026-08-29T00:06:44.640983+00:00

## المعمارية الفعلية

المشروع تطبيق Windows محلي Offline-first بنمط Modular Monolith. نقطة الدخول الفعلية هي `src/quran_educator/presentation/app.py`. تتصل الواجهة بـ`presentation/controller.py`، ويستدعي المتحكم خدمات التطبيق، بينما تنفذ طبقة Infrastructure قاعدة البيانات والمصادقة والنسخ الاحتياطي والتسجيل.

| الطبقة | المسار الفعلي | الدور المثبت |
|---|---|---|
| Presentation | `src/quran_educator/presentation` | PySide6، Splash، Login، MainWindow، QStackedWidget، Navigation، Views، Reporting |
| Application | `src/quran_educator/application` | domain services، query services، authorization، حالات الاستخدام |
| Domain | `src/quran_educator/domain` | نماذج وقيم المجال والقواعد الأساسية |
| Infrastructure | `src/quran_educator/infrastructure` | SQLite/SQLAlchemy، migrations، auth، backup، productization، logging |
| Tests | `tests` | اختبارات الوحدات والتكامل والتحقق الاصطناعي |

## مسار البيانات الفعلي

يبدأ الحدث من زر أو نموذج في `app.py`. تستدعي الواجهة دالة في `ControlledAppController`. يتحقق المتحكم من المدخلات ويستدعي مثلًا `StudentDomainService` أو `SessionService` أو `CurriculumService`. تتولى الخدمة استخدام `factory` الناتج من `initialize_database`، ثم تُحفظ الكيانات في SQLite عبر SQLAlchemy. عمليات القراءة تمر عبر المتحكم أو `SearchService` وتعود إلى عناصر QListWidget أو البطاقات في الواجهة.

## حدود التصميم

لا تعدل Schema أو Domain Model أو Relations أو semantics المصادقة والصلاحيات داخل تحسينات Presentation. أي تغيير في هذه الطبقات يحتاج Change Control واختبارًا قبل/بعد.
