---
name: huawei-ai-choice-mock
description: >-
  从华为 AI 岗机考选择题真题库 object.json 按 tag1/tag2 频次比例随机抽题，生成一场模拟卷（15 单选 + 5 多选）。
  当用户提到华为选择题模拟题、AI 岗选择题出题、按日期出一套选择题、模拟赛选择题时使用。
---

# 华为 AI 岗选择题模拟卷

从 `华为模拟赛出题/选择题出题/object.json` **原样抽取真题**（不改写题干/选项），按当天日期落盘一场 20 题模拟卷。

完整流程与脚本在出题目录：先读并执行 `华为模拟赛出题/选择题出题/SKILL.md`。

```powershell
python "华为模拟赛出题/选择题出题/scripts/make_mock.py"
```
