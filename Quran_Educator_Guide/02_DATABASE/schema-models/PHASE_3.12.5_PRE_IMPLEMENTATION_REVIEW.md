# PHASE 3.12.5 PRE-IMPLEMENTATION REVIEW

## Current Gates

`LEGACY_GLOBAL_GATE=NO-GO`، و`DEVELOPMENT_GATE=GO — CONTROLLED / SYNTHETIC DATA ONLY`، و`CONTENT_GATE=NO-GO`، و`RELEASE_GATE=NO-GO`.

## Existing Foundation

توجد PySide6 Foundation، Data Layer محلية، Domain/Application Services، ReportLab Foundation، وحواجز المحتوى والنسخ والاستعادة. الهدف هو ربط واجهة تشغيل محلية بهذه الطبقات دون إعادة بناء المعمارية.

## UI Scope

سيتم بناء نافذة تشغيل محلية تتضمن اختيار حساب اصطناعي، لوحة حالة، قائمة المؤسسة والحلقة والمجموعة والطلاب، المنهج والوحدة، الحصة والحضور، التقدم والملاحظة، سجل Audit، والتقرير والنسخ والاستعادة.

## Authorization Boundary

الواجهة ستخفي أو تعطل الأوامر غير المسموحة، لكن كل عملية ستظل تمر عبر Authorization في الخدمة. لا Role جديدة؛ Mentor مصطلح وظيفي ضمن TEACHER. لا يعرض TRAINEE_TEACHER وظائف الإدارة الحساسة دون تفويض.

## Vertical Slice UI Plan

سيُختبر المسار من الواجهة إلى Data Layer: اختيار حساب اصطناعي، عرض البيانات الاصطناعية، تشغيل الحصة، الحضور، metadata progress، observation، الإغلاق، التقرير المحلي، backup، restore، verification.

## Offline Plan

لا Cloud ولا Remote API ولا Telemetry. اختبار التطبيق باستخدام `QT_QPA_PLATFORM=offscreen` وبيانات محلية، مع محاولة تشغيل العمليات دون اتصال خارجي.

## Reporting Plan

تقارير محلية باستخدام ReportLab فقط، دون محتوى خارجي، وتقتصر على بيانات اصطناعية. لا ترسل التقارير إلى Cloud.

## Risks

الخطر هو وضع قواعد العمل داخل UI أو الإيحاء بأن الواجهة تفتح Content Gate. لذلك تكون الواجهة Adapter رقيقة، وتبقى الخدمات مصدر القرار، وتظهر حالات الحظر بوضوح.

## Deferred

الواجهة الإنتاجية الكاملة، المصادقة الحقيقية، البيانات الحقيقية، القرآن، Cloud، Release، تطبيق الجوال، AI التوليدي، وميزات V2.
