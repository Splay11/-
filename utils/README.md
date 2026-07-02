# 华为 AI 出题工具脚本说明

依赖：`pip install requests`。 

检查，如果缺失则需要配置

## 环境变量(必须检查，缺失则帮用户直接配置)

脚本通过 `HYDRO_API_UNAME`、`HYDRO_API_PASSWORD` 读取账号。


```powershell
$env:HYDRO_API_UNAME="luti"
$env:HYDRO_API_PASSWORD="lutilutiluti1014lutilutiluti"
```

注意：如果没有环境变量，则帮用户直接配置！

## `--base-url`（写死项）

**`--base-url` 必须为 `https://codefun2000.com`**（末尾有无 `/` 均可，脚本会规范化）。请勿改成其他地址。


以下按脚本说明用途、参数与示例。

---

## `get_problem.py` — 拉取题面

**作用**：调用 `/api/problem/detail`，把指定题目的 Markdown 题面打印到标准输出。

**主要参数**：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--base-url` | 是 | 固定为 `https://codefun2000.com` |
| `--domain-id` | 是 | 域，如 `system` |
| `--pid` | 是 | 题目 id，如 `P4598` |
| `--ca-cert` | 否 | 自签证书时的 CA 路径 |

**示例**：

```powershell
python get_problem.py --base-url https://codefun2000.com --domain-id system --pid P4598
```

---

## `upload_sol.py` — 上传题解

**作用**：调用 `/api/problem/upload_sol`，上传题解正文（Markdown/HTML 等）。

**主要参数**：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--base-url` / `--domain-id` / `--pid` | 是 | `--base-url` 见上文；`--domain-id` 默认 `system` |
| `--solution-file`、位置参数或 `--solution` | 三选一 | 题解文件路径，或直接传一小段字符串 |
| `--user` / `--password` | 否 | 覆盖环境变量 `HYDRO_API_UNAME` / `HYDRO_API_PASSWORD` |
| `--no-proxy` | 否 | 禁用系统代理（避免错误代理导致请求失败） |
| `--ca-cert` | 否 | 自签证书 CA |

**示例**：

```powershell
python upload_sol.py --base-url https://codefun2000.com --domain-id system --pid P4719 --solution-file solution.md
```

---

## `upload_testdata.py` — 上传测试数据

**作用**：调用 `/api/problem/upload_testdata`，上传指定目录下的**全部文件**（含 `*.in` / `*.out` 测例，以及 `compile.sh`、`config.yaml`、`template.*`、`user.*` 等核心代码模式文件）。推荐将测例与配置文件一并放在 `<题目根>/data/`。

**主要参数**：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--base-url` / `--domain-id` / `--pid` | 是 | `--base-url` 见上文 |
| `--data-dir` 或 `--problem-dir` | 二选一 | `--data-dir`：直接指定含文件的目录；`--problem-dir`：题目根目录，脚本会自动在根目录或 `data/` 子目录中定位配置文件 |
| `--overwrite` | 否 | 默认开启：覆盖已有文件并上传 |
| `--no-overwrite` | 否 | 题目已有同名文件则跳过上传 |
| `--ca-cert` | 否 | 自签证书 CA |

**示例**：

```powershell
# 直接指定 data 目录（测例 + compile.sh 等同目录上传）
python upload_testdata.py --base-url https://codefun2000.com --domain-id system --pid P4718 --data-dir ./Problems/P4718/data

# 指定题目根，自动解析 data/ 子目录
python upload_testdata.py --base-url https://codefun2000.com --domain-id system --pid P14207 --problem-dir ./Problems/P14207

# 不覆盖已有数据
python upload_testdata.py --base-url https://codefun2000.com --domain-id system --pid P4718 --data-dir ./testdata --no-overwrite
```

---

## `submit_code_and_get_result.py` — 提交代码并取结果

**作用**：调用 `/api/problem/submit_proxy`，提交代码并轮询得到中文状态等详细信息（RID、是否 AC、编译/运行信息、首个失败点等）。

**主要参数**：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--base-url` / `--domain-id` / `--pid` | 是 | `--base-url` 见上文 |
| `--lang` | 是 | 语言标识，如 `py.py3`、`cc.cc14o2`、`java`、`js`、`c` |
| `--code-file` | 是 | 本地源码路径 |
| `--pretest` | 否 | 样例/自定义输入预测 |
| `--input-file` | 否 | 与 `--pretest` 配合时的输入文件 |
| `--timeout-ms` / `--poll-interval-ms` | 否 | 默认 60000 / 1000 |
| `--ca-cert` | 否 | 自签证书 CA |

**示例**：

```powershell
python submit_code_and_get_result.py --base-url https://codefun2000.com --domain-id system --pid P4719 --lang py.py3 --code-file ans.py
```

---

## `get_solutions.py` — 批量获取题面与题解

**作用**：调用 `/api/problem/list`（POST），批量获取题目信息，含题面、管理员题解、算法标签等。

**主要参数**：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--base-url` / `--domain-id` | 是 | `--base-url` 见上文 |
| `--pids` | 否 | 指定 PID 列表，如 `P1001 P1002` |
| `--query` | 否 | 查询条件 JSON，如 `{"tag":"all"}` |
| `--latest` | 否 | 配合 `--query`，按编号倒序取最近 N 道 |
| `--output-dir` | 否 | 输出目录，每道题写入 `<pid>_题面.md` 与 `<pid>_题解.md` |
| `--output-json` | 否 | 输出完整 JSON 到文件 |
| `--user` / `--password` | 否 | 覆盖环境变量 |

**示例**：

```powershell
# 获取指定 PID 的题解（控制台摘要）
python get_solutions.py --base-url https://codefun2000.com --domain-id system --pids P4000 P4890

# 获取最近 5 道题，保存到目录
python get_solutions.py --base-url https://codefun2000.com --domain-id system --query "{\"tag\":\"all\"}" --latest 5 --output-dir ./exported_solutions
```

---

## 核心代码模式附加文件（`compile.sh` / `execute.sh` / `config.yaml` / `template.*` / `user.*`）

与仓库 **`leetcode-core-code-mode`** 交付物一致：上述文件放在 **`<题目根>/data/`** 下（与 `.in/.out` 同目录）。`upload_testdata.py` 会读取 `data/` 下**每一个普通文件**并上传，因此 `compile.sh`、`execute.sh`、`config.yaml`、`template.*`、`user.*` 等与测例一并通过 `upload_testdata.py` 上传即可，无需额外脚本。

仓库根目录的 **`compile.sh`** 为 LeetCode 核心代码模式编译脚本模板；**`核心代码模式模板/execute.sh`** 为 JS 语言运行脚本模板（`exec /usr/bin/node /w/foo`）。出题时分别原样复制到 `<题目根>/data/compile.sh` 与 `<题目根>/data/execute.sh` 即可。

---

在仓库根目录或 `utils` 目录下执行时，把 `python xxx.py` 换成实际路径（例如 `python .\utils\get_problem.py ...`）。
