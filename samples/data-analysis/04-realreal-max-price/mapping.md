# D4：RealReal 的最高调整收盘价的任务—查询—对象映射

[同类样本](../README.md) · [完整步骤](README.md) · [完整 JSON](trace.json) · [结构化映射](mapping.json) · [六任务横向分析](../../../reports/dab-six-case-mapping-2026-10-30.md)

## 原始任务

```text
What was the maximum adjusted closing price in 2020 for The RealReal, Inc.?
```

来源 `gemini-3-pro/stockmarket/query1/run_0.json`；8 条消息、3 个 assistant 步骤、3 次工具调用，调用均有对应观察。

## Query / action → 结果对象 → 后续显式使用

每个工具调用单独一行；并行调用保留同一步骤。SQL/Mongo/Python 的完整参数及观察见对应步骤和 mapping.json。后续使用列只自动记录字面 locals 存储键引用，不作为完整依赖图。

| 来源步骤与消息索引 | Query / action（定位摘录） | 结果表示、实际入口或状态 | 后续显式使用 |
|---|---|---|---|
| [S1 / C1](README.md#step-1)：trace[2] → [3] | query_db / stockinfo_database — SELECT Symbol, &quot;Company Description&quot; FROM stockinfo WHERE &quot;Company Description&quot; LIKE &#x27;%The RealReal%&#x27; | 内联结果；`var_function-call-3588029033442653475` | 未记录字面 locals 消费；人工链见下文 |
| [S2 / C1](README.md#step-2)：trace[4] → [5] | query_db / stocktrade_database — SELECT MAX(&quot;Adj Close&quot;) FROM REAL WHERE Date LIKE &#x27;2020%&#x27; | 内联结果；`var_function-call-1270503224643372012` | 未记录字面 locals 消费；人工链见下文 |
| [S3 / C1](README.md#step-3)：trace[6] → [7] | return_answer — 18.440000534057617 | 内联结果；`var_function-call-11309881479268100484` | 未记录字面 locals 消费；人工链见下文 |

## 人工核对的信息链

S1 公司描述取得 REAL → S2 对 REAL 的 2020 年 Adj Close 求 MAX → S3 直接回答 18.440000534057617。

## 具体管理候选

- **应保留：**保留公司名到 REAL 的匹配、2020 年筛选、MAX/Adj Close 口径及原始精度。
- **可考虑外移 / 替代：**S2 后公司描述长说明可候选缩成实体匹配事实；结果本身已是小标量，无需为统一方案强行外部化。
- **条件与例外：**这是小结果对照；没有大结果、Python 或恢复调用。不能声称复杂压缩在该任务有显著收益。

这些是静态观察得到的候选动作，未构造模型续跑结果，也未将未被显式引用的内容判为可删除。完整来源消息序列不等于完整可重放环境。
