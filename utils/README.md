# 华为 AI 出题工具脚本说明

依赖：`pip install requests`。 

检查，如果缺失则需要配置

## 环境变量（项目根 `.env`）

题目类 `/api/problem*` **只认站点秘钥** `CF_API_KEY`（请求头 `X-Api-Key`）。账号密码不能再当接口鉴权。

`submit_proxy` 额外需要 `HYDRO_API_UNAME` / `HYDRO_API_PASSWORD`，那是 Hydro 交题身份。

在仓库根目录建 `.env`（已 gitignore，不要提交）：

```
CF_API_KEY=（控制面板 /manage/external-api）
HYDRO_API_UNAME=luti
HYDRO_API_PASSWORD=...
```

脚本会自动读取该文件。也可先 `$env:CF_API_KEY="..."` 再跑。

## `--base-url`（写死项）

**`--base-url` 必须为 `https://codefun2000.com`**（末尾有无 `/` 均可，脚本会规范化）。请勿改成其他地址。


以下按脚本说明用途、参数与示例。

---

## `get_problem.py` — 拉取题面

**作用**：调用 `/api/problem/detail`，把指定题目的 Markdown 题面以 UTF-8 写入 `--output` 文件。

**主要参数**：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--base-url` | 是 | 固定为 `https://codefun2000.com` |
| `--domain-id` | 是 | 域，如 `system` |
| `--pid` | 是 | 题目 id，如 `P4598` |
| `--output` | 是 | 输出 Markdown 路径，如 `./Problems/P4598/题面.md` |
| `--ca-cert` | 否 | 自签证书时的 CA 路径 |

**示例**：

```powershell
python get_problem.py --base-url https://codefun2000.com --domain-id system --pid P4598 --output ./Problems/P4598/题面.md
```

> 与 `problem-statement-restyle-flavor` 联用时：缺本地题面会自动按上式拉取到 `Problems/P{pid}/题面.md` 再改写。
---

## `upload_sol.py` — 上传题解

**作用**：调用 `/api/problem/upload_sol`，上传题解正文（Markdown/HTML 等）。

**主要参数**：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--base-url` / `--domain-id` / `--pid` | 是 | `--base-url` 见上文；`--domain-id` 默认 `system` |
| `--solution-file`、位置参数或 `--solution` | 三选一 | 题解文件路径，或直接传一小段字符串 |
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

**示例**：

```powershell
# 获取指定 PID 的题解（控制台摘要）
python get_solutions.py --base-url https://codefun2000.com --domain-id system --pids P4000 P4890

# 获取最近 5 道题，保存到目录
python get_solutions.py --base-url https://codefun2000.com --domain-id system --query "{\"tag\":\"all\"}" --latest 5 --output-dir ./exported_solutions
```

---

## `get_problem_markdown.py` — 拉取题面到控制台

与 `get_problem.py` 相同接口（`GET /api/problem/detail`），把 Markdown 打印到 stdout，不写文件。

```powershell
python get_problem_markdown.py --base-url https://codefun2000.com --domain-id system --pid P4598
```

---

## `get_pset_detail.py` — 题单摘要

**作用**：`GET /api/problems/detail`，题单简介、画像、各章题目难度/算法标签。

```powershell
python get_pset_detail.py --base-url https://codefun2000.com --domain-id system --psid 65xxxxxxxxxxxxxxxxxxxxxx
```

---

## `update_pset.py` — 修改题库

**作用**：`POST /api/problems/update`，只更新传入字段。`psid` 可以是 ObjectId 或题库简称。改 `dag` 时会带上 `--domain-id`（默认 `system`）。

```powershell
python update_pset.py --base-url https://codefun2000.com --psid 65xxxxxxxxxxxxxxxxxxxxxx --name "算法基础题库" --introduction "从入门到进阶" --price 99

python update_pset.py --base-url https://codefun2000.com --psid algo-basic --dag-file .\dag.json
```

---

## `get_chinese_list.py` — 题单全部中文题面

**作用**：`GET /api/problems/chinese_list`。`--output-dir` 时每题写 `<pid>.md`；否则打印 JSON。

```powershell
python get_chinese_list.py --base-url https://codefun2000.com --domain-id system --psid 65xxxxxxxxxxxxxxxxxxxxxx --output-dir ./articles
```

---

## `get_admin_solution.py` — 单题管理员题解

**作用**：`GET /api/problem/admin_solution`。`--output` 写入第一条题解 Markdown。

```powershell
python get_admin_solution.py --base-url https://codefun2000.com --domain-id system --pid P1001 --output ./P1001/题解.md
```

---

## `upload_zh_content.py` — 上传中文题面

**作用**：`POST /api/problem/upload_zh_content`。

```powershell
python upload_zh_content.py --base-url https://codefun2000.com --domain-id system --pid P1001 --content-file ./P1001/题面.md
```

---

## `get_testdata.py` — 下载测试数据

**作用**：`GET /api/problem/get_testdata`。`--output-dir` 按文件名写入（UTF-8 文本）。

```powershell
python get_testdata.py --base-url https://codefun2000.com --domain-id system --pid P1001 --output-dir ./P1001/data
```

---

## `create_problem.py` — 新建题目

**作用**：`POST /api/problem/create`。

```powershell
python create_problem.py --base-url https://codefun2000.com --domain-id system --pid P1001 --title "A + B" --content-file ./P1001/题面.md
```

---

## `update_problem.py` — 修改题目

**作用**：`POST /api/problem/update`，只更新传入字段。

```powershell
python update_problem.py --base-url https://codefun2000.com --domain-id system --pid P1001 --title "A + B（修订）" --difficulty 1
```

---

## `generate_ai_alg_tag.py` — 生成 AI 算法标签

**作用**：`POST /api/problem/generate_ai_alg_tag`。`--cover` 覆盖已有标签。

```powershell
python generate_ai_alg_tag.py --base-url https://codefun2000.com --domain-id system --pid P1001
```

---

## `upload_problem.py` — 一键上传题面 + 题解

题面走 `upload_zh_content`，题解走 `upload_sol`。默认在当前目录查找 `{pid}/题面.md` 与 `{pid}/题解.md`。

```powershell
python upload_problem.py --base-url https://codefun2000.com --domain-id system --pid P1001
```

---

## `problem_zip.py` — 题目压缩包导入导出

**作用**：`/api/problem-zip/*`。指定 `--domain-id` 时走 `/d/<domainId>/api/problem-zip/...`。

```powershell
# 导出单题
python problem_zip.py export-problem --pid P1001 --output P1001.zip

# 题库后台打包并等待下载
python problem_zip.py export-pset-local --psid 65xxxxxxxxxxxxxxxxxxxxxx --wait --download --output pset.zip

# 导入单题 zip
python problem_zip.py import --file P1001.zip --pid P1001 --overwrite

# 任务查询 / 重试 / 删除
python problem_zip.py export-jobs
python problem_zip.py export-job --job-id <id>
python problem_zip.py export-file --job-id <id> --output out.zip
python problem_zip.py export-retry --job-id <id>
python problem_zip.py export-delete --job-id <id>
python problem_zip.py import-jobs
python problem_zip.py import-job --job-id <id>
python problem_zip.py import-retry --job-id <id>
python problem_zip.py import-delete --job-id <id>
```

大题库不要用 `export-pset` 长时间占连接，改用 `export-pset-local`。

---

## 接口与脚本对照（`API.md`）

| 接口 | 脚本 |
|------|------|
| `GET /api/problem/detail` | `get_problem.py` / `get_problem_markdown.py` |
| `GET /api/problems/detail` | `get_pset_detail.py` |
| `POST /api/problems/update` | `update_pset.py` |
| `GET /api/problems/chinese_list` | `get_chinese_list.py` |
| `GET /api/problem/admin_solution` | `get_admin_solution.py` |
| `POST /api/problem/list` | `get_solutions.py` |
| `POST /api/problem/submit_proxy` | `submit_code_and_get_result.py` |
| `POST /api/problem/upload_sol` | `upload_sol.py` |
| `POST /api/problem/upload_testdata` | `upload_testdata.py` |
| `POST /api/problem/upload_zh_content` | `upload_zh_content.py` |
| `GET /api/problem/get_testdata` | `get_testdata.py` |
| `POST /api/problem/create` | `create_problem.py` |
| `POST /api/problem/update` | `update_problem.py` |
| `POST /api/problem/generate_ai_alg_tag` | `generate_ai_alg_tag.py` |
| `/api/problem-zip/*` | `problem_zip.py` |

共享鉴权：`codefun_auth.py`（读项目根 `.env` 的 `CF_API_KEY`）。

---

## 核心代码模式附加文件（`compile.sh` / `execute.sh` / `config.yaml` / `template.*` / `user.*`）

与仓库 **`leetcode-core-code-mode`** 交付物一致：上述文件放在 **`<题目根>/data/`** 下（与 `.in/.out` 同目录）。`upload_testdata.py` 会读取 `data/` 下**每一个普通文件**并上传，因此 `compile.sh`、`execute.sh`、`config.yaml`、`template.*`、`user.*` 等与测例一并通过 `upload_testdata.py` 上传即可，无需额外脚本。

仓库根目录的 **`compile.sh`** 为 LeetCode 核心代码模式编译脚本模板；**`核心代码模式模板/execute.sh`** 为 JS 语言运行脚本模板（`exec /usr/bin/node /w/foo`）。出题时分别原样复制到 `<题目根>/data/compile.sh` 与 `<题目根>/data/execute.sh` 即可。

---

在仓库根目录或 `utils` 目录下执行时，把 `python xxx.py` 换成实际路径（例如 `python .\utils\get_problem.py ...`）。
