## 解题思路

* 将每个用户在各新闻类别上的阅读次数转为概率分布 $p_i = \frac{count_i}{\sum count}$。
* 按信息熵公式计算：

  $$
  H = -\sum_{i=1}^{n} p_i \log_2 p_i
  $$

  当 $p_i=0$ 时，该项视为 0（避免对数无定义）。
* 对每个用户分别计算并四舍五入到小数点后三位。
* 输入为一个字典（JSON），键是用户 id，值是“类别→次数”的字典；输出为同样键集合的字典，但值为形如 `{"entropy": <值>}` 的字典。

## 复杂度分析

* 设用户数为 $U$，每个用户的类别数为 $C$。
* 时间复杂度：遍历一次所有计数，$O(U \times C)$。
* 空间复杂度：仅保存输出字典，$O(U)$。

## 代码实现

### Python

```python
# -*- coding: utf-8 -*-
"""
ACM 风格：从标准输入读取 JSON，计算每个用户的信息熵并输出 JSON。
"""

import sys
import json
import math

def user_entropy(category_counts):
    """
    计算单个用户的信息熵（以 2 为底），保留三位小数
    :param category_counts: dict，键为类别，值为阅读次数（非负整数）
    :return: float，四舍五入到 3 位小数
    """
    # 总次数
    total = sum(category_counts.values())
    if total == 0:
        return 0.0  # 没有阅读记录时信息熵为 0

    # 累加 -p*log2(p)
    h = 0.0
    for c in category_counts.values():
        if c == 0:
            continue  # p=0 时该项记为 0
        p = c / total
        h -= p * math.log2(p)

    # 四舍五入到 3 位小数
    return round(h, 3)

def main():
    # 读取全部标准输入并解析为 JSON 字典
    raw = sys.stdin.read().strip()
    if not raw:
        print("{}")
        return
    data = json.loads(raw)

    # 对每个用户计算信息熵
    result = {}
    for uid, counts in data.items():
        result[uid] = {"entropy": user_entropy(counts)}

    # 以 JSON 形式输出，保持中文不转义（以防类别为中文）
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
```