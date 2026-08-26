## 解题思路

题目要求实现一种新的注意力机制 $TG\text{-}SA$，整体流程可以直接按题意模拟，核心涉及两个算法步骤：

1. 矩阵乘法计算注意力原始分数
2. 按行进行双门控分段映射与 $Top\text{-}k$ 保留

设输入矩阵为 $Q,K,V \in \mathbb{R}^{L \times d}$。

### 核心思路

先计算原始得分矩阵：

$$
S = \frac{QK^T}{\sqrt{d}}
$$

这里每个位置 $S_{ij}$ 表示第 $i$ 个查询向量和第 $j$ 个键向量的相关性。

然后对每一行做双门控折线映射。设当前行为 $S_i$，该行最大值为：

$$
s_{\max} = \max_j S_{ij}
$$

定义两个门限：

$$
t_1 = \alpha s_{\max}, \quad t_2 = \beta s_{\max}
$$

其中 $0 < \alpha < \beta < 1$。

对于每个分数 $S_{ij}$，按分段函数映射为新的分数 $\tilde{S}_{ij}$：

* 若 $S_{ij} < t_1$，则置为 $0$
* 若 $t_1 \le S_{ij} < t_2$，则线性映射到 $[0,1]$
* 若 $S_{ij} \ge t_2$，则保留为 $1$

也就是：

$$
\tilde{S}*{ij} =
\begin{cases}
0, & S*{ij} < t_1 \
\dfrac{S_{ij} - t_1}{t_2 - t_1}, & t_1 \le S_{ij} < t_2 \
1, & S_{ij} \ge t_2
\end{cases}
$$

这样做的目的，是把较小分数直接过滤掉，把中间分数做平滑过渡，把较大分数直接强化，得到更稀疏、更可解释的注意力分布。

接着执行每行的 $Top\text{-}k$ 稀疏化：每一行只保留最大的 $k_{top}$ 个 $\tilde{S}_{ij}$，其余位置置为 $0$。

之后按行归一化：

* 如果某一行全为 $0$，说明这一行没有有效注意力，则该行改成均匀分布
* 否则将该行除以行和，使其总和为 $1$

最终得到注意力矩阵 $A$，再计算输出：

$$
O = AV
$$

### 实现方法

实现时只需按题意分成一个函数：

* 外部函数负责实现 $TG\text{-}SA$
* 主函数负责读取一行 $JSON$，解析输入，调用函数并输出结果

其中：

* 矩阵运算使用 $numpy$
* 输入输出使用 $json$
* 保留 $6$ 位小数使用 `round(x, 6)`

---

## 复杂度分析

设序列长度为 $L$，隐藏维度为 $d$。

### 时间复杂度

1. 计算 $QK^T$ 的时间复杂度为 $O(L^2 d)$
2. 双门控映射需要遍历整个矩阵，时间复杂度为 $O(L^2)$
3. 每行做一次 $Top\text{-}k$，总复杂度为 $O(L^2 \log L)$ 或在本题数据范围下可视为 $O(L^2)$
4. 计算 $AV$ 的时间复杂度为 $O(L^2 d)$

因此总时间复杂度为：

$$
O(L^2 d + L^2 \log L)
$$

在题目给定范围 $2 \le L \le 6,\ 2 \le d \le 4$ 下，复杂度完全可行。

### 空间复杂度

需要存储：

* 原始得分矩阵 $S$
* 注意力矩阵 $A$
* 输出矩阵 $O$

所以空间复杂度为：

$$
O(L^2 + Ld)
$$

---

## 代码实现

### Python3

```python
import sys
import json
import math
import numpy as np


# 实现 TG-SA 注意力机制
def tg_sa(Q, K, V, k_top, alpha=0.2, beta=0.6):
    # 转为 numpy 数组，方便矩阵运算
    Q = np.array(Q, dtype=float)
    K = np.array(K, dtype=float)
    V = np.array(V, dtype=float)

    # 获取序列长度 L 和隐藏维度 d
    L, d = Q.shape

    # 1. 计算初始打分矩阵 S = QK^T / sqrt(d)
    S = np.dot(Q, K.T) / math.sqrt(d)

    # 初始化映射后的分数矩阵
    T = np.zeros((L, L), dtype=float)

    # 2. 对每一行做双门控折线映射
    for i in range(L):
        # 当前行最大值
        s_max = np.max(S[i])

        # 两个门限
        t1 = alpha * s_max
        t2 = beta * s_max

        for j in range(L):
            x = S[i][j]

            # 如果两个门限重合，避免除零
            if abs(t2 - t1) < 1e-12:
                if x < t1:
                    T[i][j] = 0.0
                else:
                    T[i][j] = 1.0
            else:
                # 分段映射
                if x < t1:
                    T[i][j] = 0.0
                elif x < t2:
                    T[i][j] = (x - t1) / (t2 - t1)
                else:
                    T[i][j] = 1.0

    # 3. 每行只保留 Top-k 最大值，其余置 0
    for i in range(L):
        if k_top < L:
            # 取当前行按从大到小排序后的前 k_top 个下标
            idx = np.argsort(-T[i])[:k_top]

            # 构造保留后的新行
            new_row = np.zeros(L, dtype=float)
            for p in idx:
                new_row[p] = T[i][p]
            T[i] = new_row

    # 4. 行归一化，若全 0 则改为均匀分布
    A = np.zeros((L, L), dtype=float)
    for i in range(L):
        row_sum = np.sum(T[i])

        if abs(row_sum) < 1e-12:
            # 全 0 时改为均匀分布
            A[i] = np.ones(L, dtype=float) / L
        else:
            # 否则归一化
            A[i] = T[i] / row_sum

    # 5. 计算输出 O = A V
    O = np.dot(A, V)

    return A, O


def main():
    # 读取整行输入
    s = sys.stdin.readline().strip()

    # 解析 JSON
    data = json.loads(s)

    # 读取输入数据，alpha 和 beta 允许缺省
    Q = data["Q"]
    K = data["K"]
    V = data["V"]
    k_top = data["k_top"]
    alpha = data.get("alpha", 0.2)
    beta = data.get("beta", 0.6)

    # 调用函数计算结果
    A, O = tg_sa(Q, K, V, k_top, alpha, beta)

    # 按题意保留 6 位小数
    A_out = []
    for row in A:
        A_out.append([round(float(x), 6) for x in row])

    O_out = []
    for row in O:
        O_out.append([round(float(x), 6) for x in row])

    # 按要求输出一行 JSON
    ans = {
        "A": A_out,
        "O": O_out
    }
    print(json.dumps(ans, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
```