# 数据分析 / Agentic SQL

[首页](../../README.md) · [六任务映射与管理候选](../../reports/dab-six-case-mapping-2026-10-30.md) · [跨应用决策点](../../reports/context-management-decision-points-2026-10-30.md)

共 6 个不同任务，各保留一条来源完整轨迹；包含小标量、大结果恢复、延迟引用、双结果计算和聚合口径对照。来源消息完整不等于外部结果文件或环境完整；提交答案未作独立核验。

| ID / 样本 | 原始来源 | 任务 | 消息 / 步骤 / 调用 | 阅读入口 |
|---|---|---|---|---|
| D1 · 亚洲股指平均日内波动率 | `stockindex/query1` | 找出 2020 年以来平均日内波动率最高的亚洲股票指数。 | 18 / 7 / 9 | [完整步骤](01-asian-index/README.md) · [映射](01-asian-index/mapping.md) · [JSON](01-asian-index/trace.json) |
| D2 · 财务困难公司的平均成交量 | `stockmarket/query3` | 筛选 NASDAQ 财务困难公司，计算 2008 年非空平均日成交量。 | 26 / 12 / 12 | [完整步骤](02-trading-volume/README.md) · [映射](02-trading-volume/mapping.md) · [JSON](02-trading-volume/trace.json) |
| D3 · 英文文学类满分图书 | `bookreview/query2` | 找出英文 Literature & Fiction 图书中平均评分为 5.0 的全部图书。 | 15 / 5 / 8 | [完整步骤](03-perfect-rated-books/README.md) · [映射](03-perfect-rated-books/mapping.md) · [JSON](03-perfect-rated-books/trace.json) |
| D4 · RealReal 的最高调整收盘价 | `stockmarket/query1` | 查询 The RealReal, Inc. 在 2020 年的最高调整收盘价。 | 8 / 3 / 3 | [完整步骤](04-realreal-max-price/README.md) · [映射](04-realreal-max-price/mapping.md) · [JSON](04-realreal-max-price/trace.json) |
| D5 · 工作日晚间营业的高评分商户 | `googlelocal/query3` | 找出至少一个工作日 18 点后仍营业、平均评分最高的前 5 家商户，返回名称、时间和评分。 | 20 / 9 / 9 | [完整步骤](05-evening-businesses/README.md) · [映射](05-evening-businesses/mapping.md) · [JSON](05-evening-businesses/trace.json) |
| D6 · Indianapolis 商户的平均评分 | `yelp/query1` | 查询位于 Indianapolis, Indiana 的商户的平均评分。 | 20 / 9 / 9 | [完整步骤](06-indianapolis-ratings/README.md) · [映射](06-indianapolis-ratings/mapping.md) · [JSON](06-indianapolis-ratings/trace.json) |
