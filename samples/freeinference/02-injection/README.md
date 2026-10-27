# 注入改写：kilo

[FreeInference 首页](../README.md) · [分析报告](../report/README.md) · [可读请求 JSON](requests.json) · [完整 JSON](trace.json) · [原始记录](trace.raw.json)

会话 `d3cf2b494fbb04a8d1850c2367f5fcdd`。选取原因：kilo，27 次请求，含 injection 标记。这是展示用选样，不用于估计类型发生率。

共 27 次请求、20 次工具调用。初始输入 15,531 token，末次输入 30,651，峰值 30,651。

## 如何阅读

一行对应一次模型请求，不一定对应一次用户对话。该行输入是发送给模型的上下文；tool_calls 是这次模型响应产生的工具调用，其结果随后才可能进入下一次请求。工具参数仅保留匿名化骨架，没有用户问题、回答或工具结果正文。

`trace.raw.json` 保留来源记录，`trace.json` 只增加缩进；`requests.json` 保留各请求字段并附加计算指标，将很长的 block_ids 数组明确替换为摘要，完整数组仍在 trace.json。

## 逐轮请求

输入和 tool 角色占比使用 o200k_base。tool 角色为 0 不代表没有工具结果：某些框架会把观察放入 user 消息，匿名数据无法完整分离。新工具结果 token 为本次响应所调用工具的 result_tokens 之和，不能与本行输入重复计算。共享前缀按完整 16-token 块统计；首轮共享值为 0。编号从 1 开始，step 为来源索引。

| 请求 | step | 触发 | 输入 token | 较上轮变化 | tool 角色占比 | 与上轮共享前缀 | 历史已见块占比 | transition / cause | 本次响应的工具调用 | 新工具结果 token |
|---:|---:|---|---:|---:|---:|---:|---:|---|---|---:|
| [1](#request-1) | 0 | user | 15,531 | — | 7.57% | 0 (0.00%) | 0.00% | initial / — | glob | 377 |
| [2](#request-2) | 1 | tool | 15,940 | +409 | 9.75% | 15,520 (97.39%) | 97.39% | append / — | — | 0 |
| [3](#request-3) | 2 | user | 16,091 | +151 | 9.66% | 15,456 (96.12%) | 96.12% | mutation / injection | webfetch | 1,114 |
| [4](#request-4) | 3 | tool | 17,232 | +1,141 | 15.49% | 16,080 (93.31%) | 93.31% | append / — | bash | 20 |
| [5](#request-5) | 4 | tool | 17,306 | +74 | 15.56% | 17,232 (99.63%) | 99.63% | append / — | bash | 131 |
| [6](#request-6) | 5 | tool | 17,473 | +167 | 16.17% | 17,296 (98.99%) | 98.99% | append / — | bash | 277 |
| [7](#request-7) | 6 | tool | 17,780 | +307 | 17.46% | 17,472 (98.29%) | 98.29% | append / — | bash | 200 |
| [8](#request-8) | 7 | tool | 18,014 | +234 | 18.35% | 17,776 (98.76%) | 98.76% | append / — | bashbash | 3 |
| [9](#request-9) | 8 | tool | 18,053 | +39 | 18.34% | 18,000 (99.73%) | 99.73% | append / — | bash | 23 |
| [10](#request-10) | 9 | tool | 18,131 | +78 | 18.40% | 18,048 (99.56%) | 99.56% | append / — | bash | 280 |
| [11](#request-11) | 10 | tool | 18,444 | +313 | 19.62% | 18,128 (98.35%) | 98.35% | append / — | glob | 28 |
| [12](#request-12) | 11 | tool | 18,506 | +62 | 19.71% | 18,432 (99.65%) | 99.65% | append / — | bash | 3 |
| [13](#request-13) | 12 | tool | 18,567 | +61 | 19.67% | 18,496 (99.66%) | 99.66% | append / — | bash | 66 |
| [14](#request-14) | 13 | tool | 18,689 | +122 | 19.91% | 18,560 (99.32%) | 99.32% | append / — | — | 0 |
| [15](#request-15) | 14 | user | 18,743 | +54 | 19.85% | 16,016 (85.48%) | 85.48% | mutation / injection | read | 1,162 |
| [16](#request-16) | 15 | tool | 19,935 | +1,192 | 24.50% | 18,736 (94.06%) | 94.06% | append / — | — | 0 |
| [17](#request-17) | 16 | user | 20,148 | +213 | 24.25% | 18,672 (92.69%) | 92.69% | mutation / injection | glob | 2,458 |
| [18](#request-18) | 17 | tool | 22,630 | +2,482 | 32.46% | 20,144 (89.04%) | 89.04% | append / — | read | 810 |
| [19](#request-19) | 18 | tool | 23,465 | +835 | 34.76% | 22,624 (96.45%) | 96.45% | append / — | read | 620 |
| [20](#request-20) | 19 | tool | 24,114 | +649 | 36.41% | 23,456 (97.28%) | 97.28% | append / — | glob | 19 |
| [21](#request-21) | 20 | tool | 24,160 | +46 | 36.42% | 24,112 (99.80%) | 99.80% | append / — | glob | 15 |
| [22](#request-22) | 21 | tool | 24,201 | +41 | 36.43% | 24,160 (99.87%) | 99.87% | append / — | grep | 6,220 |
| [23](#request-23) | 22 | tool | 30,459 | +6,258 | 49.37% | 24,192 (79.45%) | 79.45% | append / — | read | 24 |
| [24](#request-24) | 23 | tool | 30,513 | +54 | 49.37% | 30,448 (99.79%) | 99.79% | append / — | — | 0 |
| [25](#request-25) | 24 | user | 30,600 | +87 | 49.23% | 20,064 (65.59%) | 65.59% | mutation / injection | — | 0 |
| [26](#request-26) | 25 | user | 30,627 | +27 | 49.19% | 30,528 (99.69%) | 99.69% | mutation / injection | — | 0 |
| [27](#request-27) | 26 | user | 30,651 | +24 | 49.15% | 30,544 (99.69%) | 99.69% | mutation / injection | — | 0 |

<a id="request-1"></a>

### 请求 1

<details>
<summary>展开模型、token、变化标记和工具骨架</summary>

```json
{
  "step": 0,
  "turn_index": 0,
  "step_trigger": "user",
  "link_reason": null,
  "start_ms": 1779018068851,
  "end_ms": 1779018070036,
  "ttft_ms": 972,
  "model": "minimax-m2.7",
  "provider": "G",
  "stream": true,
  "provider_tokens": {
    "prompt": 5389,
    "completion": 0,
    "cached": null
  },
  "role_tokens": {
    "system": 3832,
    "user": 115,
    "assistant": 374,
    "tool": 1175,
    "tool_definitions": 10035
  },
  "n_messages": 14,
  "tool_definition_names": [
    "question",
    "bash",
    "read",
    "glob",
    "grep",
    "edit",
    "write",
    "task",
    "webfetch",
    "todowrite",
    "skill",
    "suggest",
    "kilo_local_recall"
  ],
  "finish_reason": "tool_calls",
  "mutation": null,
  "tool_calls": [
    {
      "call_index": 0,
      "name": "glob",
      "category": "Read",
      "programs": null,
      "parse_status": null,
      "arguments": [
        [
          "path",
          "<path>"
        ],
        [
          "pattern",
          "<path>"
        ]
      ],
      "outcome": "ok",
      "result_tokens": 377,
      "latency_ms": 5847,
      "subagent": null
    }
  ]
}
```

</details>

<a id="request-2"></a>

### 请求 2

<details>
<summary>展开模型、token、变化标记和工具骨架</summary>

```json
{
  "step": 1,
  "turn_index": 0,
  "step_trigger": "tool",
  "link_reason": "tool_call_id",
  "start_ms": 1779018075883,
  "end_ms": 1779018077360,
  "ttft_ms": 1263,
  "model": "minimax-m2.7",
  "provider": "G",
  "stream": true,
  "provider_tokens": {
    "prompt": 5775,
    "completion": 118,
    "cached": null
  },
  "role_tokens": {
    "system": 3832,
    "user": 115,
    "assistant": 404,
    "tool": 1554,
    "tool_definitions": 10035
  },
  "n_messages": 16,
  "tool_definition_names": [
    "question",
    "bash",
    "read",
    "glob",
    "grep",
    "edit",
    "write",
    "task",
    "webfetch",
    "todowrite",
    "skill",
    "suggest",
    "kilo_local_recall"
  ],
  "finish_reason": "stop",
  "mutation": {
    "transition": "append",
    "cause": null
  },
  "tool_calls": []
}
```

</details>

<a id="request-3"></a>

### 请求 3

<details>
<summary>展开模型、token、变化标记和工具骨架</summary>

```json
{
  "step": 2,
  "turn_index": 1,
  "step_trigger": "user",
  "link_reason": "assistant_message",
  "start_ms": 1779018155024,
  "end_ms": 1779018156283,
  "ttft_ms": 1037,
  "model": "minimax-m2.7",
  "provider": "G",
  "stream": true,
  "provider_tokens": {
    "prompt": 5963,
    "completion": 0,
    "cached": null
  },
  "role_tokens": {
    "system": 3832,
    "user": 157,
    "assistant": 513,
    "tool": 1554,
    "tool_definitions": 10035
  },
  "n_messages": 18,
  "tool_definition_names": [
    "question",
    "bash",
    "read",
    "glob",
    "grep",
    "edit",
    "write",
    "task",
    "webfetch",
    "todowrite",
    "skill",
    "suggest",
    "kilo_local_recall"
  ],
  "finish_reason": "tool_calls",
  "mutation": {
    "transition": "mutation",
    "cause": "injection"
  },
  "tool_calls": [
    {
      "call_index": 0,
      "name": "webfetch",
      "category": "Browser",
      "programs": null,
      "parse_status": null,
      "arguments": [
        [
          "format",
          "<str>"
        ],
        [
          "url",
          "<path>"
        ]
      ],
      "outcome": "ok",
      "result_tokens": 1114,
      "latency_ms": 4903,
      "subagent": null
    }
  ]
}
```

</details>

<a id="request-4"></a>

### 请求 4

<details>
<summary>展开模型、token、变化标记和工具骨架</summary>

```json
{
  "step": 3,
  "turn_index": 1,
  "step_trigger": "tool",
  "link_reason": "tool_call_id",
  "start_ms": 1779018161186,
  "end_ms": 1779018163553,
  "ttft_ms": 2161,
  "model": "minimax-m2.7",
  "provider": "G",
  "stream": true,
  "provider_tokens": {
    "prompt": 7098,
    "completion": 0,
    "cached": null
  },
  "role_tokens": {
    "system": 3832,
    "user": 157,
    "assistant": 538,
    "tool": 2670,
    "tool_definitions": 10035
  },
  "n_messages": 20,
  "tool_definition_names": [
    "question",
    "bash",
    "read",
    "glob",
    "grep",
    "edit",
    "write",
    "task",
    "webfetch",
    "todowrite",
    "skill",
    "suggest",
    "kilo_local_recall"
  ],
  "finish_reason": "tool_calls",
  "mutation": {
    "transition": "append",
    "cause": null
  },
  "tool_calls": [
    {
      "call_index": 0,
      "name": "bash",
      "category": "*Git/VCS",
      "programs": [
        "git clone"
      ],
      "parse_status": "success",
      "arguments": [
        [
          "command",
          "git clone --depth <num> <path> <var>"
        ],
        [
          "description",
          "<str>"
        ],
        [
          "timeout",
          "<num>"
        ]
      ],
      "outcome": "ok",
      "result_tokens": 20,
      "latency_ms": 20739,
      "subagent": null
    }
  ]
}
```

</details>

<a id="request-5"></a>

### 请求 5

<details>
<summary>展开模型、token、变化标记和工具骨架</summary>

```json
{
  "step": 4,
  "turn_index": 1,
  "step_trigger": "tool",
  "link_reason": "tool_call_id",
  "start_ms": 1779018184292,
  "end_ms": 1779018187677,
  "ttft_ms": 3154,
  "model": "minimax-m2.7",
  "provider": "G",
  "stream": true,
  "provider_tokens": {
    "prompt": 7128,
    "completion": 0,
    "cached": null
  },
  "role_tokens": {
    "system": 3832,
    "user": 157,
    "assistant": 590,
    "tool": 2692,
    "tool_definitions": 10035
  },
  "n_messages": 22,
  "tool_definition_names": [
    "question",
    "bash",
    "read",
    "glob",
    "grep",
    "edit",
    "write",
    "task",
    "webfetch",
    "todowrite",
    "skill",
    "suggest",
    "kilo_local_recall"
  ],
  "finish_reason": "tool_calls",
  "mutation": {
    "transition": "append",
    "cause": null
  },
  "tool_calls": [
    {
      "call_index": 0,
      "name": "bash",
      "category": "*File Ops",
      "programs": [
        "ls"
      ],
      "parse_status": "success",
      "arguments": [
        [
          "command",
          "ls <var>"
        ],
        [
          "description",
          "<str>"
        ]
      ],
      "outcome": "ok",
      "result_tokens": 131,
      "latency_ms": 19291,
      "subagent": null
    }
  ]
}
```

</details>

<a id="request-6"></a>

### 请求 6

<details>
<summary>展开模型、token、变化标记和工具骨架</summary>

```json
{
  "step": 5,
  "turn_index": 1,
  "step_trigger": "tool",
  "link_reason": "tool_call_id",
  "start_ms": 1779018206968,
  "end_ms": 1779018208176,
  "ttft_ms": 966,
  "model": "minimax-m2.7",
  "provider": "G",
  "stream": true,
  "provider_tokens": {
    "prompt": 7269,
    "completion": 0,
    "cached": null
  },
  "role_tokens": {
    "system": 3832,
    "user": 157,
    "assistant": 624,
    "tool": 2825,
    "tool_definitions": 10035
  },
  "n_messages": 24,
  "tool_definition_names": [
    "question",
    "bash",
    "read",
    "glob",
    "grep",
    "edit",
    "write",
    "task",
    "webfetch",
    "todowrite",
    "skill",
    "suggest",
    "kilo_local_recall"
  ],
  "finish_reason": "tool_calls",
  "mutation": {
    "transition": "append",
    "cause": null
  },
  "tool_calls": [
    {
      "call_index": 0,
      "name": "bash",
      "category": "*File Ops",
      "programs": [
        "ls"
      ],
      "parse_status": "success",
      "arguments": [
        [
          "command",
          "ls <var>"
        ],
        [
          "description",
          "<str>"
        ]
      ],
      "outcome": "ok",
      "result_tokens": 277,
      "latency_ms": 17765,
      "subagent": null
    }
  ]
}
```

</details>

<a id="request-7"></a>

### 请求 7

<details>
<summary>展开模型、token、变化标记和工具骨架</summary>

```json
{
  "step": 6,
  "turn_index": 1,
  "step_trigger": "tool",
  "link_reason": "tool_call_id",
  "start_ms": 1779018225941,
  "end_ms": 1779018228642,
  "ttft_ms": 2491,
  "model": "minimax-m2.7",
  "provider": "G",
  "stream": true,
  "provider_tokens": {
    "prompt": 7556,
    "completion": 0,
    "cached": null
  },
  "role_tokens": {
    "system": 3832,
    "user": 157,
    "assistant": 652,
    "tool": 3104,
    "tool_definitions": 10035
  },
  "n_messages": 26,
  "tool_definition_names": [
    "question",
    "bash",
    "read",
    "glob",
    "grep",
    "edit",
    "write",
    "task",
    "webfetch",
    "todowrite",
    "skill",
    "suggest",
    "kilo_local_recall"
  ],
  "finish_reason": "tool_calls",
  "mutation": {
    "transition": "append",
    "cause": null
  },
  "tool_calls": [
    {
      "call_index": 0,
      "name": "bash",
      "category": "*File Ops",
      "programs": [
        "ls"
      ],
      "parse_status": "success",
      "arguments": [
        [
          "command",
          "ls <var>"
        ],
        [
          "description",
          "<str>"
        ]
      ],
      "outcome": "ok",
      "result_tokens": 200,
      "latency_ms": 16229,
      "subagent": null
    }
  ]
}
```

</details>

<a id="request-8"></a>

### 请求 8

<details>
<summary>展开模型、token、变化标记和工具骨架</summary>

```json
{
  "step": 7,
  "turn_index": 1,
  "step_trigger": "tool",
  "link_reason": "tool_call_id",
  "start_ms": 1779018244871,
  "end_ms": 1779018246443,
  "ttft_ms": 1337,
  "model": "minimax-m2.7",
  "provider": "G",
  "stream": true,
  "provider_tokens": {
    "prompt": 7766,
    "completion": 0,
    "cached": null
  },
  "role_tokens": {
    "system": 3832,
    "user": 157,
    "assistant": 684,
    "tool": 3306,
    "tool_definitions": 10035
  },
  "n_messages": 28,
  "tool_definition_names": [
    "question",
    "bash",
    "read",
    "glob",
    "grep",
    "edit",
    "write",
    "task",
    "webfetch",
    "todowrite",
    "skill",
    "suggest",
    "kilo_local_recall"
  ],
  "finish_reason": "tool_calls",
  "mutation": {
    "transition": "append",
    "cause": null
  },
  "tool_calls": [
    {
      "call_index": 0,
      "name": "bashbash",
      "category": "Other",
      "programs": [],
      "parse_status": "failed",
      "arguments": null,
      "outcome": "ok",
      "result_tokens": 3,
      "latency_ms": 15600,
      "subagent": null
    }
  ]
}
```

</details>

<a id="request-9"></a>

### 请求 9

<details>
<summary>展开模型、token、变化标记和工具骨架</summary>

```json
{
  "step": 8,
  "turn_index": 1,
  "step_trigger": "tool",
  "link_reason": "tool_call_id",
  "start_ms": 1779018262043,
  "end_ms": 1779018263771,
  "ttft_ms": 1523,
  "model": "minimax-m2.7",
  "provider": "G",
  "stream": true,
  "provider_tokens": {
    "prompt": 7779,
    "completion": 0,
    "cached": null
  },
  "role_tokens": {
    "system": 3832,
    "user": 157,
    "assistant": 718,
    "tool": 3311,
    "tool_definitions": 10035
  },
  "n_messages": 30,
  "tool_definition_names": [
    "question",
    "bash",
    "read",
    "glob",
    "grep",
    "edit",
    "write",
    "task",
    "webfetch",
    "todowrite",
    "skill",
    "suggest",
    "kilo_local_recall"
  ],
  "finish_reason": "tool_calls",
  "mutation": {
    "transition": "append",
    "cause": null
  },
  "tool_calls": [
    {
      "call_index": 0,
      "name": "bash",
      "category": "*Git/VCS",
      "programs": [
        "git clone"
      ],
      "parse_status": "success",
      "arguments": [
        [
          "command",
          "git clone --depth <num> <path> <var>"
        ],
        [
          "description",
          "<str>"
        ],
        [
          "timeout",
          "<num>"
        ]
      ],
      "outcome": "ok",
      "result_tokens": 23,
      "latency_ms": 18695,
      "subagent": null
    }
  ]
}
```

</details>

<a id="request-10"></a>

### 请求 10

<details>
<summary>展开模型、token、变化标记和工具骨架</summary>

```json
{
  "step": 9,
  "turn_index": 1,
  "step_trigger": "tool",
  "link_reason": "tool_call_id",
  "start_ms": 1779018282466,
  "end_ms": 1779018283522,
  "ttft_ms": 796,
  "model": "minimax-m2.7",
  "provider": "G",
  "stream": true,
  "provider_tokens": {
    "prompt": 7812,
    "completion": 0,
    "cached": null
  },
  "role_tokens": {
    "system": 3832,
    "user": 157,
    "assistant": 771,
    "tool": 3336,
    "tool_definitions": 10035
  },
  "n_messages": 32,
  "tool_definition_names": [
    "question",
    "bash",
    "read",
    "glob",
    "grep",
    "edit",
    "write",
    "task",
    "webfetch",
    "todowrite",
    "skill",
    "suggest",
    "kilo_local_recall"
  ],
  "finish_reason": "tool_calls",
  "mutation": {
    "transition": "append",
    "cause": null
  },
  "tool_calls": [
    {
      "call_index": 0,
      "name": "bash",
      "category": "*File Ops",
      "programs": [
        "ls"
      ],
      "parse_status": "success",
      "arguments": [
        [
          "command",
          "ls <var>"
        ],
        [
          "description",
          "<str>"
        ]
      ],
      "outcome": "ok",
      "result_tokens": 280,
      "latency_ms": 23304,
      "subagent": null
    }
  ]
}
```

</details>

<a id="request-11"></a>

### 请求 11

<details>
<summary>展开模型、token、变化标记和工具骨架</summary>

```json
{
  "step": 10,
  "turn_index": 1,
  "step_trigger": "tool",
  "link_reason": "tool_call_id",
  "start_ms": 1779018306826,
  "end_ms": 1779018308133,
  "ttft_ms": 1088,
  "model": "minimax-m2.7",
  "provider": "G",
  "stream": true,
  "provider_tokens": {
    "prompt": 8102,
    "completion": 0,
    "cached": null
  },
  "role_tokens": {
    "system": 3832,
    "user": 157,
    "assistant": 802,
    "tool": 3618,
    "tool_definitions": 10035
  },
  "n_messages": 34,
  "tool_definition_names": [
    "question",
    "bash",
    "read",
    "glob",
    "grep",
    "edit",
    "write",
    "task",
    "webfetch",
    "todowrite",
    "skill",
    "suggest",
    "kilo_local_recall"
  ],
  "finish_reason": "tool_calls",
  "mutation": {
    "transition": "append",
    "cause": null
  },
  "tool_calls": [
    {
      "call_index": 0,
      "name": "glob",
      "category": "Read",
      "programs": null,
      "parse_status": null,
      "arguments": [
        [
          "path",
          "<path>"
        ],
        [
          "pattern",
          "<path>"
        ]
      ],
      "outcome": "ok",
      "result_tokens": 28,
      "latency_ms": 4665,
      "subagent": null
    }
  ]
}
```

</details>

<a id="request-12"></a>

### 请求 12

<details>
<summary>展开模型、token、变化标记和工具骨架</summary>

```json
{
  "step": 11,
  "turn_index": 1,
  "step_trigger": "tool",
  "link_reason": "tool_call_id",
  "start_ms": 1779018312798,
  "end_ms": 1779018315956,
  "ttft_ms": 2921,
  "model": "minimax-m2.7",
  "provider": "G",
  "stream": true,
  "provider_tokens": {
    "prompt": 8140,
    "completion": 0,
    "cached": null
  },
  "role_tokens": {
    "system": 3832,
    "user": 157,
    "assistant": 834,
    "tool": 3648,
    "tool_definitions": 10035
  },
  "n_messages": 36,
  "tool_definition_names": [
    "question",
    "bash",
    "read",
    "glob",
    "grep",
    "edit",
    "write",
    "task",
    "webfetch",
    "todowrite",
    "skill",
    "suggest",
    "kilo_local_recall"
  ],
  "finish_reason": "tool_calls",
  "mutation": {
    "transition": "append",
    "cause": null
  },
  "tool_calls": [
    {
      "call_index": 0,
      "name": "bash",
      "category": "*File Ops",
      "programs": [
        "Move-Item"
      ],
      "parse_status": "success",
      "arguments": [
        [
          "command",
          "Move-Item <var> <var>"
        ],
        [
          "description",
          "<str>"
        ]
      ],
      "outcome": "ok",
      "result_tokens": 3,
      "latency_ms": 26401,
      "subagent": null
    }
  ]
}
```

</details>

<a id="request-13"></a>

### 请求 13

<details>
<summary>展开模型、token、变化标记和工具骨架</summary>

```json
{
  "step": 12,
  "turn_index": 1,
  "step_trigger": "tool",
  "link_reason": "tool_call_id",
  "start_ms": 1779018342357,
  "end_ms": 1779018346102,
  "ttft_ms": 3516,
  "model": "minimax-m2.7",
  "provider": "G",
  "stream": true,
  "provider_tokens": {
    "prompt": 8153,
    "completion": 0,
    "cached": null
  },
  "role_tokens": {
    "system": 3832,
    "user": 157,
    "assistant": 890,
    "tool": 3653,
    "tool_definitions": 10035
  },
  "n_messages": 38,
  "tool_definition_names": [
    "question",
    "bash",
    "read",
    "glob",
    "grep",
    "edit",
    "write",
    "task",
    "webfetch",
    "todowrite",
    "skill",
    "suggest",
    "kilo_local_recall"
  ],
  "finish_reason": "tool_calls",
  "mutation": {
    "transition": "append",
    "cause": null
  },
  "tool_calls": [
    {
      "call_index": 0,
      "name": "bash",
      "category": "*File Ops",
      "programs": [
        "Remove-Item",
        "ls"
      ],
      "parse_status": "success",
      "arguments": [
        [
          "command",
          "Remove-Item -Recurse -Force <var> ; ls <var>"
        ],
        [
          "description",
          "<str>"
        ]
      ],
      "outcome": "ok",
      "result_tokens": 66,
      "latency_ms": 19567,
      "subagent": null
    }
  ]
}
```

</details>

<a id="request-14"></a>

### 请求 14

<details>
<summary>展开模型、token、变化标记和工具骨架</summary>

```json
{
  "step": 13,
  "turn_index": 1,
  "step_trigger": "tool",
  "link_reason": "tool_call_id",
  "start_ms": 1779018365669,
  "end_ms": 1779018367486,
  "ttft_ms": 1559,
  "model": "minimax-m2.7",
  "provider": "G",
  "stream": true,
  "provider_tokens": {
    "prompt": 8229,
    "completion": 53,
    "cached": null
  },
  "role_tokens": {
    "system": 3832,
    "user": 157,
    "assistant": 944,
    "tool": 3721,
    "tool_definitions": 10035
  },
  "n_messages": 40,
  "tool_definition_names": [
    "question",
    "bash",
    "read",
    "glob",
    "grep",
    "edit",
    "write",
    "task",
    "webfetch",
    "todowrite",
    "skill",
    "suggest",
    "kilo_local_recall"
  ],
  "finish_reason": "stop",
  "mutation": {
    "transition": "append",
    "cause": null
  },
  "tool_calls": []
}
```

</details>

<a id="request-15"></a>

### 请求 15

<details>
<summary>展开模型、token、变化标记和工具骨架</summary>

```json
{
  "step": 14,
  "turn_index": 2,
  "step_trigger": "user",
  "link_reason": "assistant_message",
  "start_ms": 1779018417503,
  "end_ms": 1779018418797,
  "ttft_ms": 1095,
  "model": "minimax-m2.7",
  "provider": "G",
  "stream": true,
  "provider_tokens": {
    "prompt": 8307,
    "completion": 0,
    "cached": null
  },
  "role_tokens": {
    "system": 3832,
    "user": 170,
    "assistant": 985,
    "tool": 3721,
    "tool_definitions": 10035
  },
  "n_messages": 42,
  "tool_definition_names": [
    "question",
    "bash",
    "read",
    "glob",
    "grep",
    "edit",
    "write",
    "task",
    "webfetch",
    "todowrite",
    "skill",
    "suggest",
    "kilo_local_recall"
  ],
  "finish_reason": "tool_calls",
  "mutation": {
    "transition": "mutation",
    "cause": "injection"
  },
  "tool_calls": [
    {
      "call_index": 0,
      "name": "read",
      "category": "Read",
      "programs": null,
      "parse_status": null,
      "arguments": [
        [
          "filePath",
          "<path>"
        ]
      ],
      "outcome": "ok",
      "result_tokens": 1162,
      "latency_ms": 5251,
      "subagent": null
    }
  ]
}
```

</details>

<a id="request-16"></a>

### 请求 16

<details>
<summary>展开模型、token、变化标记和工具骨架</summary>

```json
{
  "step": 15,
  "turn_index": 2,
  "step_trigger": "tool",
  "link_reason": "tool_call_id",
  "start_ms": 1779018424048,
  "end_ms": 1779018426268,
  "ttft_ms": 1983,
  "model": "minimax-m2.7",
  "provider": "G",
  "stream": true,
  "provider_tokens": {
    "prompt": 9507,
    "completion": 238,
    "cached": null
  },
  "role_tokens": {
    "system": 3832,
    "user": 170,
    "assistant": 1013,
    "tool": 4885,
    "tool_definitions": 10035
  },
  "n_messages": 44,
  "tool_definition_names": [
    "question",
    "bash",
    "read",
    "glob",
    "grep",
    "edit",
    "write",
    "task",
    "webfetch",
    "todowrite",
    "skill",
    "suggest",
    "kilo_local_recall"
  ],
  "finish_reason": "stop",
  "mutation": {
    "transition": "append",
    "cause": null
  },
  "tool_calls": []
}
```

</details>

<a id="request-17"></a>

### 请求 17

<details>
<summary>展开模型、token、变化标记和工具骨架</summary>

```json
{
  "step": 16,
  "turn_index": 3,
  "step_trigger": "user",
  "link_reason": "assistant_message",
  "start_ms": 1779018549875,
  "end_ms": 1779018551853,
  "ttft_ms": 1761,
  "model": "minimax-m2.7",
  "provider": "G",
  "stream": true,
  "provider_tokens": {
    "prompt": 9790,
    "completion": 0,
    "cached": null
  },
  "role_tokens": {
    "system": 3832,
    "user": 197,
    "assistant": 1199,
    "tool": 4885,
    "tool_definitions": 10035
  },
  "n_messages": 46,
  "tool_definition_names": [
    "question",
    "bash",
    "read",
    "glob",
    "grep",
    "edit",
    "write",
    "task",
    "webfetch",
    "todowrite",
    "skill",
    "suggest",
    "kilo_local_recall"
  ],
  "finish_reason": "tool_calls",
  "mutation": {
    "transition": "mutation",
    "cause": "injection"
  },
  "tool_calls": [
    {
      "call_index": 0,
      "name": "glob",
      "category": "Read",
      "programs": null,
      "parse_status": null,
      "arguments": [
        [
          "path",
          "<path>"
        ],
        [
          "pattern",
          "<path>"
        ]
      ],
      "outcome": "ok",
      "result_tokens": 2458,
      "latency_ms": 5016,
      "subagent": null
    }
  ]
}
```

</details>

<a id="request-18"></a>

### 请求 18

<details>
<summary>展开模型、token、变化标记和工具骨架</summary>

```json
{
  "step": 17,
  "turn_index": 3,
  "step_trigger": "tool",
  "link_reason": "tool_call_id",
  "start_ms": 1779018556869,
  "end_ms": 1779018558122,
  "ttft_ms": 1029,
  "model": "minimax-m2.7",
  "provider": "G",
  "stream": true,
  "provider_tokens": {
    "prompt": 12246,
    "completion": 0,
    "cached": null
  },
  "role_tokens": {
    "system": 3832,
    "user": 197,
    "assistant": 1221,
    "tool": 7345,
    "tool_definitions": 10035
  },
  "n_messages": 48,
  "tool_definition_names": [
    "question",
    "bash",
    "read",
    "glob",
    "grep",
    "edit",
    "write",
    "task",
    "webfetch",
    "todowrite",
    "skill",
    "suggest",
    "kilo_local_recall"
  ],
  "finish_reason": "tool_calls",
  "mutation": {
    "transition": "append",
    "cause": null
  },
  "tool_calls": [
    {
      "call_index": 0,
      "name": "read",
      "category": "Read",
      "programs": null,
      "parse_status": null,
      "arguments": [
        [
          "filePath",
          "<path>"
        ]
      ],
      "outcome": "ok",
      "result_tokens": 810,
      "latency_ms": 3852,
      "subagent": null
    }
  ]
}
```

</details>

<a id="request-19"></a>

### 请求 19

<details>
<summary>展开模型、token、变化标记和工具骨架</summary>

```json
{
  "step": 18,
  "turn_index": 3,
  "step_trigger": "tool",
  "link_reason": "tool_call_id",
  "start_ms": 1779018561974,
  "end_ms": 1779018563305,
  "ttft_ms": 1126,
  "model": "minimax-m2.7",
  "provider": "G",
  "stream": true,
  "provider_tokens": {
    "prompt": 13063,
    "completion": 0,
    "cached": null
  },
  "role_tokens": {
    "system": 3832,
    "user": 197,
    "assistant": 1244,
    "tool": 8157,
    "tool_definitions": 10035
  },
  "n_messages": 50,
  "tool_definition_names": [
    "question",
    "bash",
    "read",
    "glob",
    "grep",
    "edit",
    "write",
    "task",
    "webfetch",
    "todowrite",
    "skill",
    "suggest",
    "kilo_local_recall"
  ],
  "finish_reason": "tool_calls",
  "mutation": {
    "transition": "append",
    "cause": null
  },
  "tool_calls": [
    {
      "call_index": 0,
      "name": "read",
      "category": "Read",
      "programs": null,
      "parse_status": null,
      "arguments": [
        [
          "filePath",
          "<path>"
        ]
      ],
      "outcome": "ok",
      "result_tokens": 620,
      "latency_ms": 3343,
      "subagent": null
    }
  ]
}
```

</details>

<a id="request-20"></a>

### 请求 20

<details>
<summary>展开模型、token、变化标记和工具骨架</summary>

```json
{
  "step": 19,
  "turn_index": 3,
  "step_trigger": "tool",
  "link_reason": "tool_call_id",
  "start_ms": 1779018566648,
  "end_ms": 1779018568974,
  "ttft_ms": 2094,
  "model": "minimax-m2.7",
  "provider": "G",
  "stream": true,
  "provider_tokens": {
    "prompt": 13695,
    "completion": 0,
    "cached": null
  },
  "role_tokens": {
    "system": 3832,
    "user": 197,
    "assistant": 1271,
    "tool": 8779,
    "tool_definitions": 10035
  },
  "n_messages": 52,
  "tool_definition_names": [
    "question",
    "bash",
    "read",
    "glob",
    "grep",
    "edit",
    "write",
    "task",
    "webfetch",
    "todowrite",
    "skill",
    "suggest",
    "kilo_local_recall"
  ],
  "finish_reason": "tool_calls",
  "mutation": {
    "transition": "append",
    "cause": null
  },
  "tool_calls": [
    {
      "call_index": 0,
      "name": "glob",
      "category": "Read",
      "programs": null,
      "parse_status": null,
      "arguments": [
        [
          "path",
          "<path>"
        ],
        [
          "pattern",
          "<path>"
        ]
      ],
      "outcome": "ok",
      "result_tokens": 19,
      "latency_ms": 3347,
      "subagent": null
    }
  ]
}
```

</details>

<a id="request-21"></a>

### 请求 21

<details>
<summary>展开模型、token、变化标记和工具骨架</summary>

```json
{
  "step": 20,
  "turn_index": 3,
  "step_trigger": "tool",
  "link_reason": "tool_call_id",
  "start_ms": 1779018572321,
  "end_ms": 1779018573429,
  "ttft_ms": 862,
  "model": "minimax-m2.7",
  "provider": "G",
  "stream": true,
  "provider_tokens": {
    "prompt": 13724,
    "completion": 0,
    "cached": null
  },
  "role_tokens": {
    "system": 3832,
    "user": 197,
    "assistant": 1296,
    "tool": 8800,
    "tool_definitions": 10035
  },
  "n_messages": 54,
  "tool_definition_names": [
    "question",
    "bash",
    "read",
    "glob",
    "grep",
    "edit",
    "write",
    "task",
    "webfetch",
    "todowrite",
    "skill",
    "suggest",
    "kilo_local_recall"
  ],
  "finish_reason": "tool_calls",
  "mutation": {
    "transition": "append",
    "cause": null
  },
  "tool_calls": [
    {
      "call_index": 0,
      "name": "glob",
      "category": "Read",
      "programs": null,
      "parse_status": null,
      "arguments": [
        [
          "path",
          "<path>"
        ],
        [
          "pattern",
          "<path>"
        ]
      ],
      "outcome": "ok",
      "result_tokens": 15,
      "latency_ms": 4303,
      "subagent": null
    }
  ]
}
```

</details>

<a id="request-22"></a>

### 请求 22

<details>
<summary>展开模型、token、变化标记和工具骨架</summary>

```json
{
  "step": 21,
  "turn_index": 3,
  "step_trigger": "tool",
  "link_reason": "tool_call_id",
  "start_ms": 1779018577732,
  "end_ms": 1779018579691,
  "ttft_ms": 1726,
  "model": "minimax-m2.7",
  "provider": "G",
  "stream": true,
  "provider_tokens": {
    "prompt": 13749,
    "completion": 0,
    "cached": null
  },
  "role_tokens": {
    "system": 3832,
    "user": 197,
    "assistant": 1320,
    "tool": 8817,
    "tool_definitions": 10035
  },
  "n_messages": 56,
  "tool_definition_names": [
    "question",
    "bash",
    "read",
    "glob",
    "grep",
    "edit",
    "write",
    "task",
    "webfetch",
    "todowrite",
    "skill",
    "suggest",
    "kilo_local_recall"
  ],
  "finish_reason": "tool_calls",
  "mutation": {
    "transition": "append",
    "cause": null
  },
  "tool_calls": [
    {
      "call_index": 0,
      "name": "grep",
      "category": "Read",
      "programs": null,
      "parse_status": null,
      "arguments": [
        [
          "path",
          "<path>"
        ],
        [
          "pattern",
          "<path>"
        ]
      ],
      "outcome": "ok",
      "result_tokens": 6220,
      "latency_ms": 11943,
      "subagent": null
    }
  ]
}
```

</details>

<a id="request-23"></a>

### 请求 23

<details>
<summary>展开模型、token、变化标记和工具骨架</summary>

```json
{
  "step": 22,
  "turn_index": 3,
  "step_trigger": "tool",
  "link_reason": "tool_call_id",
  "start_ms": 1779018591634,
  "end_ms": 1779018592993,
  "ttft_ms": 1156,
  "model": "minimax-m2.7",
  "provider": "G",
  "stream": true,
  "provider_tokens": {
    "prompt": 19955,
    "completion": 0,
    "cached": null
  },
  "role_tokens": {
    "system": 3832,
    "user": 197,
    "assistant": 1356,
    "tool": 15039,
    "tool_definitions": 10035
  },
  "n_messages": 58,
  "tool_definition_names": [
    "question",
    "bash",
    "read",
    "glob",
    "grep",
    "edit",
    "write",
    "task",
    "webfetch",
    "todowrite",
    "skill",
    "suggest",
    "kilo_local_recall"
  ],
  "finish_reason": "tool_calls",
  "mutation": {
    "transition": "append",
    "cause": null
  },
  "tool_calls": [
    {
      "call_index": 0,
      "name": "read",
      "category": "Read",
      "programs": null,
      "parse_status": null,
      "arguments": [
        [
          "filePath",
          "<path>"
        ]
      ],
      "outcome": "ok",
      "result_tokens": 24,
      "latency_ms": 3850,
      "subagent": null
    }
  ]
}
```

</details>

<a id="request-24"></a>

### 请求 24

<details>
<summary>展开模型、token、变化标记和工具骨架</summary>

```json
{
  "step": 23,
  "turn_index": 3,
  "step_trigger": "tool",
  "link_reason": "tool_call_id",
  "start_ms": 1779018596843,
  "end_ms": 1779018603734,
  "ttft_ms": 6599,
  "model": "minimax-m2.7",
  "provider": "G",
  "stream": true,
  "provider_tokens": {
    "prompt": 19988,
    "completion": 116,
    "cached": null
  },
  "role_tokens": {
    "system": 3832,
    "user": 197,
    "assistant": 1384,
    "tool": 15065,
    "tool_definitions": 10035
  },
  "n_messages": 60,
  "tool_definition_names": [
    "question",
    "bash",
    "read",
    "glob",
    "grep",
    "edit",
    "write",
    "task",
    "webfetch",
    "todowrite",
    "skill",
    "suggest",
    "kilo_local_recall"
  ],
  "finish_reason": "stop",
  "mutation": {
    "transition": "append",
    "cause": null
  },
  "tool_calls": []
}
```

</details>

<a id="request-25"></a>

### 请求 25

<details>
<summary>展开模型、token、变化标记和工具骨架</summary>

```json
{
  "step": 24,
  "turn_index": 4,
  "step_trigger": "user",
  "link_reason": "assistant_message",
  "start_ms": 1779018648873,
  "end_ms": 1779018650587,
  "ttft_ms": 1457,
  "model": "minimax-m2.7",
  "provider": "G",
  "stream": true,
  "provider_tokens": {
    "prompt": 20122,
    "completion": 12,
    "cached": null
  },
  "role_tokens": {
    "system": 3832,
    "user": 204,
    "assistant": 1464,
    "tool": 15065,
    "tool_definitions": 10035
  },
  "n_messages": 62,
  "tool_definition_names": [
    "question",
    "bash",
    "read",
    "glob",
    "grep",
    "edit",
    "write",
    "task",
    "webfetch",
    "todowrite",
    "skill",
    "suggest",
    "kilo_local_recall"
  ],
  "finish_reason": "stop",
  "mutation": {
    "transition": "mutation",
    "cause": "injection"
  },
  "tool_calls": []
}
```

</details>

<a id="request-26"></a>

### 请求 26

<details>
<summary>展开模型、token、变化标记和工具骨架</summary>

```json
{
  "step": 25,
  "turn_index": 5,
  "step_trigger": "user",
  "link_reason": "assistant_message",
  "start_ms": 1779018708429,
  "end_ms": 1779018709791,
  "ttft_ms": 1099,
  "model": "minimax-m2.7",
  "provider": "G",
  "stream": true,
  "provider_tokens": {
    "prompt": 20165,
    "completion": 17,
    "cached": null
  },
  "role_tokens": {
    "system": 3832,
    "user": 218,
    "assistant": 1477,
    "tool": 15065,
    "tool_definitions": 10035
  },
  "n_messages": 64,
  "tool_definition_names": [
    "question",
    "bash",
    "read",
    "glob",
    "grep",
    "edit",
    "write",
    "task",
    "webfetch",
    "todowrite",
    "skill",
    "suggest",
    "kilo_local_recall"
  ],
  "finish_reason": "stop",
  "mutation": {
    "transition": "mutation",
    "cause": "injection"
  },
  "tool_calls": []
}
```

</details>

<a id="request-27"></a>

### 请求 27

<details>
<summary>展开模型、token、变化标记和工具骨架</summary>

```json
{
  "step": 26,
  "turn_index": 6,
  "step_trigger": "user",
  "link_reason": "assistant_message",
  "start_ms": 1779018778341,
  "end_ms": 1779018779792,
  "ttft_ms": 1129,
  "model": "minimax-m2.7",
  "provider": "G",
  "stream": true,
  "provider_tokens": {
    "prompt": 20212,
    "completion": 16,
    "cached": null
  },
  "role_tokens": {
    "system": 3832,
    "user": 231,
    "assistant": 1488,
    "tool": 15065,
    "tool_definitions": 10035
  },
  "n_messages": 66,
  "tool_definition_names": [
    "question",
    "bash",
    "read",
    "glob",
    "grep",
    "edit",
    "write",
    "task",
    "webfetch",
    "todowrite",
    "skill",
    "suggest",
    "kilo_local_recall"
  ],
  "finish_reason": "stop",
  "mutation": {
    "transition": "mutation",
    "cause": "injection"
  },
  "tool_calls": []
}
```

</details>

## 阅读边界

工具 arguments 是匿名化骨架，outcome、result_tokens 和 latency_ms 是观察元数据；没有工具结果正文。latency_ms 按来源定义是至下一模型请求的间隔，不能直接当作精确工具执行耗时。mutation 原样照录，不据其标签推断被删除内容是否已完成用途。

来源：[数据集](https://huggingface.co/datasets/harvardMadsys/freeinference_agentic_trace) · [官方仓库](https://github.com/HarvardMadSys/freeinference_agentic_trace)。固定数据版本与统计口径见分析首页。

来源：FreeInference `2026-05-17`，原始记录 SHA-256 `88e11e41edb579a4760bf824762d6e6e770712c23c2c2df556c1a4f89a51dc64`。
