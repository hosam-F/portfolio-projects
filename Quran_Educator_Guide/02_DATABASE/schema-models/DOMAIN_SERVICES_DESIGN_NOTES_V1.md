# DOMAIN SERVICES DESIGN NOTES V1

## Principles

خدمات النطاق الحالية صغيرة ومفصولة عن PySide6 وReportLab والشبكة. تعتمد على Data Layer عبر session factory، وتستخدم AuthorizationContext، وتسجيل Audit مركزيًا عبر `_audit` و`_require_audited`.

## Implemented Services

| Service | Responsibility | Content Boundary |
|---|---|---|
| CircleService | الحلقة والمجموعة والتعطيل | Synthetic entities only |
| StudentDomainService | الإنشاء والتعديل والنقل والتعطيل | Minimum data، TEST identifiers |
| SessionService | الحصة والحضور والإغلاق | No closed-session mutation |
| CurriculumService | المنهج والوحدة | Source of Truth في Data Layer |
| ProjectService | المشروع المحدود | No advanced workflow |
| ProgressService | Metadata abstraction | Synthetic Source only، لا نص |
| TeacherService | Evidence descriptive | لا اعتماد شرعي/مهني |

## Deferred

محتوى القرآن runtime، التفسير، الترجمة، AI authority، Cloud، workflow المتقدم، التقارير الكاملة، وميزات V2.

## Architectural Decisions

لا توجد SQL statements في Domain، ولا business rules في UI، ولا اعتماد على Cloud. الأسماء التاريخية لا تنشئ خدمات مكررة، بل تبقى `REPLACED_BY`. `ProgressService` يتعامل مع Source ID/Version ورقم نطاق اصطناعي فقط، ولا يملك طريقة لتمرير نص قرآن.
