# DPO（Direct Preference Optimization）

## 题目描述

实现 DPO（Direct Preference Optimization）损失函数的计算。

给定 $n$ 组偏好数据，每组包含一个 chosen（偏好好回答）和一个 rejected（非偏好回答）的 log 概率。DPO 损失定义为：

$$
\mathcal{L}_{DPO} = -\frac{1}{n}\sum_{i=1}^{n}\log\sigma\left(\beta\cdot\left[(r_{\theta}^{w_i}-r_{\theta}^{l_i})-(r_{ref}^{w_i}-r_{ref}^{l_i})\right]\right)
$$

其中 $\sigma$ 是 sigmoid 函数，$\beta$ 是温度参数，$r_{\theta}^{w}$ 和 $r_{\theta}^{l}$ 分别是策略模型对 chosen / rejected 的 log 概率，$r_{ref}^{w}$ 和 $r_{ref}^{l}$ 是参考模型对 chosen / rejected 的 log 概率。

简化记号：令 $\Delta_i = \beta\cdot\left[(r_{\theta}^{w_i}-r_{\theta}^{l_i})-(r_{ref}^{w_i}-r_{ref}^{l_i})\right]$

$$
\mathcal{L}_{DPO} = -\frac{1}{n}\sum_{i=1}^{n}\log\sigma(\Delta_i)
$$

## 输入描述

第一行包含一个整数 $n$（$1 \le n \le 1000$）和一个浮点数 $\beta$（$0.01 \le \beta \le 1.0$）。

接下来 $n$ 行，每行 $4$ 个浮点数：$r_{\theta}^{w_i}$，$r_{\theta}^{l_i}$，$r_{ref}^{w_i}$，$r_{ref}^{l_i}$。

## 输出描述

输出 DPO 损失值，保留 $4$ 位小数。

## 样例 1

**输入**

```text
2 0.1
-1.0 -3.0 -1.5 -2.5
-2.0 -4.0 -2.5 -3.0
```

**输出**

```text
0.6327
```

**样例解释**

$n = 2$，$\beta = 0.1$。第一组：$\Delta_1 = 0.1 \times [(-1.0-(-3.0))-(-1.5-(-2.5))] = 0.1 \times [2.0-1.0] = 0.1$。第二组类似。$\mathcal{L} = -\dfrac{1}{2}[\log\sigma(0.1)+\log\sigma(0.15)]$。

## 提示

1. Sigmoid 数值稳定：$\log\sigma(x) = x - \log(1+e^{x})$，当 $x$ 很大时用 $-\log(1+e^{-x})$。
2. 物理含义：DPO 希望策略模型比参考模型更偏好 chosen（$\Delta > 0$）。
