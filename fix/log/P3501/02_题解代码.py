### 解题步骤

1. **读取数据**：输入是一个 Python 格式的二维 `list`（每一行中的最后一列为类别 label），我们可以直接用 `eval(input())` 将字符串转成 `list` 对象。
2. **提取标签**：遍历二维列表的最后一列，统计每个类别出现次数。
3. **计算比例**：用每个类别的样本数除以总样本数，得到 $p_k = \frac{|C_k|}{|D|}$。
4. **代入公式**：按公式用 `math.log(p_k, 2)` 求对数并累计求和。
5. **保留小数**：按照题目要求保留三位小数。


## Python 

```python
import math

# 读取输入数据（字符串转二维列表）
data = eval(input().strip())

# 获取数据集总样本数
total = len(data)

# 统计各类别样本个数
label_count = {}
for sample in data:
    label = sample[-1]  # 最后一列是类别
    label_count[label] = label_count.get(label, 0) + 1

# 计算信息熵
entropy = 0.0
for count in label_count.values():
    p = count / total  # 该类别比例
    if p > 0:  # 避免 log(0)
        entropy -= p * math.log(p, 2)  # 累加公式

# 输出信息熵，保留三位小数
print(f"{entropy:.3f}")
```