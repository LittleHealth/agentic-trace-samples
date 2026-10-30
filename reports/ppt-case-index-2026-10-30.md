# 案例与 JSON 定位

[首页](../README.md) · [数据分析六任务](../samples/data-analysis/README.md) · [分析目录](README.md)

下表对应 2026-10-30 的 11 页介绍材料。相同案例在不同页重复使用，合计十个不同的正文案例；所有记录来自已有公开来源，本次未运行新 agent，也未补写步骤。

- **先读 README**：任务、按顺序排列的调用与返回、来源和结束状态。折叠块内保留完整调用与观察。
- **查看 trace.json**：增加缩进并展开工具参数，便于直接阅读。
- **核对 trace.raw.json**：同目录下保留来源原始格式；它不要求重新排版。
- **S 是原步骤号**，消息索引从 **0** 开始。一个步骤可以包含多个工具调用，不能把步骤号直接当作消息索引。

## 十个正文案例

| 页码 | 案例 | 逐步阅读 | 可读 JSON | 重点位置 |
|---|---|---|---|---|
| 2、8、9、10 | 工作日晚间营业的高评分商户 | [步骤](../samples/data-analysis/05-evening-businesses/README.md) | [trace.json](../samples/data-analysis/05-evening-businesses/trace.json) | 顶层消息 `[10]`–`[19]`：两份查询结果、读取失败、重新读取并计算、提交答案。计算前位置为 `[15]` 后、`[16]` 前。 |
| 3、7 | 路径转换修复 | [步骤](../samples/software-repair/01-posix-path/README.md) | [trace.json](../samples/software-repair/01-posix-path/trace.json) | `trajectory[40]`–`[49]`：复现失败、读取函数、修改与复测；`trajectory[90]`：结束提交。 |
| 4、7 | 发布关系求助帖 | [步骤](../samples/browser/01-relationship-post/README.md) | [trace.json](../samples/browser/01-relationship-post/trace.json) | `trajectory[2]`–`[8]`：填表、提交、新帖子、评论与结束。同条记录先看 `observation`，再看 `action`。 |
| 5、6 | 四位法老排序 | [步骤](../samples/research-qa/01-pharaoh-order/README.md) | [trace.json](../samples/research-qa/01-pharaoh-order/trace.json) | `messages[19]`–`[23]`：打开资料与查找；`messages[64]`–`[70]`：再次读取和最后回答。 |
| 6、9 | 财务困难公司的平均成交量 | [步骤](../samples/data-analysis/02-trading-volume/README.md) | [trace.json](../samples/data-analysis/02-trading-volume/trace.json) | 顶层 `[6]` / `[7]`：S3 取得公司介绍；`[22]` / `[23]`：S11 读回，结合成交量。 |
| 8 | 足球决赛资料读取失败 | [步骤](../samples/research-qa/03-football-finalist/README.md) | [trace.json](../samples/research-qa/03-football-finalist/trace.json) | `messages[19]` / `[20]` 与 `[133]` / `[134]`：同一路径两次返回 404。只说明工具未取得内容，不证明文件不存在。 |
| 9 | 亚洲股指平均日内波动率 | [步骤](../samples/data-analysis/01-asian-index/README.md) | [trace.json](../samples/data-analysis/01-asian-index/trace.json) | 顶层 `[12]`–`[15]`：S5 查询大结果，S6 读取完整文件并计算。 |
| 9 | 英文文学类满分图书 | [步骤](../samples/data-analysis/03-perfect-rated-books/README.md) | [trace.json](../samples/data-analysis/03-perfect-rated-books/trace.json) | 顶层 `[8]`–`[12]`：S3 两份查询结果，S4 匹配得到 15 本书。 |
| 9 | RealReal 的最高调整收盘价 | [步骤](../samples/data-analysis/04-realreal-max-price/README.md) | [trace.json](../samples/data-analysis/04-realreal-max-price/trace.json) | 顶层 `[4]` / `[5]`：数据库直接计算并返回最高值。 |
| 9 | Indianapolis 商户的平均评分 | [步骤](../samples/data-analysis/06-indianapolis-ratings/README.md) | [trace.json](../samples/data-analysis/06-indianapolis-ratings/trace.json) | 顶层 `[8]`–`[13]`：评论级平均、各商户均值、对商户均值再平均。两种平均的含义不同。 |

数据分析的 JSON 顶层就是消息数组；软件修复和网页使用 `trajectory`，问答使用 `messages`。表中的中文说明是定位摘要，不能替代原文，也不表示删减后的输入已经用于模型继续执行。

## 补充：三条 FreeInference 会话

这部分只有请求结构、长度及匿名信息，没有消息正文，单独列在正文案例之外。

| 会话 | 逐轮阅读 | 精简逐轮 JSON | 完整记录 |
|---|---|---|---|
| 持续追加 | [步骤](../samples/freeinference/01-append/README.md) | [requests.json](../samples/freeinference/01-append/requests.json) | [trace.json](../samples/freeinference/01-append/trace.json) |
| 历史注入改写 | [步骤](../samples/freeinference/02-injection/README.md) | [requests.json](../samples/freeinference/02-injection/requests.json) | [trace.json](../samples/freeinference/02-injection/trace.json) |
| 历史裁剪 | [步骤](../samples/freeinference/03-dropped-turns/README.md) | [requests.json](../samples/freeinference/03-dropped-turns/requests.json) | [trace.json](../samples/freeinference/03-dropped-turns/trace.json) |

## 记录边界

三个新增 DAB 目录与此前样本采用相同结构：任务及完整步骤在 `README.md`，原记录在 `trace.raw.json`，阅读副本在 `trace.json`。另附 `mapping.md` / `mapping.json`，记录实际查询、工具返回和后续使用；它们是从原记录整理的阅读辅助，不是新生成的 agent 轨迹。

来源中的完整消息不等于完整运行环境：大结果可能只有预览与读取入口，外部完整结果文件未随 DAB 归档提供。来源的提交或成功标记也不等于本次独立核验了答案。
