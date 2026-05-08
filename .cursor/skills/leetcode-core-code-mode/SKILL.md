---
name: leetcode-core-code-mode
description: |
  用于在自建 OJ 上交付「LeetCode 核心代码模式」题目包：题面（支持 PID+get_problem.py 从网站拉取）、题解、标程、测试数据，以及 compile.sh、config.yaml、template.{cc,java,py}、user.{cc,java,py}。
  当用户提到「LeetCode 模式」「核心代码模式」「PID 拉题面」「template/user」「样例格式造数」时使用。
  题解：章节骨架须遵循仓库 `题解模板.md`，格式与三语言代码须遵守 `题解生成规范(核心代码模式).md`；出题质量结合 `algorithm-contest-problemsetter`（即使用户 prompt 未逐条复述，仍须执行）。
  造数须对齐 `codefun2000-problem-generator` 第 8 节，且 stdin 形态须与题面样例输入一致；缺依赖时 fail closed。
---

# LeetCode 核心代码模式出题 Skill

本 Skill 在「算法核 + 可评测交付」前提下，把一道题整理成 **与 LeetCode 类似的函数式接口**，并在题目目录下生成 **OJ 后台文件包**（`template.*` 读入并调用 `Solution`，`user.*` 仅为选手可见空壳）。

默认语言交付：**C++ / Java / Python** 三语言；`compile.sh`、`config.yaml`、`template.*`、`user.*` 的**文件名与仓库根目录模板一致**；**`compile.sh` 必须从仓库根原样拷贝，禁止修改**。

---

## 0. 与其它 Skill 的关系

| 依赖 | 用途 |
|------|------|
| `algorithm-contest-problemsetter` | 数据范围、六类测试、hack 思路、边界与验题心智。 |
| `题解模板.md`（与本 Skill 同仓库的 `problem-maker/` 根下） | **题解.md** 的章节骨架（解题思路 → 复杂度 → 代码实现）。 |
| `题解生成规范(核心代码模式).md`（同上） | **题解.md** 的格式细则与第 3 节三语言 LeetCode 式代码（含中文注释要求）。 |
| `codefun2000-problem-generator` 第 **8** 节 | **造数脚本、组数、大小数据分布、换行规则、自校验**；本 Skill **第 7 节**在其基础上增加 **「与题面样例格式一致」** 的强制约束。 |

本 Skill **不负责** 平台上传 API；上传见 `codefun2000-problem-uploader` 与 `utils/README.md`。

---

## 1. 题面来源（显式题面或 PID 抓取）

### 1.1 判定顺序（与 `codefun2000-problem-generator` 对齐）

1. **显式题面**：用户在本轮任务中提供完整或可编辑题面（附件 `题面.md`、长文本等）→ 以用户内容为准写入 `<题目目录>/题面.md`，**不要求** PID。
2. **否则**：用户给出 **PID**（如 `P4000`）→ 必须通过 **`utils/get_problem.py`** 从网站拉取题面。

规则：

- 有显式题面时，不得因「未提供 PID」而 fatal stop。
- 无显式题面且无 PID → fatal stop，缺失项：`未提供题面（无 PID 且无显式题面）`。
- **同时**有 PID 与显式题面：以**显式题面**写入 `题面.md`；若与抓取结果差异大，用一句话提示「已采用对话中的题面」。

### 1.2 题目目录名

- 用户指定在 `Problems/Pxxxx/`（或等价父目录）下出题，且给出 **PID**（如 `P4000`）时：目录名 **`Problems/P4000/`**（`P` + PID 数字部分，大小写以用户/平台为准，须与对话约定一致）。
- 仅显式题面、无 PID：目录名由用户指定，否则用 `P_custom` 或题目标题 slug，**不得**静默覆盖已有非空 `题面.md`。

### 1.3 PID 抓取执行顺序（强制）

当题面来源为 **PID + `get_problem.py`**，且已确认脚本存在、环境变量按 **`utils/README.md`** 配置可用时：

1. **立即**创建 `<题目目录>/`（若已存在则复用，**不得**在无用户授权时覆盖非空 `题面.md`）。
2. **立即**创建占位 `<题目目录>/题面.md`（可为空一行）。
3. 执行 `utils/get_problem.py`（`--base-url`、`--domain-id`、`--pid` 等以 `utils/README.md` 与脚本为准）。
4. 将脚本产出写入 `题面.md`，**覆盖占位**。

**编码（强制）**：抓取到的字节流可能非 UTF-8。须探测/尝试常见编码后，以 **UTF-8（建议无 BOM）** 写入 `题面.md`；策略与 `codefun2000-problem-generator` 第 4.1.1 节一致。

### 1.4 题面就绪校验

`题面.md` 不存在或为空 → fatal stop：`题面.md 未成功生成或内容为空`。

---

## 2. Fatal Stop（fail closed）

在已确定题面/接口/标程策略后，若出现以下任一情况，**只列原因并中止**（输出格式同 `codefun2000-problem-generator` 第 0.2 节）：

- 需要 **PID 抓取**但 **`utils/get_problem.py` 不存在**，或未按 `utils/README.md` 配置导致无法调用。
- 找不到 `algorithm-contest-problemsetter` Skill（路径候选同 `codefun2000-problem-generator` 第 1.4 节）。
- 找不到 **`题解生成规范(核心代码模式).md`** 或 **`题解模板.md`**（与本 Skill 同仓库的 `problem-maker/` 根下路径），且用户要求自动生成题解。
- 无法从题面确定 **唯一的** `Solution` 公开接口；存在歧义且用户未确认。
- 无法得到可运行标程用于造数或对拍。
- `config.yaml` 中 `cases` 与 `data/` 中文件不一致，或 `.in`/`.out` 与标程不一致。
- 用户要求 **`compile.sh` 与仓库根一致**，但工作区 **`problem-maker/compile.sh` 缺失**。
- **第 7 节**造数完成后，任一组 `.in` 的**行结构/分隔习惯**与题面 **样例输入** 明显不一致（见 7.0），且用户未授权偏离。

执行抓取或安装依赖前，**必须先**阅读并遵守 **`utils/README.md`**。

---

## 3. 交付物目录结构（`<题目目录>/`）

### 3.1 题面与题解

- `题面.md`：写清函数语义、参数、返回值、**样例输入/输出**（须与后续 `template.*` / `data` 一致）。
- `题解.md`：
  - **章节顺序**须与 **`题解模板.md`** 一致（解题思路 → 复杂度分析 → 代码实现）。
  - **正文格式与第 3 节三语言代码**须符合 **`题解生成规范(核心代码模式).md`**；其中 Python、Java、C++ 三段须在**各自**核心逻辑与关键分支处有实质**中文注释**（三语言对齐，具体要求以该规范为准）。
  - **出题质量**（区分度、hack、边界、测试设计表述等）须体现 **`algorithm-contest-problemsetter`** 心智。
  - 以上为默认交付义务，**不依赖**用户在 prompt 中是否再次写出「按规范 / 按模板 / 参考 problemsetter」。

### 3.2 标程

- `std.cpp` / `std.py` / `Main.java`（或团队约定名），与选手同一 `Solution` 逻辑；造数基准选择顺序同 `codefun2000-problem-generator` 第 8 节引言。

### 3.3 OJ 后台文件（与仓库根**同名**）

| 文件 | 说明 |
|------|------|
| `compile.sh` | 与仓库根 **`problem-maker/compile.sh` 完全一致**，Agent **禁止**改一字。 |
| `config.yaml` | `user_extra_files`、`cases`、`langs`。 |
| `template.*` | stdin 解析 → 调 `Solution` → stdout；三语言解析**必须一致**。 |
| `user.*` | **仅** `Solution` 空壳（`return 0` / `pass` 等）；**禁止** `main`、读入、无关 `import`/`#include`。 |

### 3.4 数据与生成器

- `data/`、**`gen.py`**（`codefun2000-problem-generator` 第 8.1 节推荐主名）；若另有 `gen_data.py` 作兼容入口，须在 `data/README.md` 写明主脚本名。
- `config.yaml` 里每个 `input`/`output` 须在 `data/` 存在且编号连续。

---

## 4. 工作流（建议顺序）

0. **题面**：按 **第 1 节** 完成 `题面.md`（含网站样例的原文摘录或等价规范化描述）。
1. **算法核与接口**：用 `algorithm-contest-problemsetter` 定核与数据强度；从题面抽取并冻结 **LeetCode 式 API**（含网站/力扣式函数签名时须与之一致）。
2. **题解**：按 **`题解模板.md`** 搭骨架，按 **`题解生成规范(核心代码模式).md`** 写内容与三语言代码，并体现 **`algorithm-contest-problemsetter`** 的测试与区分度意识。
3. **标程**：实现 std，确保可通过样例。
4. **template / user**：`template.*` 的解析规则 **以题面样例输入为金标准**；`user.*` 仅桩代码。
5. **造数**：按 **第 7 节** 编写并运行 **`gen.py`**（或经 `data/README.md` 声明的等价主脚本），生成 `data/` 与 `config.yaml` 对齐。
6. **compile.sh**：从仓库根 **原样复制**。
7. **config.yaml**：`cases` 与 `data/` 一致。
8. **验题**：空 `user.*` 换入标程（或等价）跑全量；多语言 std 存在时比对输出。

---

## 5. 成功完成时的输出

```text
任务完成。

题目目录：<题目目录>/
题面来源：<PID 抓取 | 用户显式题面>

已生成或对齐的主要文件：
- 题面.md、题解.md
- std（列出实际文件）
- data/、gen.py（及 data/README.md 中声明的兼容脚本名，若有）
- compile.sh（已与仓库根校验一致）
- config.yaml、template.cc、template.java、template.py、user.cc、user.java、user.py

验题摘要：（编译/对拍/样例格式抽查说明）
```

---

## 6. 验题人重点核对

- **样例格式**：随机打开若干 `.in`，与题面「样例输入」对照字符级形态（空格、逗号、括号、换行、多行顺序）。
- **样例输出**：`.out` 与题面「样例输出」的**行数、空格、末尾换行**习惯一致（且遵守第 7.5 节换行硬性规则）。
- **题解代码注释**：`题解.md` 第 3 节 **Python / Java / C++** 三段是否在**各自**的**核心逻辑与关键分支**处均有**有实质含义的中文注释**（三语言对齐，见第 3.1 节与 `题解生成规范(核心代码模式).md`）。
- 接口歧义、`compile.sh` Java 步骤、Python 版本与 `langs` 一致。

---

## 7. 生成数据（对齐 `codefun2000-problem-generator` 第 8 节 + LeetCode 专用约束）

生成数据的**组数、分布、hack、换行、自校验**须严格遵守 **`codefun2000-problem-generator` 第 8 节**（8.1–8.6），**不得敷衍**。本节为在该节之上的 **LeetCode 模式补充**，有冲突时以本节 **7.0** 为准。

### 7.0 与题面样例格式一致（强制）

- 从题面（含 **PID 抓取** 的原文）中定位 **样例输入**（及多组样例时的每一组）。**造数主脚本**（见第 7.1 节，如 `gen.py`）生成的 **每一份 `.in`**，其文本形态须与样例所体现的格式 **同类同构**：
  - **单行/多行**、**行顺序**、**分隔符**（空格/逗号/无分隔）、**括号与引号风格**、**等号或键名**（若有）须与官方样例一致；仅允许在**语义合法**前提下替换为不同数值/长度，**禁止**自造与样例展示冲突的另一种 I/O 方言（例如样例为 `nums = [1,2,3]` 风格却改成纯 JSON 一行，除非题面明确两种等价）。
- **`template.cc` / `template.java` / `template.py`** 的解析逻辑必须能 **无歧义解析样例输入**；建议先用「将样例输入原文作为 `1.in`」跑通三语言 template + 标程，再扩展造数脚本。
- 若题面无清晰样例输入，须在对话中标注 **「需要验题确认 stdin 格式」**，不得凭空编造；可 fatal stop 或请用户补充样例截图/原文。

### 7.1–7.4 与 codefun 第 8.1–8.4 对齐

- **7.1**：题目目录下须有**完整可运行**的 Python 生成脚本（须符合 **`codefun2000-problem-generator` 第 8.1 节**：推荐主文件名为 **`gen.py`**；若保留 `gen_data.py` 仅作转调，须在 `data/README.md` 写明主脚本名）。脚本须含：按约束造 `.in`、求标准输出、写文件；覆盖六类测试思想。
- **7.2**：**默认 10 组**数据 `1.in`…`10.in` 及对应 `.out`；若用户或已有 `config.yaml` 明确为其它组数，则 **`config.yaml` 的 `cases` 与造数脚本输出须一致**，并在 `data/README.md` 说明原因。
- **7.3**：前 8 组偏中小、后 2 组偏大；分布均匀。**「大」须在 `题面.md` 已给出的数据范围内压满**（极限定义见 `codefun2000-problem-generator` 第 8 节「极限数据」），不得突破题面未允许的规模。
- **7.4**：显式 hack 设计，并在说明中写清针对哪类错解。

### 7.5–7.6 与 codefun 第 8.5–8.6 对齐

- **7.5**：与 **`codefun2000-problem-generator` 第 8.5 节**一致：`.in` 最后一行数据后**不要**换行符（文件不以 `\n` 结尾）；`.out` 末尾**有且仅有**一个 `\n`。
- **7.6**：生成后对每组用基准 std 重算，与 `.out` 比对；不一致则 fatal stop。

**基准 std 选择顺序**：`std.py` → `std.cpp` → `Main.java`（同 codefun 第 8 节）。

---

> 本 Skill 与 `codefun2000-problem-generator` 共用 **PID + `get_problem.py`** 与 **第 8 节造数纪律**；本 Skill 额外固定 **LeetCode 式 `Solution` + template/user 壳**，并强制 **stdin 与题面样例同形**。
