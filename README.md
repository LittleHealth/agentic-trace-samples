# Agentic Trace Samples

四类应用，各一条已有 agent 执行轨迹。点击阅读版，可以顺着任务、调用、工具观察和结束状态读完整个过程；同目录的 `trace.json` 保留来源原文。

本版用于向导师展示“不同 application 下的 traces 长什么样”。样本均来自已有材料，本次没有运行新 agent、重放工具命令或进行压缩实验。

## 从这里开始

| Application | 具体任务 | 能直接看到的执行过程 | 阅读版与原文 | 来源记录的结束情况 |
|---|---|---|---|---|
| 数据分析 / Agentic SQL | 找出 2020 年以来平均日内波动率最高的亚洲股指 | 查库 → 日期解析报错 → 取大结果 → Python 读取与计算 → 回答 | [逐步阅读](samples/data-analysis/README.md) · [原始 JSON](samples/data-analysis/trace.json) | 已提交答案；没有附加成功标签 |
| 软件修复 | 修复 `GetEdk2RelativePathFromAbsolutePath()` 返回非 POSIX 路径的问题 | 查看文件 → 创建复现 → 修改代码 → 运行测试 → 提交补丁 | [逐步阅读](samples/software-repair/README.md) · [原始 JSON](samples/software-repair/trace.json) | `submit`，来源 `resolved=1` |
| 网页操作 | 在关系讨论社区发布有关出轨的求助帖 | 页面观察 → 搜索 → 点击与输入 → 提交帖子、评论 → 停止 | [逐步阅读](samples/browser/README.md) · [原始 JSON](samples/browser/trace.json) | `stop`，来源 `success=true` |
| 检索问答 | 根据线索识别四位古埃及法老，并按在位时间排序 | 搜索 → 打开资料 → 页内查找 → 继续核对 → 带引用回答 | [逐步阅读](samples/research-qa/README.md) · [原始 JSON](samples/research-qa/trace.json) | 存在 final 回答，来源运行状态 `success` |

## 怎么阅读

1. 先读样本的完整任务，再看步骤表。
2. 点击步骤编号，展开该步的完整调用、参数与观察正文。表格中的短句是定位摘录，折叠块不再裁短这些正文。
3. 最后看“如何结束”和“来源与原文”，对照样本 ID、来源链接与 JSON。

软件 / SQL / 问答的工具返回按原消息顺序展示；并行调用通过原始调用 ID 对应返回。网页样本中的观察按动作前页面展示，详细页面时序说明见该样本。

## 原文保存方式

- DAB：逐字节复制本地公开轨迹归档中的一条原始 JSON。
- 其余三条：从本地已缓存的 Hugging Face Viewer JSON 响应中提取选中 row 对象的原始文本切片。字段、消息、转义与来源类型保留；没有重新生成会话或补写缺失步骤。
- 不统一原始 schema。例如 MATM 的 `trajectory` 在原记录中是 JSON 字符串，本仓库仍保存为字符串，只在阅读版解码展示。
- 来源运行状态照录。`submit`、`success`、`resolved` 的含义不完全相同；本版没有新增正确性验证。已知截断和缺失分别写在各样本页。
- 各样本页附原文 SHA-256、来源定位与署名；Viewer 的行号与接口可能随数据集更新变化，优先使用样本 ID 和保留的原文核对。缓存元数据中的 revision 是取样时观测值，不能单独证明 Viewer 响应已绑定到该 revision。

## 来源与署名

| 本仓库样本 | 原来源 / 发布者 | 数据集卡许可或归属信息 |
|---|---|---|
| data-analysis | [DataAgentBench，UC Berkeley EPIC / DAB 项目](https://github.com/ucbepic/DataAgentBench) | 保留上游归属；本仓库不为归档另行指定许可 |
| software-repair | [Nebius SWE-rebench OpenHands trajectories](https://huggingface.co/datasets/nebius/SWE-rebench-openhands-trajectories) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| browser | [toeunkim / MATM trajectories](https://huggingface.co/datasets/toeunkim/matm-trajectories) | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| research-qa | [OpenResearcher Dataset](https://huggingface.co/datasets/OpenResearcher/OpenResearcher-Dataset) | 数据集卡声明 MIT |

阅读版是为定位原始记录添加的说明和排版，代码片段、工具结果与网页材料继续保留原来源归属。仓库没有给不同来源的内容套用统一许可。

[FreeInference](https://huggingface.co/datasets/harvardMadsys/freeinference_agentic_trace) 保留为后续研究调用规模的入口；由于缺少消息正文，本版没有将其作为四类应用的展示样本。

整理日期：2026-10-27（Asia/Taipei）。共 4 条样本，目录内只有本首页、4 份阅读版和 4 份原始 JSON，无需安装或运行程序。
