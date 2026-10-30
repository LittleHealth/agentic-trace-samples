# Agentic Trace Samples

四类应用的 15 条正文轨迹：数据分析 6 条，其余三类各 3 条。每条包含任务、调用与观察、结束状态和来源；另有 3 条 FreeInference 元数据会话。

| 应用 | 样本数 | 执行过程 | 分类索引 |
|---|---:|---|---|
| 数据分析 / Agentic SQL | 6 | 查库、读取数据、计算、回答 | [数据分析](samples/data-analysis/README.md) |
| 软件修复 | 3 | 查看文件、复现、改代码、测试 | [软件修复](samples/software-repair/README.md) |
| 网页操作 | 3 | 观察页面、点击、输入、导航 | [网页操作](samples/browser/README.md) |
| 检索问答 | 3 | 搜索、阅读、查找证据、回答 | [检索问答](samples/research-qa/README.md) |

## 分析入口

- [案例与 JSON 定位](reports/ppt-case-index-2026-10-30.md)：按介绍材料的页码找到具体任务、完整记录和对应步骤。
- [具体 context 管理决策点](reports/context-management-decision-points-2026-10-30.md)：四类应用的保留/移出候选、成立条件和反例。
- [DAB 六任务映射](reports/dab-six-case-mapping-2026-10-30.md)：Task → SQL/Mongo/Python → 结果对象 → 后续使用 → 管理候选。
- [跨应用证据](reports/cross-application-properties-2026-10-29.md) · [对象与状态的共同模型](reports/unified-object-trace-analysis-2026-10-30.md)。这两份较早的报告基于当时的 12 条正文样本及 3 条元数据会话。

候选管理分析来自已有轨迹，不代表已运行压缩实验或已验证正确性保证。

## FreeInference：三条会话与一周分析

[阅读首页与图表](samples/freeinference/README.md) · [完整分析报告](samples/freeinference/report/README.md) · [官方模拟结果](samples/freeinference/report/official-simulation-summary.csv)

| 会话结构 | 请求数 | 逐轮请求表 | 阅读用 JSON | 完整 JSON |
|---|---:|---|---|---|
| 持续追加（hermes） | 44 | [请求表](samples/freeinference/01-append/README.md) | [JSON](samples/freeinference/01-append/requests.json) | [完整记录](samples/freeinference/01-append/trace.json) |
| 注入改写（kilo） | 27 | [请求表](samples/freeinference/02-injection/README.md) | [JSON](samples/freeinference/02-injection/requests.json) | [完整记录](samples/freeinference/02-injection/trace.json) |
| 删除历史轮次（cline） | 46 | [请求表](samples/freeinference/03-dropped-turns/README.md) | [JSON](samples/freeinference/03-dropped-turns/requests.json) | [完整记录](samples/freeinference/03-dropped-turns/trace.json) |

一周覆盖 **106 个顶层会话、10,548 次模型请求**，完成官方 **4 种策略 × 13 个 TTL** 缓存模拟。FreeInference 没有发布消息正文；这里展示请求结构、匿名化工具调用、token 计数和前缀变化，单独列于正文轨迹之外。

## 15 条正文轨迹

| 应用 | 具体任务 | 来源状态 | 阅读 |
|---|---|---|---|
| 数据分析 / Agentic SQL | 亚洲股指平均日内波动率 | 已提交答案（来源未附评测标签） | [步骤](samples/data-analysis/01-asian-index/README.md) · [JSON](samples/data-analysis/01-asian-index/trace.json) |
| 数据分析 / Agentic SQL | 财务困难公司的平均成交量 | 已提交答案（来源未附评测标签） | [步骤](samples/data-analysis/02-trading-volume/README.md) · [JSON](samples/data-analysis/02-trading-volume/trace.json) |
| 数据分析 / Agentic SQL | 英文文学类满分图书 | 已提交答案（来源未附评测标签） | [步骤](samples/data-analysis/03-perfect-rated-books/README.md) · [JSON](samples/data-analysis/03-perfect-rated-books/trace.json) |
| 数据分析 / Agentic SQL | RealReal 的最高调整收盘价 | 已提交答案（未独立核验） | [步骤](samples/data-analysis/04-realreal-max-price/README.md) · [映射](samples/data-analysis/04-realreal-max-price/mapping.md) · [JSON](samples/data-analysis/04-realreal-max-price/trace.json) |
| 数据分析 / Agentic SQL | 工作日晚间营业的高评分商户 | 已提交答案（未独立核验） | [步骤](samples/data-analysis/05-evening-businesses/README.md) · [映射](samples/data-analysis/05-evening-businesses/mapping.md) · [JSON](samples/data-analysis/05-evening-businesses/trace.json) |
| 数据分析 / Agentic SQL | Indianapolis 商户的平均评分 | 已提交答案（未独立核验） | [步骤](samples/data-analysis/06-indianapolis-ratings/README.md) · [映射](samples/data-analysis/06-indianapolis-ratings/mapping.md) · [JSON](samples/data-analysis/06-indianapolis-ratings/trace.json) |
| 软件修复 | 修复非 POSIX 路径 | submit；resolved=1 | [步骤](samples/software-repair/01-posix-path/README.md) · [JSON](samples/software-repair/01-posix-path/trace.json) |
| 软件修复 | 修复 NetCDF 变量名中的斜杠 | submit；resolved=0 | [步骤](samples/software-repair/02-netcdf-variable-names/README.md) · [JSON](samples/software-repair/02-netcdf-variable-names/trace.json) |
| 软件修复 | 处理 AndroidTV 的 ADB 查询失败 | submit；resolved=0 | [步骤](samples/software-repair/03-androidtv-adb/README.md) · [JSON](samples/software-repair/03-androidtv-adb/trace.json) |
| 网页操作 | 发布关系问题求助帖 | success=true；done=true | [步骤](samples/browser/01-relationship-post/README.md) · [JSON](samples/browser/01-relationship-post/trace.json) |
| 网页操作 | 转发白头鹰图片 | success=false；done=false | [步骤](samples/browser/02-repost-eagle/README.md) · [JSON](samples/browser/02-repost-eagle/trace.json) |
| 网页操作 | 发布 AndroidAsync 项目介绍 | success=false；done=false | [步骤](samples/browser/03-promote-repository/README.md) · [JSON](samples/browser/03-promote-repository/trace.json) |
| 检索问答 | 排列四位古埃及法老 | status=success（运行状态） | [步骤](samples/research-qa/01-pharaoh-order/README.md) · [JSON](samples/research-qa/01-pharaoh-order/trace.json) |
| 检索问答 | 检索图像生成个性化方法 | status=success（运行状态） | [步骤](samples/research-qa/02-image-personalization/README.md) · [JSON](samples/research-qa/02-image-personalization/trace.json) |
| 检索问答 | 查找澳式足球决赛对手 | status=success（运行状态） | [步骤](samples/research-qa/03-football-finalist/README.md) · [JSON](samples/research-qa/03-football-finalist/trace.json) |

## 阅读方式

- **步骤页**：先看任务和步骤表，再展开完整调用与观察。长轨迹按页保留全部步骤。
- **可读 JSON（trace.json）**：双空格缩进；工具 arguments 中的 JSON 展开为对象，网页 trajectory 字符串展开为数组。
- **原始 JSON（trace.raw.json）**：保留来源字节、字段类型和转义。可读 JSON 是展示副本，不替代原始记录。

assistant 是模型生成的消息，tool 是工具返回。同一模型消息可包含多个工具调用，通过调用 ID 对应返回。网页样本按动作前观察展示，时序依据写在各样本页。

来源中的成功、提交、运行结束和失败标记分别照录；它们不等同于新增的独立正确性验证。已有截断和缺失会在样本页注明。

## 来源

| 应用 | 数据来源 | 数据集卡许可 / 归属 |
|---|---|---|
| 数据分析 | [DataAgentBench](https://github.com/ucbepic/DataAgentBench) | 保留 DataAgentBench 项目归属 |
| 软件修复 | [Nebius SWE-rebench OpenHands trajectories](https://huggingface.co/datasets/nebius/SWE-rebench-openhands-trajectories) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| 网页操作 | [toeunkim / MATM trajectories](https://huggingface.co/datasets/toeunkim/matm-trajectories) | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| 检索问答 | [OpenResearcher Dataset](https://huggingface.co/datasets/OpenResearcher/OpenResearcher-Dataset) | 数据集卡声明 MIT |
| 会话与缓存元数据 | [FreeInference Agentic Trace](https://huggingface.co/datasets/harvardMadsys/freeinference_agentic_trace) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

样本 ID、来源链接和原文校验值见各样本页。阅读版添加索引与排版，来源内容保留原归属。
