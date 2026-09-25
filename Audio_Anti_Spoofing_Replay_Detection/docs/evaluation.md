# Evaluation

استُخدمت 1710 عينة من ASVspoof 2017 V2 Development Set مع Labels من الـProtocol الرسمي: 760 Genuine و950 Replay. قُسمت البيانات stratified إلى 1368 للتدريب و342 للاختبار، مع `random_state=42`.

| Metric | Value |
|---|---:|
| Accuracy | 0.979532 |
| Precision (Replay) | 0.969231 |
| Recall (Replay) | 0.994737 |
| F1-score (Replay) | 0.981818 |

مصفوفة الالتباس بالترتيب `[GENUINE, REPLAY]` هي:

```text
[[146, 6],
 [  1, 189]]
```

حُفظت المقاييس في `results/metrics/metrics.json` والتنبؤات الفردية في `results/predictions/predictions.csv`. هذه النتائج تجريبية محلية على Development Set وليست قياسًا مستقلًا على Dataset خارجية.
