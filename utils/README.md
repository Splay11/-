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
| `--base-url` / `--domain-id` / `--pid` | 是 | `--base-url` 见上文 |
| `--solution-file` 或 `--solution` | 二选一 | 题解文件路径，或直接传一小段字符串 |
| `--ca-cert` | 否 | 自签证书 CA |

**示例**：

```powershell
python upload_sol.py --base-url https://codefun2000.com --domain-id system --pid P4719 --solution-file solution.md
```

---

## `upload_testdata.py` — 上传测试数据

**作用**：调用 `/api/problem/upload_testdata`，把目录下成对的 `*.in` / `*.out` 打包上传；每个 stem 必须同时有 `.in` 与 `.out`。

**主要参数**：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--base-url` / `--domain-id` / `--pid` | 是 | `--base-url` 见上文 |
| `--data-dir` | 是 | 含 `1.in`、`1.out` 等的目录 |
| `--overwrite` | 否 | 默认开启：覆盖已有测试数据 |
| `--no-overwrite` | 否 | 题目已有 `.in/.out` 时跳过上传 |
| `--ca-cert` | 否 | 自签证书 CA |

**示例**：

```powershell
# 默认覆盖已有数据并上传
python upload_testdata.py --base-url https://codefun2000.com --domain-id system --pid P4718 --data-dir ./testdata

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
| `--lang` | 是 | 语言标识，如 `py.py3`、`cc.cc14o2` |
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

在仓库根目录或 `utils` 目录下执行时，把 `python xxx.py` 换成实际路径（例如 `python .\utils\get_problem.py ...`）。
