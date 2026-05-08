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
| `--body-file` | 否 | 将本次请求的 JSON 先写入该路径再以流式 POST，**大体积 `data/`（如单行极限输入）强烈建议指定**，并配合 **Python 3.9+** 执行；脚本内已 `trust_env=False` 以降低错误代理导致的中断 |
| `--ca-cert` | 否 | 自签证书 CA |

**示例**：

```powershell
# 默认覆盖已有数据并上传
python upload_testdata.py --base-url https://codefun2000.com --domain-id system --pid P4718 --data-dir ./testdata

# 大测试数据：先落盘请求体再上传（示例路径可改）
python upload_testdata.py --base-url https://codefun2000.com --domain-id system --pid P4724 --data-dir ./Problems/P4724/data --body-file ./.upload_body_cache.json

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

## 核心代码模式附加文件（`compile.sh` / `config.yaml` / `template.*` / `user.*`）

与仓库 **`leetcode-core-code-mode`** 交付物一致：题目根目录下上述文件名与平台侧「附加评测文件」键名一致。本组脚本用于在本地生成**路径清单 JSON**，并调用平台扩展接口**按文件名上传文本内容**。

### `generate_leetcode_core_manifest.py` — 生成清单

**作用**：扫描题目根目录下约定文件名，写入 **`leetcode_core_bundle_paths.json`**（默认与题目根同级），记录已找到文件的**绝对路径**及 `missing` 列表。

**主要参数**：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--problem-dir` | 是 | 题目根目录 |
| `--out` | 否 | 清单输出路径（默认 `<题目根>/leetcode_core_bundle_paths.json`） |

**示例**：

```powershell
python generate_leetcode_core_manifest.py --problem-dir ./Problems/P14207
```

### `upload_leetcode_core_bundle.py` — 按清单上传

**作用**：读取清单中的 `files`（逻辑文件名 → 本地绝对路径），将**实际可读**的文件以 UTF-8 文本读入，组装为 `files` 字典，调用 **`POST {base}/api/problem/{api-segment}`**。缺失或路径失效的文件**不会**进入请求体；脚本在 stderr/stdout 中提示缺失项（**不**因部分缺失而整体失败退出，除非无可上传内容且你选择将「无文件」视为正常跳过——见脚本说明）。

**主要参数**：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--base-url` / `--domain-id` / `--pid` | 是 | 与其它脚本一致 |
| `--problem-dir` | 是 | 题目根；用于默认 manifest 路径及刷新扫描 |
| `--manifest` | 否 | 清单路径（默认 `<题目根>/leetcode_core_bundle_paths.json`） |
| `--refresh-manifest` | 否 | **默认开启**：上传前重新扫描并写回 manifest |
| `--no-refresh-manifest` | 否 | 仅使用已有 JSON，不覆盖 |
| `--api-segment` | 否 | 默认 `upload_leetcode_core_bundle`，完整 URL 为 `.../api/problem/upload_leetcode_core_bundle`。**若线上部署路径不同，以平台文档为准并用本参数覆盖** |
| `--body-file` | 否 | 与 `upload_testdata.py` 相同，大 JSON 时可先落盘再流式 POST |
| `--ca-cert` | 否 | 自签证书 CA |

**请求体约定**（须与 CodeFun2000 侧实现一致；若有差异请改 `--api-segment` 或联系平台）：

```json
{
  "domainId": "...",
  "uname": "...",
  "password": "...",
  "pid": "P14207",
  "files": {
    "compile.sh": "文件全文",
    "config.yaml": "..."
  }
}
```

**示例**：

```powershell
python upload_leetcode_core_bundle.py --base-url https://codefun2000.com --domain-id system --pid P14207 --problem-dir ./Problems/P14207
```

依赖模块：`leetcode_core_bundle_common.py`（与上两脚本同目录，勿删）。

---

在仓库根目录或 `utils` 目录下执行时，把 `python xxx.py` 换成实际路径（例如 `python .\utils\get_problem.py ...`）。
