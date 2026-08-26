# Agent 改写约定（替代 DeepSeek）

默认 `--source agent`，**不调用 DeepSeek**。Cursor Agent 按 `prompts/` 规则写入产物，脚本只负责拉取、拼接、上传。

## 工作流

1. 拉取原题：`python batch_rewrite.py --mode 2 --source agent`
2. Agent 在 `log/{pid}/` 写入下面 3 个文件
3. （推荐）回填样例答案：`python fill_sample_outputs.py --pid Pxxxx`
4. 拼接并上传：`python batch_rewrite.py --mode 6 --source agent`

已 `overall_success=true` 的题目会自动跳过。

## 必须写入的文件

| 文件 | 内容 |
|------|------|
| `03_LLM生成的新题面.json` | `title`, `content`, `input_description`, `output_description` |
| `03.5_修改后的题解.md` | 从 `## 解题思路` 起的模板题解，含 Python/Java/C++ |
| `04_LLM生成的新样例.json` | `{"samples":[{"input","output","explanation"}, ...]}` 2~4 条 |

规则与 DeepSeek 提示词相同：`prompts/step3_system.txt`、`step35_system.txt`、`step4_system.txt`。

硬性约束：

- 算法核与 I/O 协议、字符集与原题解代码一致
- 换场景、换术语、换标题；不改输入输出结构
- **业务背景要写饱满**（角色、目标、规则来源约 2～5 句），不要只剩数学定义
- **数据范围记法必须对调**：原题 $2\\times 10^5$/$2e5$/$10^9$ → 新题 `200000`/`1000000000`；原题 `100000`/`200000` → 新题 $10^5$/$2 \\times 10^5$。只换记法不改数值
- 题面不要写样例；样例另放 04
- 题面不要写样例；样例另放 04
- **04 一定不能出现原题面样例**：整段输入不得相同；原样例里带字母/`?` 的行、至少 3 个数的数据行也不得复用。只改一条边或只改说明不算新样例
- 原标题若带 `第x题-` 前缀，上传时脚本会自动加回

## 单题命令

```powershell
python rewrite_and_upload.py --pid P5201 --mode 2 --source agent
python fill_sample_outputs.py --pid P5201
python rewrite_and_upload.py --pid P5201 --mode 6 --source agent
```
