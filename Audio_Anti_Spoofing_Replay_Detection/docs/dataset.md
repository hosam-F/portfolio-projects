# Dataset

يعتمد التنفيذ العملي على **ASVspoof 2017 Version 2 – Development Set** الموجود محليًا داخل `data/raw/`. الملفات المحلية الحالية هي ملفات WAV بأسماء `D_...`، بينما لا يوجد معها Protocol أو ملف Labels يربط كل اسم بتصنيف `GENUINE` أو `REPLAY`.

وفق [الصفحة الرسمية لـ ASVspoof 2017](http://www.asvspoof.org/index2017.html)، يجب أن تتضمن مجموعة التطوير أمثلة معنونة Genuine/Replay وMetadata إضافية. كما يوضح [سجل University of Edinburgh DataShare](https://datashare.ed.ac.uk/items/59543650-e9b0-415d-8058-0567f908ce37) أن الإصدار Version 2 يتضمن README وChangeLog وMetadata.

لذلك لم تُنشأ Labels تخمينية، ولم يبدأ التدريب أو التقييم. عند توفير Protocol الرسمي يوضع في `data/metadata/` ويُمرر إلى التدريب عبر `--protocol`. لا يتم تنزيل ASVspoof 2019 PA؛ يُذكر فقط كمرجع علمي مستقبلي.
