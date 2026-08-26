## 思路

感知机使用分类函数：

$ \operatorname{sign}(w \cdot x + b) $

对于样本 $(x_i, y_i)$，若分类错误，则有：

$ y_i(w \cdot x_i + b) \le 0 $

题目给出的损失函数为：

$ Loss(w,b) = - \sum y_i(w \cdot x_i + b) $

其中求和只对当前被误分类的样本进行。

对 $w,b$ 求梯度：

$ \frac{\partial Loss}{\partial w} = - \sum y_i x_i $

$ \frac{\partial Loss}{\partial b} = - \sum y_i $

按梯度下降更新：

$ w \leftarrow w - \eta \frac{\partial Loss}{\partial w}
= w + \eta \sum y_i x_i $

$ b \leftarrow b - \eta \frac{\partial Loss}{\partial b}
= b + \eta \sum y_i $

因此，每一轮遍历所有样本，只累计误分类样本对参数的贡献，最后统一更新一次即可。


## 算法步骤

1. 初始化 $w_1=w_2=b=0$；
2. 重复指定轮数：

   * 遍历全部样本；
   * 若 $y_i(w \cdot x_i+b)\le 0$，说明该样本被误分类；
   * 累加 $\sum y_i x_i$ 与 $\sum y_i$；
   * 一轮结束后更新 $w,b$；
3. 输出保留至多三位小数的 $w_1,w_2,b$。

## 代码实现

### Python

```python
import sys
import numpy as np

data = eval(sys.stdin.readline().strip())
epoch, lr = eval(sys.stdin.readline().strip())

X = np.array([item[0] for item in data], dtype=float)
y = np.array([item[1] for item in data], dtype=float)

w = np.zeros(2, dtype=float)
b = 0.0

for _ in range(epoch):
    scores = X @ w + b
    wrong = y * scores <= 0

    if np.any(wrong):
        w += lr * (y[wrong] @ X[wrong])
        b += lr * y[wrong].sum()

print([round(w[0], 3), round(w[1], 3), round(b, 3)])
```