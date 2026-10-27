# 复现 FreeInference 周级分析

[报告](README.md) · [FreeInference 首页](../README.md)

本报告是已完成运行的公开副本。下列步骤从固定数据与代码版本重新生成结果，不运行轨迹中的工具，也不调用大模型。工作目录从本仓库根目录开始，需要 Python 3.12、Git 和 zstd。

## 1. 准备环境与官方代码

```bash
python3.12 -m venv .venv-freeinference
.venv-freeinference/bin/python -m pip install -r samples/freeinference/report/requirements.txt
mkdir -p tmp/freeinference
git clone --filter=blob:none --sparse https://github.com/HarvardMadSys/freeinference_agentic_trace tmp/freeinference/upstream
git -C tmp/freeinference/upstream sparse-checkout set release simulation
git -C tmp/freeinference/upstream checkout 925a718eed7cc01255e7dcea024e70389cf021e5
```

## 2. 只下载选定一周，按官方逻辑校验

公开数据共 12 个文件、约 26 MB，解压后更大。下载版本固定为 `16d3c04dae6ccaa0c48a9064e204e3a8f1eb9ade`，不会下载其余 15 周。将缓存放在本仓库 tmp 下，便于清理。

```bash
HF_HOME="$PWD/tmp/freeinference/hf-cache" PYTHONPATH="$PWD/tmp/freeinference/upstream" .venv-freeinference/bin/python - <<'PY'
from pathlib import Path
from huggingface_hub import snapshot_download
from release.download import lay_out_week

week = '2026-05-17_2026-05-23'
hub = Path('tmp/freeinference/hub')
snapshot_download(
    repo_id='harvardMadsys/freeinference_agentic_trace', repo_type='dataset',
    revision='16d3c04dae6ccaa0c48a9064e204e3a8f1eb9ade', local_dir=hub, token=False,
    allow_patterns=[f'release/{week}/manifest.json', f'release/{week}/processed/*', f'release/{week}/traces/*'],
    max_workers=3,
)
lay_out_week(hub / 'release' / week, Path('tmp/freeinference/release') / week, tables=True, traces=True)
print('Official table and raw-trace checksum checks passed.')
PY
```

## 3. 运行未修改的官方模拟

```bash
PYTHONPATH="$PWD/tmp/freeinference/upstream" .venv-freeinference/bin/python -m simulation \
  --week 2026-05-17 --release tmp/freeinference/release \
  --output tmp/freeinference/simulation --processes 2
```

输出的 tallies.parquet 是四种策略 × 13 个 TTL；另外生成 totals、逐请求无限 TTL 未命中统计和 cheaper-reads 假设价格模型。运行结果可与本仓库 [official-simulation](official-simulation/2026-05-17_2026-05-23/) 比较。不同 Parquet 写入器可能生成不同文件字节，应比较表中数值和来源清单，而非只比较输出文件哈希。

## 4. 重算自定义指标与三条样本

```bash
.venv-freeinference/bin/python samples/freeinference/report/scripts/analyze_freeinference.py \
  --inputs tmp/freeinference/release/2026-05-17_2026-05-23/traces/2026-05-17.jsonl \
  --output tmp/freeinference/recomputed/day --export-samples
.venv-freeinference/bin/python samples/freeinference/report/scripts/analyze_freeinference.py \
  --inputs tmp/freeinference/release/2026-05-17_2026-05-23/traces/*.jsonl \
  --output tmp/freeinference/recomputed/week
```

脚本生成 metrics.json、逐请求/逐会话/按 harness 的 CSV。--export-samples 额外导出固定三条会话的完整 JSON、阅读用 JSON 和逐轮表。新结果写入 tmp，仓库中的阅读材料不被覆盖。

## 5. 验证与图表数据

原始运行的校验见 [validation.json](validation.json)，包括官方哈希检查、三条样本 JSON 等价、所有 52 组 hit+miss 与完整块输入总量一致、逐请求键一致，以及无限 TTL 未命中总量一致。

图表数据分别来自 [三条会话逐轮表](../README.md)、[周级逐请求表](week/request_metrics.csv) 和 [52 组模拟 CSV](official-simulation-summary.csv)。PNG 与 PDF 已保存在 figures/。图表是展示产物，不代表新增模拟策略。

[reproduction.json](reproduction.json) 保留实际运行的数据/代码版本、依赖、源文件哈希、耗时和退出码；为便于公开阅读，将本地绝对路径改成了相对路径，并明确记录了这一改动。数值与已完成的本地运行一致。
