## 解题思路

题目要求我们按照给定公式，使用$NGD$，也就是归一化梯度下降，来优化目标函数：

$$
f(\mathbf{w})=\frac{1}{2}|X\mathbf{w}-\mathbf{y}|_2^2+\lambda|\mathbf{w}|_2^2
$$

对应梯度为：

$$
\nabla f=X^T(X\mathbf{w}-\mathbf{y})+2\lambda \mathbf{w}
$$

### 核心思路

这道题本质上是一个按题意模拟迭代的过程，核心算法就是$NGD$。

普通梯度下降直接用梯度更新，而这里要先把梯度归一化：

$$
\hat{\mathbf{g}}=\frac{\nabla f}{\max(|\nabla f|_2,\varepsilon)}
$$

然后按衰减学习率更新：

$$
\eta_t=\frac{\eta_0}{\sqrt{t}}
$$

$$
\mathbf{w}_{t+1}=\mathbf{w}_t-\eta_t\hat{\mathbf{g}}
$$

其中要注意几个细节：

1. 权重初始为全$0$向量。
2. 一共迭代固定的$60$步。
3. 如果梯度中出现$NaN$或$Inf$，或者梯度范数小于$\varepsilon$，则跳过本轮更新，但这一步仍然算一次迭代。
4. 训练结束后，用测试集做线性输出：

$$
\hat{\mathbf{y}}=X_{test}\mathbf{w}
$$

再按符号函数转成分类结果，若结果$\ge 0$则输出$1$，否则输出$0$。

### 实现方法

实现时直接使用$numpy$进行矩阵运算即可：

* 用数组保存训练集和测试集；
* 写一个外部函数专门完成训练；
* 主函数中负责读入单行$JSON$、调用函数、组织输出；
* 最后把权重按题意保留$6$位小数输出。

---

## 复杂度分析

设训练集大小为$n \times d$，测试集大小为$m \times d$。

每次迭代中，主要计算是：

* $X\mathbf{w}$，复杂度为$O(nd)$；
* $X^T(X\mathbf{w}-\mathbf{y})$，复杂度为$O(nd)$。

因为总迭代次数固定为$T=60$，所以总时间复杂度为：

$$
O(Tnd)
$$

由于$T$是常数，也可以写成：

$$
O(nd)
$$

空间复杂度主要来自存储输入数据和若干中间向量，为：

$$
O(nd+md)
$$

在题目的数据范围内，这个复杂度完全合适。

---

## 代码实现

### Python3

```python
import sys
import json
import numpy as np


# 训练函数：按照题目要求执行归一化梯度下降
def train_ngd(train_X, train_y):
    # 题目给定参数
    eta0 = 0.2
    lam = 0.01
    T = 60
    eps = 1e-10

    # 获取特征维度 d
    d = train_X.shape[1]

    # 权重初始化为全 0 向量
    w = np.zeros(d, dtype=float)

    # 严格按题意迭代 60 步
    for t in range(1, T + 1):
        # 计算梯度：X^T(Xw - y) + 2λw
        grad = train_X.T.dot(train_X.dot(w) - train_y) + 2 * lam * w

        # 若梯度中存在 NaN 或 Inf，则跳过本次更新
        if not np.all(np.isfinite(grad)):
            continue

        # 计算梯度的 L2 范数
        norm = np.linalg.norm(grad, 2)

        # 若梯度范数过小，则跳过本次更新
        if norm < eps:
            continue

        # 梯度归一化
        g_hat = grad / max(norm, eps)

        # 计算当前学习率
        eta = eta0 / np.sqrt(t)

        # 更新权重
        w = w - eta * g_hat

    return w


# 预测函数：线性输出后按题意取符号
def predict(test_X, w):
    # 计算测试集线性输出
    scores = test_X.dot(w)

    # 结果 >= 0 输出 1，否则输出 0
    pred = (scores >= 0).astype(int)

    return pred.tolist()


def main():
    # 读取单行 JSON 输入
    s = sys.stdin.readline().strip()
    data = json.loads(s)

    # 读取并转为 numpy 数组
    train_X = np.array(data["train_X"], dtype=float)
    train_y = np.array(data["train_y"], dtype=float)
    test_X = np.array(data["test_X"], dtype=float)

    # 调用训练函数得到最终权重
    w = train_ngd(train_X, train_y)

    # 调用预测函数得到测试集结果
    test_pred = predict(test_X, w)

    # 权重按题意保留 6 位小数
    weights = [round(float(x), 6) for x in w]

    # 按要求输出 JSON
    ans = {
        "weights": weights,
        "test_pred": test_pred
    }
    print(json.dumps(ans, ensure_ascii=False))


if __name__ == "__main__":
    main()
```