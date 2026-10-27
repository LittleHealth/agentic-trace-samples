# Agentic Trace Samples

四类应用，12 条已有执行轨迹。每条包含完整任务、按顺序排列的调用与观察、结束状态和来源。

| 应用 | 样本数 | 执行过程 | 分类索引 |
|---|---:|---|---|
| 数据分析 / Agentic SQL | 3 | 查库、读取数据、计算、回答 | [数据分析](samples/data-analysis/README.md) |
| 软件修复 | 3 | 查看文件、复现、改代码、测试 | [软件修复](samples/software-repair/README.md) |
| 网页操作 | 3 | 观察页面、点击、输入、导航 | [网页操作](samples/browser/README.md) |
| 检索问答 | 3 | 搜索、阅读、查找证据、回答 | [检索问答](samples/research-qa/README.md) |

## 全部样本

| 应用 | 具体任务 | 来源状态 | 阅读 |
|---|---|---|---|
| 数据分析 / Agentic SQL | 亚洲股指平均日内波动率 | 已提交答案（来源未附评测标签） | [步骤](samples/data-analysis/01-asian-index/README.md) · [JSON](samples/data-analysis/01-asian-index/trace.json) |
| 数据分析 / Agentic SQL | 财务困难公司的平均成交量 | 已提交答案（来源未附评测标签） | [步骤](samples/data-analysis/02-trading-volume/README.md) · [JSON](samples/data-analysis/02-trading-volume/trace.json) |
| 数据分析 / Agentic SQL | 英文文学类满分图书 | 已提交答案（来源未附评测标签） | [步骤](samples/data-analysis/03-perfect-rated-books/README.md) · [JSON](samples/data-analysis/03-perfect-rated-books/trace.json) |
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

样本 ID、来源链接和原文校验值见各样本页。阅读版添加索引与排版，来源内容保留原归属。

[FreeInference](https://huggingface.co/datasets/harvardMadsys/freeinference_agentic_trace) 作为调用规模研究的补充入口，不计入上述 12 条正文样本。
