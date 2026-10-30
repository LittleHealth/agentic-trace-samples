# D3：英文文学类满分图书的任务—查询—对象映射

[同类样本](../README.md) · [完整步骤](README.md) · [完整 JSON](trace.json) · [结构化映射](mapping.json) · [六任务横向分析](../../../reports/dab-six-case-mapping-2026-10-30.md)

## 原始任务

```text
Which English-language books in the 'Literature & Fiction' category have a perfect average rating of 5.0? Return all matching books.
```

来源 `gemini-3-pro/bookreview/query2/run_0.json`；15 条消息、5 个 assistant 步骤、8 次工具调用，调用均有对应观察。

## Query / action → 结果对象 → 后续显式使用

每个工具调用单独一行；并行调用保留同一步骤。SQL/Mongo/Python 的完整参数及观察见对应步骤和 mapping.json。后续使用列只自动记录字面 locals 存储键引用，不作为完整依赖图。

| 来源步骤与消息索引 | Query / action（定位摘录） | 结果表示、实际入口或状态 | 后续显式使用 |
|---|---|---|---|
| [S1 / C1](README.md#step-1)：trace[2] → [3] | list_db / books_database — | 内联结果；`var_function-call-17861652249802093723` | 未记录字面 locals 消费；人工链见下文 |
| [S1 / C2](README.md#step-1)：trace[2] → [4] | list_db / review_database — | 内联结果；`var_function-call-17861652249802093564` | 未记录字面 locals 消费；人工链见下文 |
| [S2 / C1](README.md#step-2)：trace[5] → [6] | query_db / books_database — SELECT * FROM books_info LIMIT 5 | 文件入口＋来源预览；`var_function-call-4880349597561605530` | 未记录字面 locals 消费；人工链见下文 |
| [S2 / C2](README.md#step-2)：trace[5] → [7] | query_db / review_database — SELECT * FROM review LIMIT 5 | 内联结果；`var_function-call-4880349597561603561` | 未记录字面 locals 消费；人工链见下文 |
| [S3 / C1](README.md#step-3)：trace[8] → [9] | query_db / books_database — SELECT book_id, title FROM books_info WHERE categories LIKE &#x27;%Literature &amp; Fiction%&#x27; AND details LIKE &#x27;%English%&#x27; | 内联结果；`var_function-call-6010646955784418156` | S4 通过 locals 读取 |
| [S3 / C2](README.md#step-3)：trace[8] → [10] | query_db / review_database — SELECT purchase_id FROM review GROUP BY purchase_id HAVING AVG(rating) = 5.0 | 内联结果；`var_function-call-6010646955784418113` | S4 通过 locals 读取 |
| [S4 / C1](README.md#step-4)：trace[11] → [12] | execute_python — import json # Load data books_data = locals()[&#x27;var_function-call-6010646955784418156&#x27;] reviews_data = locals()[&#x27;var_function-call-6010646955784418113&#x27;] # Helper to… | 内联结果；`var_function-call-1656047818242560665` | 未记录字面 locals 消费；人工链见下文 |
| [S5 / C1](README.md#step-5)：trace[13] → [14] | return_answer — The English-language books in the &#x27;Literature &amp; Fiction&#x27; category with a perfect average rating of 5.0 are: 1. Reunion: The Children of Lauderdale Park 2. The Proph… | 内联结果；`var_function-call-12975969061347643608` | 未记录字面 locals 消费；人工链见下文 |

## 人工核对的信息链

S3 的两组结果分别给出 book_id/title 与 purchase_id；S4 按 ID 后缀匹配为 15 本书；S5 使用该名单。

## 具体管理候选

- **应保留：**S4 前保留两个结果及 ID 对应规则；S4 后仍保留返回全部匹配项的要求、完整书名与来源。
- **可考虑外移 / 替代：**S4 后可候选用完整 15 本名单承接较早样例和中间 ID 列表；这是作答前候选，不是计算前压缩验证。
- **条件与例外：**来源为 bookreview/query2；不把其他同主题任务混入。ID 后缀匹配只按原迹照录，不独立证明连接语义。

这些是静态观察得到的候选动作，未构造模型续跑结果，也未将未被显式引用的内容判为可删除。完整来源消息序列不等于完整可重放环境。
