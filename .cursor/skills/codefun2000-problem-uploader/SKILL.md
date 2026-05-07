---
name: codefun2000-problem-uploader
description: |
  use this skill when the user wants to upload editorial (题解), test data, and/or submit std for online judge on CodeFun2000 via local utils scripts (upload_sol.py, upload_testdata.py, submit_code_and_get_result.py).
  Locate scripts under workspace `./utils` (never hardcode a parent folder like 华为AI-x月x日). User explicit pid overrides folder-name pid. User may scope to data-only / solution-only / std-submit-only; skip unrelated steps and skip data/ requirement when not uploading data.
  Fail closed: utils dir or required script missing, missing env, missing domain, missing pid when needed, missing data/ only when upload-data is in scope, broken pairs → fixed fatal message; then summarize outputs and warnings.
---

# 上传题目 Skill（CodeFun2000 / Hydro API）

本 Skill 指导通过工作区内解析到的 **`utils/`** 目录下的脚本，将本地题目目录中的**题解**、**测试数据**同步到平台，并对**标程**做**在线提交评测**。

脚本与参数细节以 **`<utils_dir>/README.md`**（若存在）为准；**`--base-url` 固定为 `https://codefun2000.com`**。

---

## 0. 依赖与环境（执行前必查）

建议结合用户表述**先判定第 4 节的任务范围**，再执行 **第 0.2 节**（只检查本轮会用到的脚本）。

### 0.1 定位 `utils` 目录（`<utils_dir>`）

在**执行任何上传/提交命令之前**，必须先解析 `<utils_dir>`。用于与无关目录区分：候选文件夹须名为 `utils`，且其中**至少存在其一**：`upload_testdata.py`、`upload_sol.py`、`submit_code_and_get_result.py`（不必三者齐全；**缺哪些由第 0.2 节按任务再判**）。

1. **优先**：以**当前工作区根目录**为起点，若存在 **`./utils`** 且满足上一段「至少其一」，则 `<utils_dir>` = 该路径。
2. **否则**：自**用户给出的题目根目录**起，向**父目录逐级上溯**（含该目录自身），查找第一个满足上一段的 `utils` 文件夹，作为 `<utils_dir>`。
3. **若仍找不到**：**fatal stop**，缺失项须包含：`工作区内未找到可用的 utils 目录（需为名为 utils 的文件夹，且至少含 upload_testdata.py / upload_sol.py / submit_code_and_get_result.py 之一）`。

解析到后，所有命令中的脚本路径使用 **`<utils_dir>/脚本名.py`**（按实际绝对路径或工作区相对路径写出即可）。

### 0.2 按任务检查脚本是否存在（缺失则 fatal stop）

在确定用户任务范围（见第 4 节「任务范围」）后，**仅对会执行到的步骤**检查对应文件是否存在于 `<utils_dir>`：

| 将执行的步骤 | 必须存在的文件 |
|-------------|----------------|
| 上传测试数据 | `upload_testdata.py` |
| 上传题解 | `upload_sol.py` |
| 在线评测 std | `submit_code_and_get_result.py` |

任一必需脚本缺失：**fatal stop**，缺失项写明：`utils 目录位于 <路径>，但缺少文件：<文件名>`。

### 0.3 其余依赖

严格按照utils/readme.md 中的说明来执行，如果readme.md不存在，则**fatal stop**

执行示例（路径中的 `<utils_dir>` 替换为实际解析结果）：

```powershell
python "<utils_dir>\upload_testdata.py" --base-url https://codefun2000.com ...
```

---

## 1. Fatal Stop 原则（与出题-ACM模式-Skill 对齐）

采用 **fail closed**：前置条件不满足时，**只输出原因并中止**，不继续上传或提交。

### 1.1 何时必须 fatal stop

- **第 0.1 / 0.2 节**：找不到 `<utils_dir>`，或当前任务所需的脚本在 `<utils_dir>` 中不存在。
- 未设置 `HYDRO_API_UNAME` / `HYDRO_API_PASSWORD`。
- 用户未提供可用的 **`--domain-id`**（且无法从任务说明中唯一确定）。
- **无法确定 PID**（见第 2 节）：题目文件夹名中**不含**形如 `P4000` 的 pid，且用户也**未在对话中显式给出** pid（例如「pid 为 P4719」「上传到 P4719」）。
- **仅当任务范围包含「上传测试数据」时**（默认整套上传，或用户明确说**只上传数据**）：用户指定的题目根目录下**不存在名为 `data` 的文件夹**（不是「data 为空」，而是**没有该目录**）。若用户明确只要**只上传题解**或**只测试 std**，**不要求**存在 `data/`。
- 用户给出的题目根路径不存在或不是目录（若任务根本不需要题目根目录，例如用户只给远程路径+显式 pid+单独题解文件——此时以用户给出的有效路径为准；缺路径则 fatal stop）。

### 1.2 fatal stop 输出格式

与 `出题-ACM模式-Skill.md` 一致，只允许列原因并中止：

```text
无法继续执行，缺失以下依赖或前置条件：

- <缺失项或失败项 1>
- <缺失项或失败项 2>

请手动补充或修复后重新发起任务。
```

---

## 2. PID 的确定规则

- **格式**：大小写不敏感匹配 **`P` + 十进制数字**（如 `P4000`、`p4598`）；规范化输出命令参数时使用平台惯例（一般 **`P` 大写 + 数字**）。
- **来源优先级**（**显式优先**）：
  1. 用户在当前任务中**显式给出**的 pid（例如「pid P4719」「题目 P4719」「上传到 P4719」）**一律作为脚本参数 `--pid` 的唯一值**，**不再**从文件夹名解析或覆盖。
  2. 仅当用户**未**显式给出 pid 时，才从**用户给出的题目根文件夹名称**中提取上述模式；若文件夹名中有多个匹配，取**第一个**并在报告中说明「从文件夹名解析到 pid：…」。
- **若仍无 pid**：触发 **第 1 节 fatal stop**，缺失项须明确写：`无法从文件夹名解析 pid（需包含形如 P4000 的片段），且用户未显式提供 pid`。

---

## 3. 使用方式一：整套题目上传（主路径）

用户只给出一个**题目根目录**（文件夹路径），且**未**在第 4 节所述意义上收窄为「只上传题解 / 只上传数据 / 只测试 std」时，走本节**整套**流程。已收窄时按第 4 节执行，本节中未包含的步骤跳过。

### 3.1 目录结构约定（扫描清单）

在**题目根目录**下查找：

| 路径（相对根目录） | 用途 |
|-------------------|------|
| `data/` | 测试数据目录；整套上传时**必须存在**（见第 1.1 节，与任务范围绑定）。 |
| `题解.md` | 若存在则调用 `upload_sol.py` 上传。 |
| `std.py` | 若存在则在线提交评测（`submit_code_and_get_result.py`）。 |
| `std.cpp` | 同上。 |
| `Main.java` | 同上（类名须为 `public class Main`，与出题 Skill 一致）。 |

### 3.2 测试数据规则（与 `upload_testdata.py` 行为一致）

- `upload_testdata.py` 会遍历 `data/` 下**所有**后缀为 `.in` / `.out` 的文件，并要求**每个 stem 同时存在** `stem.in` 与 `stem.out`，否则脚本会以 **「数据不成对」** 报错退出。
- **非** `.in` / `.out` 的文件：脚本**不会上传**，但属于「data 目录下异常/未参与上传的文件」，须在**最终报告第 5.2 节** 中列出并提示用户。
- **执行策略**：
  - 在调用脚本前**先本地扫描** `data/`：列出所有 `.in` / `.out` 的 stem，标出**缺另一半**的 stem；列出所有**非** `.in/.out` 的文件名。
  - 若存在不成对数据：`upload_testdata.py` 会报错退出，**不得**声称数据已全部上传成功。**推荐**：扫描到不成对时先 **fatal stop**（缺失项写明哪些 stem 不成对），避免无效请求；若用户要求先执行脚本以获取平台侧报错，允许调用一次，但**最终汇总（第 5 节）中必须**重复列出本地扫描的不成对明细与脚本输出。
  - 若用户要求「只上传成对部分」：将**仅成对**文件复制到临时目录，`--data-dir` 指向该目录；在 **第 5.2 节** 说明哪些 stem 因不成对被省略、哪些文件未参与上传。

### 3.3 推荐执行顺序（Agent 须真实调用脚本）

在 **第 0～2 节及第 3.2 节扫描结论**允许继续上传时：

1. **`upload_testdata.py`**（路径为 `<utils_dir>/upload_testdata.py`）：`--data-dir` 指向 `<根目录>\data`（或经第 3.2 节处理后的临时目录），带上 `--pid`、`--domain-id`、`--base-url`；按需 `--overwrite` / `--no-overwrite`（默认覆盖见 README）。
2. **`upload_sol.py`**：若存在 **`题解.md`**，则 `--solution-file` 指向该文件；若**不存在**，跳过此步并在报告中注明「未找到 题解.md，未上传题解」。
3. **`submit_code_and_get_result.py`**：对**实际存在**的标程文件分别提交（每种语言一次）：
   - `std.py` → `--lang py.py3`，`--code-file` 指向 `std.py`
   - `std.cpp` → `--lang cc.cc14o2`，`--code-file` 指向 `std.cpp`
   - `Main.java` → `--lang` 使用平台支持的 Java 标识（若 README 未写全，以 CodeFun2000/Hydro 实际为准；常见为带 `java` 的 key，**禁止瞎编**；不确定则 fatal stop 要求用户确认 `--lang`）

每步都应捕获**标准输出/标准错误**与退出码，供第 5.1 节汇总。

---

## 4. 任务范围与用户显式说明（须优先判定）

在检查 **第 1.1 节** 条件前，先根据用户**自然语言**判定本轮 **任务范围**：

| 用户显式说明（示例） | 任务范围 | 须执行的脚本 | 不要求 |
|---------------------|----------|-------------|--------|
| 「只上传数据」「仅传测试数据」等 | 仅上传测试数据 | `upload_testdata.py` | `题解.md`、标程文件、**不要求**执行题解上传与 std 提交 |
| 「只上传题解」「仅传题解」等 | 仅上传题解 | `upload_sol.py` | `data/`、标程提交 |
| 「只测试 std」「只提交标程」「只评测」等 | 仅在线评测 std | `submit_code_and_get_result.py`（可多次，每语言一次） | `data/`、题解上传（除非用户同时要求） |
| 未收窄或「整套上传」等 | 整套（第 3 节） | 三者按第 3.3 节顺序 | 整套的前置条件 |

**规则**：

- 用户**显式给出的 pid**（第 2 节）对所有范围均适用。
- 收窄范围后，**仅检查与执行**该范围对应的 **第 0.2 节**脚本；未涉及的步骤不调用、也不在 fatal 条件中要求对应资源（例如「只上传题解」时不要求 `data/` 存在）。
- **仅测试 std** 时：若用户未指定文件路径，则在**题目根目录**下查找 `std.py` / `std.cpp` / `Main.java` 中存在的文件并分别提交；若用户指定了某一文件，则只提交该文件。**若找不到任何可提交文件**，fatal stop，缺失项写明未找到标程文件。
- **仅上传题解**时：默认 `--solution-file` 为题目根目录下 **`题解.md`**；若用户指定了其他路径，以用户路径为准；文件不存在则 fatal stop。

整套上传（第 3 节）是上述三类的组合与前置扫描超集；**一旦用户收窄范围，不得再按整套默认强制执行被用户排除的步骤**。

---

## 5. 任务结束时的输出要求

### 5.1 脚本结果汇总（必须）

用清晰小节整理每次调用的：

- 命令意图（上传数据 / 上传题解 / 提交何种语言 std）
- **退出码**（若可得）
- **脚本打印的关键信息**（如 HTTP 状态、JSON 摘要、`submit` 的 RID、`是否完全通过`、状态中文、首个失败点等），避免大段无标注 dump；关键字段应摘录。

### 5.2 提示与告警（必须，不替代第 5.1 节）

在汇总末尾单独列出 **「提示与告警」**，凡 applicable 须勾选式说明：

- **标程不完整**：例如仅有 `std.py` 而无 `std.cpp` / `Main.java`——说明「未提交的语言：…」；**不**因此判定整套任务失败（除非用户明确要求三语言齐全）。
- **`data/` 下非 `.in/.out` 文件**：列出文件名，说明未参与上传。
- **输入输出不成对**：列出 stem 或文件名（如 `1.in` 无 `1.out`）；若已通过临时目录仅传成对文件，说明哪些 stem 未上传。
- **`题解.md` 缺失**：在**整套上传**或**仅上传题解**（且未指定其他文件）场景下分别说明：前者为「已跳过题解上传」；后者应已在执行前 fatal stop，不应静默发生。
- **Java 类名**：若存在 `Main.java` 且非 `public class Main`，须提醒用户修正（可与出题 Skill 一致处理）。

---

## 6. 严格禁止

- 伪造 API 返回或声称上传/AC 成功而实际未执行脚本或脚本失败。
- 在无法确定 pid 时猜测题目 id。
- 在未完成 **第 0.1 / 0.2 节** 解析与存在性检查、或 **utils / 所需脚本缺失** 时仍调用上传或提交接口。
- **禁止**跳过环境变量检查；**禁止**在任务范围包含上传数据时跳过 `data/` 存在性检查。
- 对不成对数据静默忽略导致用户误以为全部数据已上传。

---

## 7. 与 `出题-ACM模式-Skill.md` 的关系

- **出题 Skill**：负责创建工作区、题面、标程、题解、造数等。
- **本 Skill**：负责把**已有**目录内容通过 API **推送**到平台并拉取**在线评测结果**。
- 二者可同时被同一仓库引用；本 Skill **不**替代 `algorithm-contest-problemsetter` 的造题逻辑。
