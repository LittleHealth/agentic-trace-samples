# DAB 六任务：Task—Query—Trace—结果对象映射

日期：2026-10-30。[样本首页](../samples/data-analysis/README.md) · [跨应用管理决策点](context-management-decision-points-2026-10-30.md) · [来源与完整性清单](dab-six-case-manifest-2026-10-30.json)

**完成范围：同一 Data Agent application 的 6 个不同任务，每个任务选择一条 gemini-3-pro/run_0 原始轨迹。** 沿任务要求→实际 SQL/Mongo/Python→结果对象→后续用途整理了管理候选，未下载新数据、重跑任务 agent、执行轨迹中的工具或重算答案。这里的 query 是实际工具查询，task 是原始用户目标，不把同任务的多个 run 当成不同任务。

## 1. 六条来源完整轨迹

| ID | 原始 Task | 来源 Trace ID | 消息 / assistant 步骤 / 调用 | 阅读与映射 |
|---|---|---|---|---|
| D1 | Which stock index in the Asia region has exhibited the highest average intraday volatility since 2020? | `gemini-3-pro/stockindex/query1/run_0.json` | 18 / 7 / 9 | [逐步阅读](../samples/data-analysis/01-asian-index/README.md) · [映射](../samples/data-analysis/01-asian-index/mapping.md) · [原始 JSON](../samples/data-analysis/01-asian-index/trace.raw.json) |
| D2 | List all company names on the NASDAQ-listed Market that were financially troubled (delinquent, deficient, or both) and have trading volume in 2008, for each, report its exisiting non-null average daily trading volume in 2008. | `gemini-3-pro/stockmarket/query3/run_0.json` | 26 / 12 / 12 | [逐步阅读](../samples/data-analysis/02-trading-volume/README.md) · [映射](../samples/data-analysis/02-trading-volume/mapping.md) · [原始 JSON](../samples/data-analysis/02-trading-volume/trace.raw.json) |
| D3 | Which English-language books in the 'Literature & Fiction' category have a perfect average rating of 5.0? Return all matching books. | `gemini-3-pro/bookreview/query2/run_0.json` | 15 / 5 / 8 | [逐步阅读](../samples/data-analysis/03-perfect-rated-books/README.md) · [映射](../samples/data-analysis/03-perfect-rated-books/mapping.md) · [原始 JSON](../samples/data-analysis/03-perfect-rated-books/trace.raw.json) |
| D4 | What was the maximum adjusted closing price in 2020 for The RealReal, Inc.? | `gemini-3-pro/stockmarket/query1/run_0.json` | 8 / 3 / 3 | [逐步阅读](../samples/data-analysis/04-realreal-max-price/README.md) · [映射](../samples/data-analysis/04-realreal-max-price/mapping.md) · [原始 JSON](../samples/data-analysis/04-realreal-max-price/trace.raw.json) |
| D5 | What are the top 5 businesses that remain open after 6:00 PM on at least one weekday, ranked by highest average rating? Include their names, operating hours, and average ratings. | `gemini-3-pro/googlelocal/query3/run_0.json` | 20 / 9 / 9 | [逐步阅读](../samples/data-analysis/05-evening-businesses/README.md) · [映射](../samples/data-analysis/05-evening-businesses/mapping.md) · [原始 JSON](../samples/data-analysis/05-evening-businesses/trace.raw.json) |
| D6 | What is the average rating of all businesses located in Indianapolis, Indiana? | `gemini-3-pro/yelp/query1/run_0.json` | 20 / 9 / 9 | [逐步阅读](../samples/data-analysis/06-indianapolis-ratings/README.md) · [映射](../samples/data-analysis/06-indianapolis-ratings/mapping.md) · [原始 JSON](../samples/data-analysis/06-indianapolis-ratings/trace.raw.json) |

合计 **107 条来源消息、45 个 assistant 步骤、50 次工具调用**。所有调用 ID 都有对应工具观察，六条均以 return_answer 提交。选择用于对比管理情形，不作随机样本或总体频率估计。[来源字节、调用配对与阅读链接校验](trace-management-validation-2026-10-30.json)均通过。

“完整”在这里指**来源中可取得的完整消息序列**，不等于全量工具数据或可重放环境：共有 5 次结果以文件入口＋10,000 字符预览记录，外部完整 JSON 文件、数据库快照和每轮 API 输入/usage 不随该轨迹归档提供。来源调用成功与答案提交不构成独立正确性标签。

每个样本的 mapping.json 保留实际查询/代码、调用 ID、消息索引、存储键、原始观察和字面 locals 引用；mapping.md 给出阅读表及人工核对的信息链。自动引用只覆盖显式存储键，复制到下一次 SQL 的值、最终文字回答和隐含推理仍需人工核对。

## 2. Task—Query—对象—用途的横向映射

| Task | 实际 Query / 处理 | 结果对象与后续使用 | 在哪里考虑管理 | 必须保留的条件 |
|---|---|---|---|---|
| D1 亚洲股指 | S5 选择六个亚洲指数的 Index/Date/Open/High/Low；S6 Python 解析日期、转换数值、计算均值 | S5 文件结果被 S6 实际打开；S6 输出按指数的均值和最大项，S7 用于回答 | 计算前旧预览可候选转为格式提示＋可恢复引用；计算后候选由汇总承接 | 日期是混合格式；S3 的单行格式已在 S4 遇到反例。S6 前仍需全量数据，不能只留样例 |
| D2 公司成交量 | S3 筛选公司；S4/S5 对齐交易表；S6–9 构造 SQL；S10 对 2008 年 Volume 求 AVG | 公司描述在 S11 才通过早期存储键读回，与 S10 均值对应，最终产生公司名/代码/均值名单 | S5 后大目录可候选外移；S11 前公司描述不能按年龄淘汰 | 公司名仍依赖描述，代码到交易表映射和非空均值口径必须保留；启发式提取未独立核验 |
| D3 满分图书 | S3 查询 book_id/title 与 purchase_id 分组平均分 5.0 的集合；S4 按后缀匹配 | S4 产生 15 本书，S5 返回全部书名 | S4 后可候选把早期样例和中间 ID 列表外移，保留最终名单及出处 | 任务要求 all matching，不可只保留前 5 本；ID 对应语义仍是原迹中的规则 |
| D4 RealReal | S1 公司描述匹配 REAL；S2 `SELECT MAX("Adj Close") FROM REAL WHERE Date LIKE '2020%'` | 一个标量 18.440000534057617，S3 直接提交 | 无需为统一方法强行外部化小结果；可保留任务口径、实体匹配和数值 | MAX、Adj Close、2020、REAL 对应关系与精度；没有大结果，收益未量化 |
| D5 晚间商户 | S5 取 gmap_id/name/hours；S6 取 gmap_id/rating；S8 读取两个文件、评分聚合、解析营业时间并排名 | S7 错误拼路径失败；S8 从两个真实存储变量获取路径后实际读取，产出 top 5 的 name/hours/avg_rating | **S7 错误后、S8 计算前**：候选外移两份较早长预览，保留实际恢复协议和格式说明；S8 后另有作答检查点 | 仍需完整结果用于计算；不能拼接假文件名；保留营业时间和评分，不能把产物缩成只有名称 |
| D6 Indianapolis | Mongo 地址筛选→businessid 转 businessref→SQL 评论级 AVG 与商户级 AVG→Python 再平均 | S4 评论级均值 3.86046511627907；S5/S6 商户均值的均值 3.977777777777778；S9 提交约 3.98 | 可候选缩小探索文档；统计口径未确认前不能合并、覆盖两个 AVG | 保留筛选集合、聚合单位和权重。两种值不同，当前不据此裁定题目真值，也不把它们视为可互换摘要 |

以上各行的完整查询、错误、存储键及消息定位均可进入对应 mapping.md 查看，未用摘要替代完整来源记录。

## 3. 从六条任务归纳的三种管理候选

### M1：完整结果留在可访问存储中，旧预览用表示说明与真实引用承接

对应 D1、D5，以及 D2 的大表目录。保留任务、schema/值格式、数据范围和真实读取协议；完整数据仍需用于后续运算。D5 S7 的 FileNotFoundError 与 S8 的正确恢复是直接正反对照：把 `var_...` 当作文件名并追加 .json 会失败，必须读取该变量中的真实路径。

这是**计算前**仍可讨论的候选，但原运行环境成功读取不证明压缩后模型会正确恢复；外部数据是否仍可达、完整观察是否已展示、恢复的净成本都需单独确认。

### M2：在明确的阶段交接后，让完整派生产物承接早期信息

对应 D3 S4→5、D5 S8→9，也可观察 D1 S6→7。保留派生产物的全部任务所需字段、计算口径和来源，不再反复携带较早探索输出。D3 需要全部 15 本；D5 需要名称、营业时间和平均分，不能只留名称或前几个对象。

这些节点紧邻最终作答，只支持该阶段的管理假设，不能当作“未完成计算时已经可删原数据”的证据。D4 是对照：SQL 本来就返回小标量，新增存储/恢复层未必有实际空间。

### M3：按后续依赖与统计语义保留中间状态，而非统一缩成短文本

D2 的公司描述在 S3 获得、S11 仍使用；D6 的两个平均数虽然都很短，却不是同一统计对象。管理策略应区分尚待使用的 metadata、已承接任务的产物、以及口径尚未确认的中间结果。

若后续需要把分组统计重新合并，可能需要 sum/count 或原结果，不能仅因已有 AVG 就假定充分；**当前未记录的计数不能补造**。该例说明管理质量不由压缩率单独决定，也说明同一 application 内需要不同管理动作。

## 4. 现在可以说什么

- 已完成 6 个不同 Task 与完整来源 Trace 的一一对应，并把 50 次工具调用映射到结果、显式引用及人工核对的后续用途。
- 已定位小结果、延迟引用、计算前恢复、计算后交接、语义不可随意合并等差异；有正例、负例和不值得强行压缩的对照。
- 未执行任何候选 context 续跑，不能给出压缩后的正确率、实际 token 节省或缓存收益；也未证明统一最优管理策略。

后续如验证方法，可优先使用 D5 的计算前节点；采用同一个任务、原始历史、环境状态和工具，对比 Full 与候选 context，再看是否正确恢复全量、完成解析计算及最终回答。该实验不在本次分析范围内。
