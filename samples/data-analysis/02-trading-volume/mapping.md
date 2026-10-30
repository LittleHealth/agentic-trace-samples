# D2：财务困难公司的平均成交量的任务—查询—对象映射

[同类样本](../README.md) · [完整步骤](README.md) · [完整 JSON](trace.json) · [结构化映射](mapping.json) · [六任务横向分析](../../../reports/dab-six-case-mapping-2026-10-30.md)

## 原始任务

```text
List all company names on the NASDAQ-listed Market that were financially troubled (delinquent, deficient, or both) and have trading volume in 2008, for each, report its exisiting non-null average daily trading volume in 2008.
```

来源 `gemini-3-pro/stockmarket/query3/run_0.json`；26 条消息、12 个 assistant 步骤、12 次工具调用，调用均有对应观察。

## Query / action → 结果对象 → 后续显式使用

每个工具调用单独一行；并行调用保留同一步骤。SQL/Mongo/Python 的完整参数及观察见对应步骤和 mapping.json。后续使用列只自动记录字面 locals 存储键引用，不作为完整依赖图。

| 来源步骤与消息索引 | Query / action（定位摘录） | 结果表示、实际入口或状态 | 后续显式使用 |
|---|---|---|---|
| [S1 / C1](README.md#step-1)：trace[2] → [3] | query_db / stockinfo_database — SELECT DISTINCT &quot;Financial Status&quot; FROM stockinfo | 内联结果；`var_function-call-5364542946618092679` | 未记录字面 locals 消费；人工链见下文 |
| [S2 / C1](README.md#step-2)：trace[4] → [5] | query_db / stockinfo_database — SELECT DISTINCT &quot;Listing Exchange&quot; FROM stockinfo | 内联结果；`var_function-call-7902520603048016019` | 未记录字面 locals 消费；人工链见下文 |
| [S3 / C1](README.md#step-3)：trace[6] → [7] | query_db / stockinfo_database — SELECT Symbol, &quot;Company Description&quot; FROM stockinfo WHERE &quot;Listing Exchange&quot; = &#x27;Q&#x27; AND &quot;Financial Status&quot; IN (&#x27;D&#x27;, &#x27;E&#x27;, &#x27;H&#x27;) | 内联结果；`var_function-call-5122763496814090020` | S11 通过 locals 读取 |
| [S4 / C1](README.md#step-4)：trace[8] → [9] | list_db / stocktrade_database — | 文件入口＋来源预览；`var_function-call-1970093475337278536` | S5 通过 locals 读取 |
| [S5 / C1](README.md#step-5)：trace[10] → [11] | execute_python — import json # Load the candidate symbols candidates_list = [ {&quot;Symbol&quot;: &quot;AGMH&quot;}, {&quot;Symbol&quot;: &quot;AMTX&quot;}, {&quot;Symbol&quot;: &quot;APEX&quot;}, {&quot;Symbol&quot;: &quot;BIOC&quot;}, {&quot;Symbol&quot;: &quot;BKYI&quot;}, {&quot;… | 内联结果；`var_function-call-12195374985922159337` | 未记录字面 locals 消费；人工链见下文 |
| [S6 / C1](README.md#step-6)：trace[12] → [13] | execute_python — import json valid_symbols = [&quot;RBZ&quot;, &quot;SNSS&quot;, &quot;CBAT&quot;, &quot;ISDS&quot;, &quot;BKYI&quot;, &quot;APEX&quot;, &quot;PEIX&quot;, &quot;NXTD&quot;, &quot;CORV&quot;, &quot;MCEP&quot;, &quot;AMTX&quot;, &quot;CPAH&quot;, &quot;IDEX&quot;, &quot;FTFT&quot;, &quot;FTR&quot;, &quot;FAMI&quot;, &quot;OPTT&quot;, … | 执行失败；无存储键；见错误观察 | 未记录字面 locals 消费；人工链见下文 |
| [S7 / C1](README.md#step-7)：trace[14] → [15] | execute_python — import json valid_symbols = [&quot;RBZ&quot;, &quot;SNSS&quot;, &quot;CBAT&quot;, &quot;ISDS&quot;, &quot;BKYI&quot;, &quot;APEX&quot;, &quot;PEIX&quot;, &quot;NXTD&quot;, &quot;CORV&quot;, &quot;MCEP&quot;, &quot;AMTX&quot;, &quot;CPAH&quot;, &quot;IDEX&quot;, &quot;FTFT&quot;, &quot;FTR&quot;, &quot;FAMI&quot;, &quot;OPTT&quot;, … | 内联结果；`var_function-call-12545864015431349019` | 未记录字面 locals 消费；人工链见下文 |
| [S8 / C1](README.md#step-8)：trace[16] → [17] | execute_python — import json valid_symbols = [&quot;RBZ&quot;, &quot;SNSS&quot;, &quot;CBAT&quot;, &quot;ISDS&quot;, &quot;BKYI&quot;, &quot;APEX&quot;, &quot;PEIX&quot;, &quot;NXTD&quot;, &quot;CORV&quot;, &quot;MCEP&quot;, &quot;AMTX&quot;, &quot;CPAH&quot;, &quot;IDEX&quot;, &quot;FTFT&quot;, &quot;FTR&quot;, &quot;FAMI&quot;, &quot;OPTT&quot;, … | 执行失败；无存储键；见错误观察 | 未记录字面 locals 消费；人工链见下文 |
| [S9 / C1](README.md#step-9)：trace[18] → [19] | execute_python — import json valid_symbols = [&quot;RBZ&quot;, &quot;SNSS&quot;, &quot;CBAT&quot;, &quot;ISDS&quot;, &quot;BKYI&quot;, &quot;APEX&quot;, &quot;PEIX&quot;, &quot;NXTD&quot;, &quot;CORV&quot;, &quot;MCEP&quot;, &quot;AMTX&quot;, &quot;CPAH&quot;, &quot;IDEX&quot;, &quot;FTFT&quot;, &quot;FTR&quot;, &quot;FAMI&quot;, &quot;OPTT&quot;, … | 内联结果；`var_function-call-9807346607472633190` | 未记录字面 locals 消费；人工链见下文 |
| [S10 / C1](README.md#step-10)：trace[20] → [21] | query_db / stocktrade_database — SELECT * FROM (SELECT &#x27;RBZ&#x27; as Symbol, AVG(Volume) as AvgVolume FROM RBZ WHERE Date LIKE &#x27;2008-%&#x27; UNION ALL SELECT &#x27;SNSS&#x27; as Symbol, AVG(Volume) as… | 内联结果；`var_function-call-16995301848373287930` | S11 通过 locals 读取 |
| [S11 / C1](README.md#step-11)：trace[22] → [23] | execute_python — import json # Load previous results stock_info = locals()[&#x27;var_function-call-5122763496814090020&#x27;] volumes = locals()[&#x27;var_function-call-16995301848373287930&#x27;] # C… | 内联结果；`var_function-call-11286810619606244106` | 未记录字面 locals 消费；人工链见下文 |
| [S12 / C1](README.md#step-12)：trace[24] → [25] | return_answer — The NASDAQ-listed companies that were financially troubled (delinquent, deficient, or both) and had non-null average daily trading volume in 2008 are: - **Apex Glob… | 内联结果；`var_function-call-2923383326373795228` | 未记录字面 locals 消费；人工链见下文 |

## 人工核对的信息链

S3 公司描述在 S11 再次读回；S4 大目录 → S5 代码交集 → S6–9 SQL 构造 → S10 均值 → S11 公司名/均值名单 → S12 回答。

## 具体管理候选

- **应保留：**S11 前保留公司描述到公司名的依赖、股票代码与均值对应、目录句柄及语法错误反馈。
- **可考虑外移 / 替代：**S5 后目录正文可候选外移，保留有效代码集合及来源；不能因为 S3 较旧就移除仍供 S11 使用的描述/恢复能力。
- **条件与例外：**公司名通过描述中的词组启发式提取，未独立验证。未出现显式 storage 引用不表示没有语义依赖。

这些是静态观察得到的候选动作，未构造模型续跑结果，也未将未被显式引用的内容判为可删除。完整来源消息序列不等于完整可重放环境。
