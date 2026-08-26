# OJ 题目重写与上传自动化脚本

默认 **不再调用 DeepSeek**。Cursor Agent 按 `prompts/` 改写题面/题解/样例并写入 `log/{pid}/`，脚本负责拉取、拼接、上传。约定见 `AGENT_REWRITE.md`。

仍可用 `--source deepseek` 走旧 LLM 流程（需要 `DEEPSEEK_API_KEY`）。

---

## 前置环境变量

脚本依赖以下环境变量，启动时会自动检查，缺失则报错退出：

| 环境变量 | 用途 | 何时需要 |
|---|---|---|
| `HYDRO_API_UNAME` | OJ 平台 API 用户名 | 始终 |
| `HYDRO_API_PASSWORD` | OJ 平台 API 密码 | 始终 |
| `DEEPSEEK_API_KEY` | DeepSeek LLM API 密钥 | 仅 `--source deepseek` |

### PowerShell 设置方式

```powershell
$env:HYDRO_API_UNAME = "your-username"
$env:HYDRO_API_PASSWORD = "your-password"
# 仅 deepseek 源需要：
$env:DEEPSEEK_API_KEY = "sk-your-deepseek-api-key"
```

---

## 文件结构

```
d:\project\Git\fix\
├── rewrite_and_upload.py    # 主脚本（单题处理）
├── batch_rewrite.py          # 批量脚本（多进程并发）
├── prompts/                  # LLM 提示词文件
│   ├── step3_system.txt      # Step 3（生成题面）系统提示词
│   ├── step3_user.txt        # Step 3 用户提示词模板
│   ├── step35_system.txt     # Step 3.5（题解检查）系统提示词
│   ├── step35_user.txt       # Step 3.5 用户提示词模板
│   ├── step4_system.txt      # Step 4（生成样例）系统提示词
│   └── step4_user.txt        # Step 4 用户提示词模板
├── all.txt                   # 批量处理的 PID 列表（每行一个）
├── 题目格式需求.txt           # 题面输出格式模板
└── 需求梳理.txt              # 完整需求文档
```

---

## 使用方法

### 1. 单题处理：`rewrite_and_upload.py`

```powershell
# 完整流程（默认模式 0）
python rewrite_and_upload.py --pid P1001

# 强制覆盖模式（忽略已有日志，重新运行）
python rewrite_and_upload.py --pid P1001 --force

# 交互暂停模式（每步完成后暂停等待确认）
python rewrite_and_upload.py --pid P1001 --mode 1

# 仅获取数据（获取原始题面 + 题解，保存到 log 目录）
python rewrite_and_upload.py --pid P1001 --mode 2

# 仅生成数据（获取 + LLM 生成，不上传）
python rewrite_and_upload.py --pid P1001 --mode 3

# 仅上传数据（从 log/{pid}/ 读取已有数据，执行上传）
python rewrite_and_upload.py --pid P1001 --mode 4
```

#### 参数说明

| 参数 | 必填 | 说明 |
|---|---|---|
| `--pid` | 是 | 题目 ID，如 `P1001` |
| `--mode` | 否 | 调试模式，0~4，默认 0 |
| `--force` | 否 | 强制覆盖：先删除 `log/{pid}/` 再运行 |

#### 模式详解

| 模式 | 执行步骤 | 用途 |
|---|---|---|
| `0` | Step 1~8（全流程） | 默认，完整重写并上传 |
| `1` | Step 1~8，每步暂停 | 调试/人工审核 |
| `2` | Step 1~2 | 仅拉取原始数据 |
| `3` | Step 1~5 | 拉取 + LLM 生成，不上传 |
| `4` | Step 6~8 | 仅从 log 目录读取并上传 |

---

### 2. 批量处理：`batch_rewrite.py`

```powershell
# Agent 工作流（默认，不调用 DeepSeek）
python batch_rewrite.py --mode 2 --source agent    # 只拉取原题
# 然后由 Cursor Agent 写入 03 / 03.5 / 04
python batch_rewrite.py --mode 6 --source agent    # 拼接并上传

# 旧 DeepSeek 全流程
python batch_rewrite.py --mode 0 --source deepseek -w 4

# 指定并发数
python batch_rewrite.py -w 8 --mode 2
```

**前置条件**：`all.txt` 文件必须存在，每行一个 PID（如 `P1001`、`P1002`...）。

**特性**：
- 多进程并发执行，每个 PID 对应一个独立子进程
- 支持 Ctrl+C 安全中断（第二次 Ctrl+C 强制退出）
- 子进程启动时带有随机延迟（0~3 秒），避免同时冲击 API
- 单题超时限制：15 分钟
- 运行状态实时写入进度文件

#### 参数说明

| 参数 | 默认值 | 说明 |
|---|---|---|
| `-w` / `--workers` | 4 | 并发进程数 |
| `--mode` | 2 | 传给单题脚本的模式；Agent 流程先 2 再 6 |
| `--source` | agent | `agent` 不调 DeepSeek；`deepseek` 为旧 LLM 流程 |
| `--force` | 否 | 强制重跑已成功题目 |

---

## 生成的文件

### 日志目录：`log/{pid}/`

每个处理过的题目在 `log/` 下生成独立子目录：

| 文件 | 来源 | 说明 |
|---|---|---|
| `01_原始题面.md` | Step 1 | 从 API 获取的原始 Markdown 题面 |
| `01_原始标题.txt` | Step 1 | 从 API 获取的原始标题 |
| `02_题解代码.py` | Step 2 | 从题解中提取的有效代码块 |
| `02_原始完整题解.md` | Step 2 | 原始完整题解 Markdown |
| `03_LLM生成的新题面_原始响应.txt` | Step 3 | LLM 返回的原始文本 |
| `03_LLM生成的新题面.json` | Step 3 | 解析后的题面 JSON（title/content/input_desc/output_desc） |
| `03.5_LLM题解检查_原始响应.txt` | Step 3.5 | LLM 检查题解冲突的原始响应 |
| `03.5_题解检查结果.json` | Step 3.5 | 解析后的检查结果 |
| `03.5_修改后的题解.md` | Step 3.5 | 修改后的题解（仅当需要修改时存在） |
| `04_LLM生成的新样例_原始响应.txt` | Step 4 | LLM 返回的样例原始文本 |
| `04_LLM生成的新样例.json` | Step 4 | 解析后的样例 JSON（含 samples 数组） |
| `05_拼接后的完整题面.md` | Step 5 | 脚本拼接后的最终题面（即上传内容） |
| `06_上传原始题面结果.json` | Step 6 | 上传原始题面的 API 响应 |
| `07_上传新题面结果.json` | Step 7 | 上传新题面的 API 响应 |
| `08a_上传原始题解结果.json` | Step 8a | 上传原始题解的 API 响应（条件生成） |
| `08b_上传题解结果.json` | Step 8b | 上传修改后题解的 API 响应（条件生成） |
| `运行汇总.json` | 脚本末尾 | 整体执行汇总（成功/失败、各步骤状态、时间等） |
| `执行日志.txt` | 全程 | 带时间戳的完整执行日志 |
| `llm_conversations/` | LLM 调用 | LLM 对话记录子目录（step3/step35/step4 各次尝试） |

### 备份目录：`backup/{pid}/`

首次获取原始数据后自动备份，避免重复 API 调用：

| 文件 | 说明 |
|---|---|
| `01_原始题面.md` | 原始题面备份 |
| `01_原始标题.txt` | 原始标题备份 |
| `02_原始完整题解.md` | 原始题解备份 |

> 备份目录仅创建一次，已存在时跳过。后续运行会优先从备份加载，避免重复 API 调用。

### 批量进度文件：`log/batch_progress.json`

批量脚本运行时实时更新的进度文件，JSON 格式：

```json
{
  "start_time": "2026-08-09 10:30:00",
  "last_update": "2026-08-09 10:35:22",
  "running": ["P1003", "P1004"],
  "total": 50,
  "interrupted": false,
  "results": {
    "P1001": {"status": "success", "time": "2026-08-09 10:31:05", "error": null},
    "P1002": {"status": "fail", "time": "2026-08-09 10:32:10", "error": "返回码 13"},
    "P1003": {"status": "running", "time": "2026-08-09 10:34:00", "error": null}
  }
}
```

### 批量汇总文件：`log/batch_summary.txt`

批量运行结束后生成的汇总文本：

```
批量执行汇总
============================================================
并发数: 4
开始时间: 2026-08-09 10:30:00
更新时间: 2026-08-09 11:00:00
总数: 50
成功: 45
失败: 3
中断: 2
未处理: 0

成功列表: P1001, P1003, P1005, ...
失败列表: P1002, P1008, P1020
中断列表: P1004, P1015
未处理列表: 无
```

---

## 结果汇总格式

### 单题：`log/{pid}/运行汇总.json`

```json
{
  "pid": "P1001",
  "mode": 0,
  "force": false,
  "start_time": "2026-08-09 10:30:00",
  "end_time": "2026-08-09 10:31:05",
  "new_title": "统计生日礼物",
  "steps": {
    "step1_fetch_problem": true,
    "step2_fetch_solution": true,
    "step3_generate_statement": true,
    "step35_check_solution": true,
    "step35_modified": false,
    "step4_generate_samples": true,
    "step5_assemble": true,
    "step6_upload_original_statement": true,
    "step7_upload_new_problem": true,
    "step8_upload_solution": false
  },
  "overall_success": true
}
```

### 退出码

| 退出码 | 含义 |
|---|---|
| `0` | 成功 / 已处理过（跳过） |
| `11` | Step 1 获取题面失败 |
| `12` | Step 2 获取题解失败 |
| `13` | Step 3 LLM 生成题面失败 |
| `14` | Step 3.5 题解检查失败 |
| `15` | Step 4 LLM 生成样例失败 |
| `16` | Step 5 拼接题面失败 |
| `17` | Step 6 上传原始题面失败 |
| `18` | Step 7 上传新题面失败 |
| `19` | Step 8 上传题解失败 |
| `20` | 环境变量缺失 |
| `21` | 模式 4 缺少必要文件 |
| `99` | 未捕获的异常 |

---

## 执行流程概览

```
Step 1  ──  获取原始题面 + 标题（GET /api/problem/detail, POST /api/problem/list）
Step 2  ──  获取题解代码（GET /api/problem/admin_solution），提取第一个有效代码块
Step 3  ──  LLM 生成新题面（标题 + 内容 + 输入/输出描述，不含样例）
Step 3.5 ── LLM 检查题解是否需要适配新题面，如需修改则生成新题解
Step 4  ──  LLM 生成新样例（2~4 条，含解释说明，以原始第一条样例为格式参考）
Step 5  ──  脚本拼接完整题面（按模板格式组装）
Step 6  ──  上传原始题面为附加文件（POST /api/problem/upload_testdata）
Step 7  ──  上传新题面和新标题（POST /api/problem/update）
Step 8  ──  上传题解（仅在 Step 3.5 判断需要修改时执行）
          ├─ 8a：上传原始题解为附加文件
          └─ 8b：上传修改后的题解（POST /api/problem/upload_sol）
```

---

## 注意事项

1. 上传时只改 `title` 和 `content`，不修改 `hidden`/`difficulty`/`tag` 等属性
2. 标题作为 API 参数单独传递，不包含在 content 中
3. 题面 content 以 `# 题目内容` 开头
4. LLM 调用最多重试 3 次，每次间隔 2 秒
5. 如果日志目录已存在且 `运行汇总.json` 中 `overall_success=true`，默认跳过该题目
6. 如需重新处理，使用 `--force` 参数覆盖
7. 原始数据首次获取后会自动备份到 `backup/{pid}/`，后续优先从备份加载
8. 仅在 LLM 判断题解与新题面有冲突时才修改并上传题解
