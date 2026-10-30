# 现有轨迹的跨应用信息使用性质

日期：2026-10-29。检查范围：`samples/` 中全部 **15 条独立轨迹**，即四类应用各 3 条正文轨迹，另加 3 条 FreeInference 元数据会话。只阅读已有调用、观察和状态；没有下载数据、执行轨迹工具、运行模型或新增实验。样本版本：`feabcee5fc2dc6f5c7f994c545f0ad9443dff326`。

**得到三条有边界的性质：信息可跨多步继续使用并转化为更局部的需求；重复访问的价值取决于状态变化与访问目的；有地址不等于能恢复同一观察。** 它们支持按“后续用途、对象状态、恢复条件”管理历史，尚不证明任何具体压缩安全。

## 1. 样本覆盖

下表保留原始问题或 issue 标题；软件问题的复现代码、数据库说明等完整约束仍在对应 JSON 中。`trace.raw.json` 与 `trace.json` 是同一来源的两种表示，不重复计数；分页阅读材料及已有周级分析表也不当作新轨迹。按四个 application 分别比较，不按步骤数投票；FreeInference 的 harness 不当作第五种应用。

| 编号 / Application | 原始任务描述或 issue 标题 | Trace 文件 |
|---|---|---|
| D1 · 数据分析 / Agentic SQL | Which stock index in the Asia region has exhibited the highest average intraday volatility since 2020? | [data-analysis/01-asian-index/trace.json](../samples/data-analysis/01-asian-index/trace.json) |
| D2 · 数据分析 / Agentic SQL | List all company names on the NASDAQ-listed Market that were financially troubled (delinquent, deficient, or both) and have trading volume in 2008, for each, report its exisiting non-null average daily trading volume in 2008. | [data-analysis/02-trading-volume/trace.json](../samples/data-analysis/02-trading-volume/trace.json) |
| D3 · 数据分析 / Agentic SQL | Which English-language books in the 'Literature & Fiction' category have a perfect average rating of 5.0? Return all matching books. | [data-analysis/03-perfect-rated-books/trace.json](../samples/data-analysis/03-perfect-rated-books/trace.json) |
| S1 · 软件修复 | [Bug]: GetEdk2RelativePathFromAbsolutePath() Can Silently Return Non-POSIX Path | [software-repair/01-posix-path/trace.json](../samples/software-repair/01-posix-path/trace.json) |
| S2 · 软件修复 | Forward slashes in variable names when writing to netcdf | [software-repair/02-netcdf-variable-names/trace.json](../samples/software-repair/02-netcdf-variable-names/trace.json) |
| S3 · 软件修复 | Android Debug Bridge (AndroidTV) app_id frequently shows "Failed to write while dumping service window: Broken pipe | [software-repair/03-androidtv-adb/trace.json](../samples/software-repair/03-androidtv-adb/trace.json) |
| W1 · 网页操作 | Ask for advice about cheat in a subreddit for relations | [browser/01-relationship-post/trace.json](../samples/browser/01-relationship-post/trace.json) |
| W2 · 网页操作 | Re-post the image of Bald Eagle in this page to earthporn subreddit and note "from /f/pics" | [browser/02-repost-eagle/trace.json](../samples/browser/02-repost-eagle/trace.json) |
| W3 · 网页操作 | Promote koush/AndroidAsync to subreddit funny with the description from the repo itself. | [browser/03-promote-repository/trace.json](../samples/browser/03-promote-repository/trace.json) |
| Q1 · 检索问答 | Four pharaohs of a golden age of ancient Egypt’s pyramid-building dynasty are described as follows: First, a ruler celebrated for his beauty and architectural innovation; second, his famous direct successor known by a different name to the Greeks and credited with the era’s greatest monument; third, a king linked to producing the most statues of all of his line and ruling for about 25 years; fourth, the monarch whose own tomb at the same necropolis is significantly smaller, its name proclaiming the king’s divinity. Arrange these rulers in chronological order from earliest to latest by their reign. List their names in English, separated by commas, without titles. | [research-qa/01-pharaoh-order/trace.json](../samples/research-qa/01-pharaoh-order/trace.json) |
| Q2 · 检索问答 | Identify the method for personalizing image synthesis models to user-provided visual concepts, especially those based on generative AI paradigms such as diffusion models or large language/multimodal models. | [research-qa/02-image-personalization/trace.json](../samples/research-qa/02-image-personalization/trace.json) |
| Q3 · 检索问答 | What is the grand finalist where the winner is Collingwood among preseason and night series Australian Football League 1977 1987?<br>Note: A Excel file '/home/zhiqi_li/mirage/data/wikitables/tables/table_1_1139835_3.xlsx' is associated with this task. You may use available tools to read its content if necessary. | [research-qa/03-football-finalist/trace.json](../samples/research-qa/03-football-finalist/trace.json) |
| F1 · 补充元数据 | 原始任务未发布；hermes 会话 `38fd82c2b2f4693bcb97a6be528dccae` | [freeinference/01-append/trace.json](../samples/freeinference/01-append/trace.json) |
| F2 · 补充元数据 | 原始任务未发布；kilo 会话 `d3cf2b494fbb04a8d1850c2367f5fcdd` | [freeinference/02-injection/trace.json](../samples/freeinference/02-injection/trace.json) |
| F3 · 补充元数据 | 原始任务未发布；cline 会话 `26b3e835fc1dc0d41af636b34005c880` | [freeinference/03-dropped-turns/trace.json](../samples/freeinference/03-dropped-turns/trace.json) |

**步骤口径：**D/S 使用各样本阅读版的 assistant 步骤；Q 使用浏览工具调用步骤，最后一步为 final；W 的观察发生在动作之前，动作效果看下一步观察；F 使用从 1 开始的模型请求编号。下表的箭头表示同一条证据链，不代表连续两个原始消息。

## 2. 每条轨迹的代表性证据

每条只保留 1–2 条证据链。编号对应上表，步骤链接直接定位已有阅读版。

| Trace | 步骤 → 具体内容 → 后续使用 / 状态变化 |
|---|---|
| D1 | [S3→4](../samples/data-analysis/01-asian-index/README.md#step-3)：单行日期样例为 `31 Dec 1986, 00:00`，按该格式解析全表时遇到 `January 02, 1987 at 12:00 AM` 而失败；小样例不覆盖全部格式。[S5→7](../samples/data-analysis/01-asian-index/README.md#step-5)：大结果存储为 `var_function-call-4501430723657214772` 指向的文件，Python 实际打开文件、解析及汇总，随后回答使用最高波动率指数和数值。 |
| D2 | [S4→5](../samples/data-analysis/02-trading-volume/README.md#step-4)：大表目录通过存储键读取，再与候选股票代码求交集。[S3→11](../samples/data-analysis/02-trading-volume/README.md#step-11)：较早的公司描述结果仍以 `stock_info` 读回，与 S10 的均值结果结合，提取公司名；经过多步不等于用途已结束。 |
| D3 | [S3→5](../samples/data-analysis/03-perfect-rated-books/README.md#step-3)：两个查询分别取得候选书名及满分购买 ID；Python 读两个存储键、按 ID 后缀匹配，输出 15 本书；最终作答使用这份名单。这里只确认执行中的信息流，不独立验证 ID 匹配规则。 |
| S1 | [S20→24](../samples/software-repair/01-posix-path/README.md#step-20)：`python reproduce_issue.py` 先返回非 POSIX 路径、退出 1；S23 修改 `path_utilities.py` 的分隔符处理；同命令 S24 返回 POSIX 路径、退出 0。相同调用因代码改变而提供新的验证证据。 |
| S2 | [S64→69](../samples/software-repair/02-netcdf-variable-names/README.md#step-64)：`git stash` 后再 `stash pop`，恢复两处 tracked 源文件改动，表明恢复需要工作树状态而非单一路径。[S79→90](../samples/software-repair/02-netcdf-variable-names/README.md#step-79)：已无斜杠名称，但保存仍出现属性类型 TypeError；后续自写验证脚本容忍该异常并打印已解决，来源仍标 `resolved=0`。局部检查与任务完成不同。 |
| S3 | [S30→34](../samples/software-repair/03-androidtv-adb/README.md#step-30)：同一复现脚本先把 Broken pipe 文本当作 app_id；S33 修改过滤规则后，S34 结果变为 `None`，退出码由 1 变 0。[S67](../samples/software-repair/03-androidtv-adb/README.md#step-67)：四个验证脚本被删除，退出 0；历史中的文件路径不再足以重取脚本，需另有内容或版本记录。 |
| W1 | [S3→4](../samples/browser/01-relationship-post/README.md#step-3)：同一 `/submit` URL 的标题从空变成已填文本，随后填写 forum。[S5→6](../samples/browser/01-relationship-post/README.md#step-5)：点击 Create submission 后，下一观察进入新帖子 URL，下一动作操作 Comment 控件；当前任务对象和可用动作发生转换。 |
| W2 | [S11→12](../samples/browser/02-repost-eagle/README.md#step-11)：两步都是 `click [14551]`，动作前的搜索页观察字符串也完全相同；未看到这次点击推进页面状态。来源最终为 `success=false`；不能由此断言环境内部完全没有变化。 |
| W3 | [S9→10](../samples/browser/03-promote-repository/README.md#step-9)：导航后下一观察已取得 AndroidAsync 项目页。[S10→11](../samples/browser/03-promote-repository/README.md#step-10)：再次 `tab_focus 0`，两条可见观察完全相同，仍显示 Tab 1 为 current；未见把项目描述写回表单，来源为失败。取得页面不等于已完成其后续用途。 |
| Q1 | [S6→21](../samples/research-qa/01-pharaoh-order/README.md#step-21)：较早打开的文档 cursor=4 被再次按 `loc=18` 取回局部行。[S21→23](../samples/research-qa/01-pharaoh-order/README.md#step-23)：最终回答引用具体行，提取人物事实并列出四个名字；原文来源与局部证据有可追踪关联。 |
| Q2 | [S3→24](../samples/research-qa/02-image-personalization/README.md#step-24)：同一 arXiv 摘要被再次打开，L0–L25 内容相同，显示 cursor 从 1 变为 21；正文重复但引用标识不同。[S25](../samples/research-qa/02-image-personalization/README.md#step-25)：相应 PDF 返回 corpus 404；摘要可读不保证全文可取。 |
| Q3 | [S6→44](../samples/research-qa/03-football-finalist/steps-01.md#step-6)：相同 Excel 路径两次交给 browser.open，均 corpus 404，没有取得文件内容；这证明所用工具访问失败，不证明文件不存在。[S110](../samples/research-qa/03-football-finalist/steps-02.md#step-110)：final 写 Fitzroy，而来源顶层 `answer` 为 Hawthorn，`status=success` 只反映运行状态，不能消除内部不一致。 |
| F1 | [R9→11](../samples/freeinference/01-append/README.md#request-9)：18,167 token 的新工具结果进入后，输入由 15,349 增至 33,603；下一请求 tool 角色仍为 22,032 token，共享前缀 33,600。支持历史被继续携带；未知其中哪些内容在语义上仍需使用。 |
| F2 | [R24→25](../samples/freeinference/02-injection/README.md#request-24)：输入只增长 87 token，`injection` 改写后共享前缀为 20,064 token、65.59%；整体长度变化不足以描述前缀状态变化。没有正文，不能判定插入了什么。 |
| F3 | [R21→23](../samples/freeinference/03-dropped-turns/README.md#request-21)：删除历史后输入从 94,984 降至 44,385，共享前缀只剩 12,848；下一请求共享前缀恢复为 44,384。缩短历史、保持前缀与语义有效性是不同判断。 |

## 3. 共性对照与结论

“支持”表示存在具体执行证据；“不足”表示没有相应观察，不能作为反例。以下不估计性质的总体发生率。

| 候选 property | 数据分析 / SQL | 软件修复 | 网页操作 | 检索问答 | FreeInference 补充 | 成立条件与例外 |
|---|---|---|---|---|---|---|
| P1：信息可跨多步继续使用，后续显式需求可转向局部片段或派生产物 | 支持：D2 S3→11 延迟使用公司描述；D1/D3 将结果转成统计或名单 | 支持：S1/S3 的具体失败输入驱动局部修改及复测 | 局部支持：W1 从表单转到帖子和 Comment；W3 取得页面后未完成用途 | 支持：Q1 从文档定位行，再生成四名列表 | 不足：F1 只能证明携带，不能证明语义使用 | 指当前可见执行路径，不能推成“局部产物已覆盖所有未来问题”；D1 单行日期样例也不足以覆盖全表 |
| P2：相同调用或相同观察再次出现，既可能是验证，也可能是无变化重试；重复不等于无用 | D2 支持旧结果再用；未观察到完全相同 SQL 的重复获取，不推断逐轮全文重发 | 支持：S1 S20/24、S3 S30/34，同命令在修改前后验证不同状态 | 支持：W2 S11/12、W3 S10/11 动作和可见观察相同，未见推进 | 支持：Q2 S3/24 摘要重复；Q3 S6/44 重复访问失败 | F1 直接支持输入携带重复；与重复获取不是同一指标 | 区分读、写、重试、复核及对象状态；可见观察相同不保证隐藏状态相同 |
| P3：对象地址是定位依据，不是恢复同一观察的充分条件 | 正例：D1 S5→6 当时通过存储键成功读文件 | 支持边界：S2 stash/pop 依赖版本状态；S3 S67 删除脚本使仅有路径不足 | 支持：W1 同 URL 下表单值变化，URL 未编码完整交互状态 | 支持边界：Q2 摘要可取而 PDF 404；Q3 给出路径但工具无法读取 | 不足：块 ID 不能还原未发布正文 | 需要对应工具、可达存储及对象状态；本次未验证跨环境、跨会话的重取一致性 |

**P1：应跟踪“还在哪里被用”，而非只看“多久没出现”。** D2 的公司描述在 S3 取得，直到 S11 才再次读取；Q1 的文档也跨多步被定位使用。D1 的完整交易结果随后转成统计结果，W1 的下一动作则聚焦于当前页面控件。对管理的启示是记录观察到派生产物/下一动作的引用关系，并区分已完成与尚未完成的用途。这里的显式引用是证据，未引用部分是否可删仍未知，不能直接用“保留最近 K 轮”或“输出变短了”判定失活。

**P2：去重之前要先识别为什么重复。** S1 的同一脚本在源码修改后重跑，输出由失败变成功，不能用旧结果代替；W2 的相同点击与相同观察却没有提供新的可见状态；Q2 还出现正文相同但 cursor 不同。对压缩或 trace 管理的启示是分别保留对象状态、最近结果、重试次数和引用标识映射，再考虑合并稳定的重复观察。此建议不等于已经证明可删历史，也不能把重复写操作当成可安全省略的读操作。

**P3：移出 context 后能否取回，需要单独成立的恢复条件。** D1 给出“存储键→文件→实际读取”的正例；Q3 则直接反驳“给出路径就能取回”，W1 反驳“同 URL 就是同一页面状态”，S3 提醒临时文件生命周期会结束。应至少标注内容来源、对象状态、访问工具及失败状态。只有这些条件满足时，handle 才可能替代长期携带的正文；轨迹中曾经可读，不代表本地仓库现在保存了该文件。

## 4. 尚不能成立的判断

- **不能给出跨应用的可安全删除比例、token 节省或正确率保证。** 本次没有进行压缩续跑；显式使用局部信息不等于局部信息对所有后续行为充分。D1 的日期格式反例尤其说明早期样例不能替代全量约束。
- **不能从普通消息日志推出每次模型输入重复多少。** 四类正文轨迹没有统一的逐请求输入快照；只有 FreeInference 提供块级输入指标，且没有正文，不能反向补出语义用途或应用分类。
- **尚未观察到数据库被更新、检索文档被在线修改。** 软件和交互页面有直接状态变化证据；数据库/文档的失效条件不能据此写成已验证的全应用规律。Q2 只能证明两次取得的摘要行相同，不能证明 URL 永久不变。
- **重复不是普遍可省略，入口也不是普遍可恢复。** S1/S3 是“同调用可直接复用旧结果”的反例；Q3 是“有路径即可恢复”的反例。W3 未完成任务、S2 `resolved=0`、Q3 答案字段不一致，均保留为边界，不被包装成成功压缩证据。

本报告的产出是已有 evidence 的归纳：最有支撑的管理对象是**带后续用途、对象状态与恢复条件的观察**。没有新增数据、模型调用、缓存模拟或压缩实现。
