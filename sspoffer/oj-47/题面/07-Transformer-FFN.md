# Transformer FFN

## 题目描述

实现 Transformer 中的 Position-wise Feed-Forward Network（FFN）前向传播。

给定输入矩阵 $X$（$N \times d_{model}$）、第一层权重 $W_1$（$d_{model} \times d_{ff}$）、第一层偏置 $b_1$（$d_{ff}$）、第二层权重 $W_2$（$d_{ff} \times d_{model}$）、第二层偏置 $b_2$（$d_{model}$），计算：

$$
\mathrm{FFN}(X) = \mathrm{ReLU}(XW_1 + b_1)W_2 + b_2
$$

其中 $\mathrm{ReLU}(z) = \max(0, z)$。输出形状为 $N \times d_{model}$。

## 输入描述

第一行包含三个整数 $N, d_{model}, d_{ff}$（$1 \le N \le 50$，$1 \le d_{model} \le 32$，$1 \le d_{ff} \le 64$），分别表示样本数、模型维度、隐层维度。

接下来 $N$ 行，每行 $d_{model}$ 个浮点数，表示输入矩阵 $X$。

接下来 $d_{model}$ 行，每行 $d_{ff}$ 个浮点数，表示权重 $W_1$。

接下来一行 $d_{ff}$ 个浮点数，表示偏置 $b_1$。

接下来 $d_{ff}$ 行，每行 $d_{model}$ 个浮点数，表示权重 $W_2$。

最后一行 $d_{model}$ 个浮点数，表示偏置 $b_2$。

## 输出描述

输出 $N$ 行，每行 $d_{model}$ 个浮点数，表示 FFN 的输出，保留 $2$ 位小数。

## 样例 1

**输入**

```text
1 2 3
1.0 2.0
0.5 -0.5 1.0
-1.0 0.5 0.5
0.1 0.0 -0.1
0.5 0.5
1.0 -1.0
-0.5 1.0
0.0 0.0
```

**输出**

```text
-0.45 1.40
```

**样例解释**

第一层：$XW_1 = [1\cdot 0.5 + 2\cdot(-1.0),\ 1\cdot(-0.5) + 2\cdot 0.5,\ 1\cdot 1.0 + 2\cdot 0.5] = [-1.5, 0.5, 2.0]$，加 $b_1$ 得 $[-1.4, 0.5, 1.9]$，过 ReLU 得 $[0, 0.5, 1.9]$。

第二层：$[0, 0.5, 1.9]W_2 + b_2 = [0\cdot 0.5 + 0.5\cdot 1.0 + 1.9\cdot(-0.5),\ 0\cdot 0.5 + 0.5\cdot(-1.0) + 1.9\cdot 1.0] + [0, 0] = [-0.45, 1.4]$。

## 提示

1. 两层结构：FFN 由两个线性层和一个非线性激活组成，中间维度 $d_{ff}$ 通常远大于 $d_{model}$（如 $4 \cdot d_{model}$）。
2. ReLU 激活：原版 Transformer 用 ReLU，BERT 用 GELU，LLaMA 用 SwiGLU。
3. 逐位置应用：FFN 对每个 token（样本）独立应用相同的两层网络。
