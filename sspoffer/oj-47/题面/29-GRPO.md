# GRPO（Group Relative Policy Optimization）

## 题目描述

实现 GRPO（Group Relative Policy Optimization）损失函数的计算。

GRPO 是 DeepSeekMath 提出的强化学习对齐算法。它与 PPO 的关键区别在于：PPO 需要训练一个 critic 网络来估计优势，而 GRPO 对同一个 prompt 采样一组回答，直接用组内奖励的相对高低来估计优势，从而省掉 critic。

给定一组 $G$ 个回答，每个回答有奖励 $r_i$、当前策略的 log 概率 $\pi_i$、采样时旧策略的 log 概率 $\pi_i^{old}$、参考模型的 log 概率 $\pi_i^{ref}$。

第一步，组内归一化得到优势：

$$
A_i = \frac{r_i - \mathrm{mean}(r)}{\mathrm{std}(r) + \varepsilon_{std}}
$$

其中 $\mathrm{std}$ 为总体标准差（除以 $G$ 而非 $G-1$），$\varepsilon_{std} = 10^{-8}$ 用于防止除零。

第二步，计算重要性采样比：

$$
\rho_i = \exp(\pi_i - \pi_i^{old})
$$

第三步，用 k3 估计器计算逐样本 KL 散度：

$$
KL_i = \exp(\pi_i^{ref} - \pi_i) - (\pi_i^{ref} - \pi_i) - 1
$$

第四步，组合成损失：

$$
\mathcal{L}_{GRPO} = -\frac{1}{G}\sum_{i=1}^{G}\left[\min\big(\rho_i A_i,\ \mathrm{clip}(\rho_i, 1-\epsilon, 1+\epsilon)\,A_i\big) - \beta \cdot KL_i\right]
$$

## 输入描述

第一行输入一个整数 $G$（$2 \le G \le 1000$）和两个浮点数 $\epsilon$（$0.01 \le \epsilon \le 0.5$）、$\beta$（$0 \le \beta \le 1.0$），分别表示组大小、裁剪范围和 KL 惩罚系数。

接下来 $G$ 行，每行输入 $4$ 个浮点数 $r_i$、$\pi_i$、$\pi_i^{old}$、$\pi_i^{ref}$，其中 $-10 \le r_i \le 10$，$-20 \le \pi_i, \pi_i^{old}, \pi_i^{ref} \le 0$。

## 输出描述

第一行输出 $G$ 个空格分隔的优势值 $A_i$，保留 $4$ 位小数。

第二行输出 GRPO 损失值，保留 $4$ 位小数。

## 样例 1

**输入**

```text
4 0.2 0.1
1.0000 -2.0000 -2.0000 -2.1000
2.0000 -1.5000 -1.6000 -1.7000
0.0000 -3.0000 -2.8000 -3.2000
1.0000 -2.2000 -2.2000 -2.0000
```

**输出**

```text
0.0000 1.4142 -1.4142 0.0000
-0.0997
```

**样例解释**

组内奖励 $r = [1, 2, 0, 1]$，均值为 $1$，总体标准差为 $\sqrt{0.5} \approx 0.7071$，故 $A = [0, 1.4142, -1.4142, 0]$。

重要性比 $\rho = [1, 1.1052, 0.8187, 1]$ 全部落在 $[0.8, 1.2]$ 内，裁剪未生效。

第 $1$ 组与第 $4$ 组优势为 $0$，对裁剪项无贡献，只留 KL 惩罚。

## 提示

1. 组内归一化用总体标准差：`np.std(r)` 默认 `ddof=0`，正是本题所需，不要写成 `ddof=1`。
2. 优势全相同时的退化：若组内奖励完全一样，$\mathrm{std}(r) = 0$，此时全部 $A_i = 0$，损失只剩 KL 项。$\varepsilon_{std}$ 保证这种情况不会除零。
3. KL 的 k3 估计器恒非负：$e^{x} - x - 1 \ge 0$ 对任意实数成立，因此 KL 惩罚永远是在增大损失。
