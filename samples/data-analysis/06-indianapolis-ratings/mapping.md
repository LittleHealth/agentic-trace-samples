# D6：Indianapolis 商户的平均评分的任务—查询—对象映射

[同类样本](../README.md) · [完整步骤](README.md) · [完整 JSON](trace.json) · [结构化映射](mapping.json) · [六任务横向分析](../../../reports/dab-six-case-mapping-2026-10-30.md)

## 原始任务

```text
What is the average rating of all businesses located in Indianapolis, Indiana?
```

来源 `gemini-3-pro/yelp/query1/run_0.json`；20 条消息、9 个 assistant 步骤、9 次工具调用，调用均有对应观察。

## Query / action → 结果对象 → 后续显式使用

每个工具调用单独一行；并行调用保留同一步骤。SQL/Mongo/Python 的完整参数及观察见对应步骤和 mapping.json。后续使用列只自动记录字面 locals 存储键引用，不作为完整依赖图。

| 来源步骤与消息索引 | Query / action（定位摘录） | 结果表示、实际入口或状态 | 后续显式使用 |
|---|---|---|---|
| [S1 / C1](README.md#step-1)：trace[2] → [3] | query_db / businessinfo_database — {&quot;collection&quot;: &quot;business&quot;, &quot;limit&quot;: 5} | 内联结果；`var_function-call-15381864210095512097` | 未记录字面 locals 消费；人工链见下文 |
| [S2 / C1](README.md#step-2)：trace[4] → [5] | query_db / businessinfo_database — {&quot;collection&quot;: &quot;business&quot;, &quot;filter&quot;: {&quot;description&quot;: {&quot;$regex&quot;: &quot;Indianapolis, IN&quot;, &quot;$options&quot;: &quot;i&quot;}}, &quot;projection&quot;: {&quot;business_id&quot;: 1}} | 内联结果；`var_function-call-8903086050556643021` | S3 通过 locals 读取 |
| [S3 / C1](README.md#step-3)：trace[6] → [7] | execute_python — import json # Load the business list business_list = locals()[&#x27;var_function-call-8903086050556643021&#x27;] # Extract business_ids business_ids = [b[&#x27;business_id&#x27;] for … | 内联结果；`var_function-call-14233399033607219845` | 未记录字面 locals 消费；人工链见下文 |
| [S4 / C1](README.md#step-4)：trace[8] → [9] | query_db / user_database — SELECT AVG(rating) as average_rating FROM review WHERE business_ref IN (&#x27;businessref_52&#x27;, &#x27;businessref_84&#x27;, &#x27;businessref_76&#x27;, &#x27;businessref_87&#x27;, &#x27;business… | 内联结果；`var_function-call-14854838588788576077` | 未记录字面 locals 消费；人工链见下文 |
| [S5 / C1](README.md#step-5)：trace[10] → [11] | query_db / user_database — SELECT business_ref, AVG(rating) as business_rating FROM review WHERE business_ref IN (&#x27;businessref_52&#x27;, &#x27;businessref_84&#x27;, &#x27;businessref_76&#x27;, &#x27;businessref… | 内联结果；`var_function-call-2025848882773634410` | S6 通过 locals 读取 |
| [S6 / C1](README.md#step-6)：trace[12] → [13] | execute_python — import json results = locals()[&#x27;var_function-call-2025848882773634410&#x27;] ratings = [float(r[&#x27;business_rating&#x27;]) for r in results] avg_rating = sum(ratings) / len(ra… | 内联结果；`var_function-call-18008588926842251060` | 未记录字面 locals 消费；人工链见下文 |
| [S7 / C1](README.md#step-7)：trace[14] → [15] | query_db / businessinfo_database — {&quot;collection&quot;: &quot;business&quot;, &quot;filter&quot;: {&quot;description&quot;: {&quot;$regex&quot;: &quot;Indianapolis, Indiana&quot;, &quot;$options&quot;: &quot;i&quot;}}, &quot;projection&quot;: {&quot;business_id&quot;: 1}} | 内联结果；`var_function-call-7600000513130432997` | 未记录字面 locals 消费；人工链见下文 |
| [S8 / C1](README.md#step-8)：trace[16] → [17] | query_db / businessinfo_database — {&quot;collection&quot;: &quot;business&quot;, &quot;filter&quot;: {&quot;description&quot;: {&quot;$regex&quot;: &quot;Indianapolis&quot;, &quot;$options&quot;: &quot;i&quot;}}, &quot;projection&quot;: {&quot;description&quot;: 1}} | 内联结果；`var_function-call-14400939568330807676` | 未记录字面 locals 消费；人工链见下文 |
| [S9 / C1](README.md#step-9)：trace[18] → [19] | return_answer — The average rating of all businesses located in Indianapolis, Indiana is approximately 3.98. | 内联结果；`var_function-call-11140961998404023104` | 未记录字面 locals 消费；人工链见下文 |

## 人工核对的信息链

S2 Mongo 筛出 business_id → S3 转为 business_ref → S4 评论级 AVG=3.86046511627907；S5 商户级 AVG → S6 再平均=3.977777777777778；S7/S8 复核地域，S9 回答约 3.98。

## 具体管理候选

- **应保留：**保留筛选地域、ID 转换、聚合分组/权重/统计对象；不同口径的两个结果不能合并成无标签的“平均分”。
- **可考虑外移 / 替代：**可候选缩减 Mongo 探索样例等宽字段；在统计口径确定前不能只留一个 AVG。若未来要重算评论级均值，仅保留各商户均值可能不足，还需计数或原结果。
- **条件与例外：**两个值来自原日志中的不同统计口径，不据此独立裁定哪一个满足任务。S7 的空结果也不证明城市中没有商户。

这些是静态观察得到的候选动作，未构造模型续跑结果，也未将未被显式引用的内容判为可删除。完整来源消息序列不等于完整可重放环境。
