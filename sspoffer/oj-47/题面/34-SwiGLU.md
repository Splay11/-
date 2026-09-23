# SwiGLU

## 题目描述

提示：本题不支持 PyPy 评测，Python 选手请使用 Python3 提交评测。

实现 LLaMA 系列模型使用的 SwiGLU 激活前向传播，它替代了原版 Transformer FFN 中的 ReLU。

给定输入矩阵 $X$（$N \times d_{model}$）、门控权重 $W_g$（$d_{model} \times d_{ff}$）、上投权重 $W_u$（$d_{model} \times d_{ff}$）、下投权重 $W_d$（$d_{ff} \times d_{model}$），计算：

$$
\mathrm{SwiGLU}(X) = \big(\mathrm{SiLU}(XW_g) \odot (XW_u)\big) W_d
$$

其中 $\mathrm{SiLU}(z) = z \cdot \sigma(z) = z / (1+e^{-z})$，$\odot$ 表示逐元素乘法。本题忽略偏置项，符合 LLaMA 实现。输出形状为 $N \times d_{model}$。

## 输入描述

第一行包含三个整数 $N, d_{model}, d_{ff}$（$1 \le N \le 50$，$1 \le d_{model} \le 32$，$1 \le d_{ff} \le 64$）。

接下来 $N$ 行，每行 $d_{model}$ 个浮点数，表示输入矩阵 $X$。

接下来 $d_{model}$ 行，每行 $d_{ff}$ 个浮点数，表示门控权重 $W_g$。

接下来 $d_{model}$ 行，每行 $d_{ff}$ 个浮点数，表示上投权重 $W_u$。

接下来 $d_{ff}$ 行，每行 $d_{model}$ 个浮点数，表示下投权重 $W_d$。

## 输出描述

输出 $N$ 行，每行 $d_{model}$ 个浮点数，表示 SwiGLU 的输出，保留 $2$ 位小数。

## 样例 1

**输入**

```text
1 2 2
1.0 0.0
1.0 0.0
0.0 1.0
1.0 1.0
1.0 1.0
1.0 0.0
0.0 1.0
```

**输出**

```text
0.73 0.00
```

**样例解释**

$XW_g = [1, 0]$，$\mathrm{SiLU}([1, 0]) = [1/(1+e^{-1}), 0] \approx [0.7311, 0]$。

$XW_u = [1, 1]$。

逐元素乘 $\approx [0.7311, 0]$。

乘 $W_d \approx [0.7311 \cdot 1 + 0 \cdot 0,\ 0.7311 \cdot 0 + 0 \cdot 1] = [0.7311, 0]$。

权重按样例解释对齐：$W_g$ 为 $2 \times 2$ 单位阵，$W_u = \begin{bmatrix}1&1\\1&1\end{bmatrix}$，$W_d$ 为单位阵。若某一行和原图对不上，以原图为准。

## 提示

1. SiLU vs Swish：SiLU（$z \cdot \sigma(z)$）就是 $\beta = 1$ 的 Swish，是 SwiGLU 的激活组件。
2. 门控机制：$\mathrm{SiLU}(XW_g)$ 作为门控信号，$XW_u$ 是被门控的特征，相乘后再下投。
3. LLaMA 等价实现：HuggingFace 中 LlamaMLP 是 `silu(gate_proj(x)) * up_proj(x)` 后再 `down_proj`。
4. 数值稳定：$\sigma(z)$ 在 $z$ 极大或极小时仍稳定，无需特殊处理。
