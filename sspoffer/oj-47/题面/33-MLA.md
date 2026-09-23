# MLA（Multi-head Latent Attention）

## 题目描述

实现 MLA（Multi-head Latent Attention）的前向传播。MLA 是 DeepSeek-V2 提出的注意力机制，核心是把 Key 和 Value 压缩到低维潜变量，从而大幅减少推理时的 KV 缓存。

本题同时包含解耦 RoPE：内容部分（NoPE）与位置部分分开。为简化，旋转之后的位置向量直接给出，不需要自行实现 RoPE。

给定输入 $X$（$N \times d$）。按头计算，每头内容维度为 $d_h$。可见计算步骤为：

1. 低秩压缩（KV 共享潜变量，位置部分单独给出）：
   - $C_{kv} = X W_{DKV}$，$C_q = X W_{DQ}$。
   - 内容 Query / Key / Value 由潜变量上投影：$Q_c = C_q W_{UQ}$，$K_c = C_{kv} W_{UK}$，$V = C_{kv} W_{UV}$。
2. 位置部分 $Q_r$、$K_r$ 由输入中的对应投影得到（已经是旋转后的向量）。
3. 每个头把内容分数和位置分数相加，再做因果掩码与 softmax：

$$
\mathrm{scores} = \frac{Q_c K_c^{\mathsf T}}{\sqrt{d_h}} + \frac{Q_r K_r^{\mathsf T}}{\sqrt{d_{rope}}}
$$

$j \le i$ 的位置保留，$j > i$（未来 token）置为 $-\infty$。然后 $\mathrm{weights} = \mathrm{softmax}(\mathrm{scores})$，$\mathrm{head} = \mathrm{weights}\, V$。

4. 各头拼接后经输出投影 $W_o$ 得到最终输出。

## 输入描述

第一行包含七个整数 $N, d, n_h, n_q, d_c, d_h, d_{rope}$。截图给出的范围约为 $2 \le N \le 12$，$2 \le d \le 8$，$1 \le n_h \le 4$，压缩秩与每头维度 $d_c, d_h, d_{rope}$ 均为小整数（约 $1$ 到 $4$），且 $d$ 能被相关头维度整除。

其后依次为 $X$ 以及各投影矩阵（查询下投影、查询上投影、KV 下投影、K 上投影、V 上投影、位置部分投影、输出投影）。每一段的行列写在截图对应段落前。

## 输出描述

输出 $N$ 行，每行与输出特征维相同的浮点数，表示 MLA 前向结果，保留 $4$ 位小数。

## 样例

截图中有两组样例。权重矩阵行数多、字号小，逐格抄录不可靠，这里不写入可能抄错的数字。两组样例的输出都是若干行浮点数（$4$ 位小数）。请以原图中的输入矩阵和输出为准。

**样例解释（可见部分）**

- 样例 1：多个 token。$Q$ 与 KV 拆成若干头。$C_{kv} = X W_{DKV}$ 得到低维潜变量；内容分数与位置分数相加后再 softmax。因果掩码把上三角置为 $-\infty$。
- 样例 2：$3$ 个 token。解释强调 $d_c$ 远小于 $n_h \cdot d_h$，KV 缓存从 $2Nn_h d_h$ 降到潜变量长度。

## 提示

1. 低秩：$d_c \ll n_h d_h$。KV 缓存从 $2Nn_h d_h$ 降到潜变量维度，对长序列节省显著。
2. 两个分数项分别计算再相加，然后做一次 softmax。缩放用每头维度的 $\sqrt{d_h}$（位置项用 $\sqrt{d_{rope}}$）。若误除以 $\sqrt{d}$，位置项会单独放大。
3. 因果掩码：上三角（不可见位置）置为 $-\infty$，softmax 之后对应权重为 $0$。
