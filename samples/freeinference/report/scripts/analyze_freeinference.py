#!/usr/bin/env python3
"""Offline metadata analysis. Does not execute agent tools or reconstruct missing text."""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
import statistics
import subprocess

BLOCK = 16
SELECTED = [
    ('01-append', '38fd82c2b2f4693bcb97a6be528dccae', '持续追加', 'hermes，44 次请求，来源 transition 全为追加'),
    ('02-injection', 'd3cf2b494fbb04a8d1850c2367f5fcdd', '注入改写', 'kilo，27 次请求，含 injection 标记'),
    ('03-dropped-turns', '26b3e835fc1dc0d41af636b34005c880', '删除历史轮次', 'cline，46 次请求，含 dropped_turns 标记'),
]
ROLES = ['tool_definitions', 'system', 'user', 'assistant', 'tool']


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')


def pct(value):
    return f'{100*value:.2f}%'


def ratio(a, b):
    return a/b if b else 0.0


def lcp(a, b):
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return i
    return min(len(a), len(b))


def input_lines(path):
    if path.suffix == '.zst':
        proc = subprocess.Popen(['zstd', '-dc', str(path)], stdout=subprocess.PIPE)
        try:
            yield from proc.stdout
        finally:
            proc.stdout.close()
            assert proc.wait() == 0, path
    else:
        with path.open('rb') as handle:
            yield from handle


def csv_file(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        writer=csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)


def session_metrics(session):
    rows=[];seen=set();previous=[];previous_request=None
    for number,r in enumerate(session['requests'],1):
        blocks=r['block_ids'];tokens=sum(r['role_tokens'].values())
        assert 0 <= tokens-BLOCK*len(blocks) < BLOCK
        assert len(set(blocks))==len(blocks)
        shared=lcp(previous,blocks) if previous_request else 0
        repeated=sum(x in seen for x in blocks)
        # Chained hashes can repeat only as a prefix, not as independent later content.
        assert shared<=repeated<=len(blocks)
        assert all(x in seen for x in blocks[:repeated])
        assert all(x not in seen for x in blocks[repeated:])
        gap=(r['start_ms']-previous_request['end_ms'])/1000 if previous_request else None
        calls=r.get('tool_calls',[]);mutation=r.get('mutation') or {}
        row=dict(session_id=session['session_id'],harness=session['harness'],request_number=number,
                 step=r['step'],turn_index=r['turn_index'],model=r['model'],provider=r['provider'],
                 start_ms=r['start_ms'],end_ms=r['end_ms'],gap_from_previous_completion_s=gap,
                 input_o200k=tokens,encoded_tokens=BLOCK*len(blocks),
                 delta_input=tokens-rows[-1]['input_o200k'] if rows else None,
                 **{f'role_{role}':r['role_tokens'].get(role,0) for role in ROLES},
                 tool_input_share=ratio(r['role_tokens'].get('tool',0),tokens),
                 previous_shared_tokens=BLOCK*shared,previous_shared_share=ratio(shared,len(blocks)),
                 session_seen_tokens=BLOCK*repeated,session_seen_share=ratio(repeated,len(blocks)),
                 warm_5m_shared_tokens=BLOCK*shared if gap is not None and gap<=300 else 0,
                 warm_15m_shared_tokens=BLOCK*shared if gap is not None and gap<=900 else 0,
                 same_model_provider_as_previous=(r['model'],r['provider'])==(previous_request['model'],previous_request['provider']) if previous_request else None,
                 n_messages=r['n_messages'],transition=mutation.get('transition','initial'),cause=mutation.get('cause'),
                 step_trigger=r['step_trigger'],tool_call_count=len(calls),
                 tool_names='; '.join(c['name'] for c in calls),
                 tool_output_tokens=sum(c.get('result_tokens') or 0 for c in calls),
                 provider_prompt=r['provider_tokens'].get('prompt'),
                 provider_cached=r['provider_tokens'].get('cached'),
                 provider_completion=r['provider_tokens'].get('completion'))
        rows.append(row);seen.update(blocks);previous=blocks;previous_request=r
    total=sum(x['input_o200k'] for x in rows);encoded=sum(x['encoded_tokens'] for x in rows)
    sizes=[x['input_o200k'] for x in rows];mutations=collections.Counter(x['transition'] for x in rows)
    causes=collections.Counter(x['cause'] for x in rows if x['cause'])
    summary=dict(session_id=session['session_id'],harness=session['harness'],day=session.get('day'),requests=len(rows),
                 tool_calls=sum(x['tool_call_count'] for x in rows),first_input=sizes[0],last_input=sizes[-1],
                 peak_input=max(sizes),peak_over_first=ratio(max(sizes),sizes[0]),last_over_first=ratio(sizes[-1],sizes[0]),
                 cumulative_input_o200k=total,encoded_tokens=encoded,tool_input_tokens=sum(x['role_tool'] for x in rows),
                 tool_input_share=ratio(sum(x['role_tool'] for x in rows),total),
                 previous_shared_share=ratio(sum(x['previous_shared_tokens'] for x in rows),encoded),
                 session_seen_share=ratio(sum(x['session_seen_tokens'] for x in rows),encoded),
                 warm_5m_shared_share=ratio(sum(x['warm_5m_shared_tokens'] for x in rows),encoded),
                 warm_15m_shared_share=ratio(sum(x['warm_15m_shared_tokens'] for x in rows),encoded),
                 append=mutations['append'],mutation=mutations['mutation'],switch=mutations['switch'],
                 dropped_turns=causes['dropped_turns'],injection=causes['injection'],
                 input_decrease_steps=sum(x['delta_input'] is not None and x['delta_input']<0 for x in rows))
    return rows,summary


def export_sample(directory,session,raw,rows,summary,label,reason):
    directory.mkdir(parents=True,exist_ok=True)
    (directory/'trace.raw.json').write_bytes(raw.rstrip(b'\r\n'))
    save_json(directory/'trace.json',session)
    readable=[]
    for r,row in zip(session['requests'],rows):
        copy={k:v for k,v in r.items() if k!='block_ids'}
        copy['block_ids_summary']={'count':len(r['block_ids']),'first_8':r['block_ids'][:8],
                                  'last_8':r['block_ids'][-8:],
                                  'sha256_of_compact_json':hashlib.sha256(json.dumps(r['block_ids'],separators=(',',':')).encode()).hexdigest()}
        readable.append({'source_request':copy,'derived_metrics':row})
    save_json(directory/'requests.json',{'session_id':session['session_id'],'harness':session['harness'],
                                       'note':'block_ids 的完整数组见 trace.json；其余来源字段和工具骨架保留。',
                                       'requests':readable})
    csv_file(directory/'requests.csv',rows)
    # Independent check: union-of-hashes reuse equals the best prefix among all past requests.
    past=[]
    for r,row in zip(session['requests'],rows):
        independent=max((lcp(old,r['block_ids']) for old in past),default=0)
        assert BLOCK*independent==row['session_seen_tokens']
        past.append(r['block_ids'])
    p=[f'# {label}：{session["harness"]}', '',
       '[分析首页](../../README.md) · [可读请求 JSON](requests.json) · [完整 JSON](trace.json) · [原始记录](trace.raw.json)', '',
       f'会话 `{session["session_id"]}`。选取原因：{reason}。这是展示用选样，不用于估计类型发生率。', '',
       f'共 {len(rows)} 次请求、{summary["tool_calls"]} 次工具调用。初始输入 {summary["first_input"]:,} token，末次输入 {summary["last_input"]:,}，峰值 {summary["peak_input"]:,}。', '',
       '## 如何阅读', '',
       '一行对应一次模型请求，不一定对应一次用户对话。该行输入是发送给模型的上下文；tool_calls 是这次模型响应产生的工具调用，其结果随后才可能进入下一次请求。工具参数仅保留匿名化骨架，没有用户问题、回答或工具结果正文。', '',
       '`trace.raw.json` 保留来源记录，`trace.json` 只增加缩进；`requests.json` 保留各请求字段并附加计算指标，将很长的 block_ids 数组明确替换为摘要，完整数组仍在 trace.json。', '',
       '## 逐轮请求', '',
       '输入和 tool 角色占比使用 o200k_base。tool 角色为 0 不代表没有工具结果：某些框架会把观察放入 user 消息，匿名数据无法完整分离。新工具结果 token 为本次响应所调用工具的 result_tokens 之和，不能与本行输入重复计算。共享前缀按完整 16-token 块统计；首轮共享值为 0。编号从 1 开始，step 为来源索引。', '',
       '| 请求 | step | 触发 | 输入 token | 较上轮变化 | tool 角色占比 | 与上轮共享前缀 | 历史已见块占比 | transition / cause | 本次响应的工具调用 | 新工具结果 token |',
       '|---:|---:|---|---:|---:|---:|---:|---:|---|---|---:|']
    for x in rows:
        change='—' if x['delta_input'] is None else f'{x["delta_input"]:+,}'
        names=x['tool_names'].replace('|','\\|') or '—'
        p.append(f'| [{x["request_number"]}](#request-{x["request_number"]}) | {x["step"]} | {x["step_trigger"]} | {x["input_o200k"]:,} | {change} | {pct(x["tool_input_share"])} | {x["previous_shared_tokens"]:,} ({pct(x["previous_shared_share"] )}) | {pct(x["session_seen_share"])} | {x["transition"]} / {x["cause"] or "—"} | {names} | {x["tool_output_tokens"]:,} |')
    for x,r in zip(rows,session['requests']):
        p += ['',f'<a id="request-{x["request_number"]}"></a>','',f'### 请求 {x["request_number"]}', '',
              '<details>', '<summary>展开模型、token、变化标记和工具骨架</summary>', '', '```json',
              json.dumps({k:v for k,v in r.items() if k!='block_ids'},ensure_ascii=False,indent=2), '```', '', '</details>']
    p += ['', '## 阅读边界', '',
          '工具 arguments 是匿名化骨架，outcome、result_tokens 和 latency_ms 是观察元数据；没有工具结果正文。latency_ms 按来源定义是至下一模型请求的间隔，不能直接当作精确工具执行耗时。mutation 原样照录，不据其标签推断被删除内容是否已完成用途。', '',
          '来源：[数据集](https://huggingface.co/datasets/harvardMadsys/freeinference_agentic_trace) · [官方仓库](https://github.com/HarvardMadSys/freeinference_agentic_trace)。固定数据版本与统计口径见分析首页。', '',
          f'来源：FreeInference `2026-05-17`，原始记录 SHA-256 `{hashlib.sha256(raw.rstrip(b"\r\n")).hexdigest()}`。']
    (directory/'README.md').write_text('\n'.join(p)+'\n',encoding='utf-8')


def analyze(paths,output,export=False):
    output.mkdir(parents=True,exist_ok=True)
    requests=[];sessions=[];input_sources=[];top_count=0;nested_count=0
    for path in paths:
        digest=hashlib.sha256();lines=0
        for raw in input_lines(path):
            digest.update(raw)
            if not raw.strip():continue
            session=json.loads(raw);top_count+=1;lines+=1
            def count_nested(s):
                return sum(1+count_nested(c['subagent']) for r in s['requests'] for c in r.get('tool_calls',[]) if c.get('subagent'))
            nested_count+=count_nested(session)
            if session['harness']=='eval:swe-bench':continue
            rows,summary=session_metrics(session);requests.extend(rows);sessions.append(summary)
            if export:
                for slug,id_,label,reason in SELECTED:
                    if session['session_id']==id_:export_sample(output/'samples'/slug,session,raw,rows,summary,label,reason)
        input_sources.append({'path':str(path.resolve()),'lines':lines,'uncompressed_sha256':digest.hexdigest()})
    assert len({(r['session_id'],r['step']) for r in requests})==len(requests)
    assert len({s['session_id'] for s in sessions})==len(sessions)
    total=sum(x['input_o200k'] for x in requests);encoded=sum(x['encoded_tokens'] for x in requests)
    roles={role:sum(x['role_'+role] for x in requests) for role in ROLES}
    available=[x for x in requests if x['provider_cached'] is not None and x['provider_prompt'] is not None]
    summary=dict(population='Agentic top-level sessions; eval:swe-bench and nested sessions excluded from metrics',
                 top_level_sessions_in_files=top_count,nested_sessions_in_files=nested_count,sessions=len(sessions),requests=len(requests),
                 tool_calls=sum(x['tool_call_count'] for x in requests),input_o200k=total,encoded_tokens=encoded,
                 omitted_partial_block_tokens=total-encoded,role_tokens=roles,tool_input_share=ratio(roles['tool'],total),
                 previous_shared_share=ratio(sum(x['previous_shared_tokens'] for x in requests),encoded),
                 session_seen_share=ratio(sum(x['session_seen_tokens'] for x in requests),encoded),
                 warm_5m_shared_share=ratio(sum(x['warm_5m_shared_tokens'] for x in requests),encoded),
                 warm_15m_shared_share=ratio(sum(x['warm_15m_shared_tokens'] for x in requests),encoded),
                 median_peak_over_first=statistics.median(x['peak_over_first'] for x in sessions),
                 sessions_peak_at_least_twice_first=sum(x['peak_over_first']>=2 for x in sessions),
                 median_session_tool_share=statistics.median(x['tool_input_share'] for x in sessions),
                 median_session_previous_shared_share=statistics.median(x['previous_shared_share'] for x in sessions),
                 request_input_median=statistics.median(x['input_o200k'] for x in requests),
                 request_input_peak=max(x['input_o200k'] for x in requests),
                 transitions=dict(collections.Counter(x['transition'] for x in requests)),
                 causes=dict(collections.Counter(x['cause'] for x in requests if x['cause'])),
                 input_decrease_steps=sum(x['delta_input'] is not None and x['delta_input']<0 for x in requests),
                 model_provider_switch_steps=sum(x['same_model_provider_as_previous'] is False for x in requests),
                 provider_cache_count_coverage=len(available),
                 provider_reported_cache_share_on_available=ratio(sum(x['provider_cached'] for x in available),sum(x['provider_prompt'] for x in available)),
                 sources=input_sources)
    save_json(output/'metrics.json',summary);csv_file(output/'session_metrics.csv',sessions);csv_file(output/'request_metrics.csv',requests)
    per_harness=[]
    for harness in sorted({x['harness'] for x in sessions}):
        sr=[x for x in sessions if x['harness']==harness];rr=[x for x in requests if x['harness']==harness]
        denom=sum(x['input_o200k'] for x in rr);blocks=sum(x['encoded_tokens'] for x in rr)
        per_harness.append(dict(harness=harness,sessions=len(sr),requests=len(rr),input_o200k=denom,
                                tool_input_share=ratio(sum(x['role_tool'] for x in rr),denom),
                                previous_shared_share=ratio(sum(x['previous_shared_tokens'] for x in rr),blocks),
                                session_seen_share=ratio(sum(x['session_seen_tokens'] for x in rr),blocks),
                                median_peak_over_first=statistics.median(x['peak_over_first'] for x in sr)))
    csv_file(output/'harness_metrics.csv',per_harness)
    lines=['# FreeInference 元数据分析','',f'{len(sessions)} 个 Agentic 顶层会话，{len(requests):,} 次请求。','',
           '| 指标 | 结果 |','|---|---:|',
           f'| 累计输入（o200k_base） | {total:,} |',f'| 工具消息在累计输入中的占比 | {pct(summary["tool_input_share"])} |',
           f'| 与上一请求共享的前缀 / 全部完整块 | {pct(summary["previous_shared_share"])} |',
           f'| 同会话历史已见块 / 全部完整块 | {pct(summary["session_seen_share"])} |',
           f'| 上一请求完成后 5 分钟内共享前缀 / 全部完整块 | {pct(summary["warm_5m_shared_share"])} |',
           f'| 会话峰值 / 初始输入，中位数 | {summary["median_peak_over_first"]:.2f}× |',
           f'| 峰值至少为初始两倍的会话 | {summary["sessions_peak_at_least_twice_first"]}/{len(sessions)} |','',
           '[完整指标](metrics.json) · [会话表](session_metrics.csv) · [逐请求表](request_metrics.csv) · [按 harness 分组](harness_metrics.csv)','']
    if export:
        lines+=['## 三个会话','']
        for slug,_,label,_ in SELECTED:lines.append(f'- [{label}](samples/{slug}/README.md)：逐轮表、可读请求 JSON 和完整记录。')
    lines+=['','## 指标解释','',
            '输入 = tool_definitions + system + user + assistant + tool，使用同一 o200k_base 口径。tool 占比是来源标为 tool 角色的输入占比，包含重复输入的旧结果；部分框架把工具观察放在其他角色，不能据此计算全部工具结果的语义占比。工具新产出的 result_tokens 单独记录，不拿它作为历史重复次数的分母。','',
            '共享前缀取同一会话相邻输入的 block_ids 最长公共前缀；历史已见块取当前块中在该会话任意早先请求出现过的块。每个 ID 为链式前缀哈希，不能据它识别改写后后缀中相同的独立段落。首轮的两个复用量都为 0。复用量包含系统提示和工具定义，不能全部归因于对话历史。','',
            '所有比率均用累计 token 或完整块加权；同时保存会话级中位数。最后不足 16 token 的部分未进入块指标。provider_tokens 是供应商口径，不能与 o200k_base 角色计数混为一谈；cached 缺失值不按 0 处理。','',
            '历史块重复与连续前缀复用衡量重复读取和缓存机会，不证明这些内容可以从推理输入中删除，也不衡量压缩后的答案正确率。harness 是执行框架标签，不能据此划分具体 application。']
    (output/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    if export:
        decision=dict(decision='continue_one_week',basis='exploratory descriptive evidence; made before weekly data analysis',
                      evidence={'tool_input_share':summary['tool_input_share'],'previous_shared_share':summary['previous_shared_share'],
                                'median_peak_over_first':summary['median_peak_over_first'],'transitions':summary['transitions']},
                      conclusion='工具消息占比、显著输入增长、可测的重复前缀和改写共同支持扩展一周，研究缓存与上下文维护的权衡；不支持语义压缩安全性结论。')
        save_json(output/'decision.json',decision)
    print(json.dumps({k:v for k,v in summary.items() if k!='sources'},ensure_ascii=False,indent=2))
    return summary


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--inputs',nargs='+',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--export-samples',action='store_true')
    args=parser.parse_args();analyze(args.inputs,args.output,args.export_samples)
