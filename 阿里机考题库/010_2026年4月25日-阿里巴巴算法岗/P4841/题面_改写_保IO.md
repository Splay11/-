# 链式折减最大余值

# 题目内容

网关侧对初始种子值做链式折减验收。

给定正整数数组 $\textit{modSet}$（长度 $\textit{cnt}$）与初始种子 $\textit{seed}$。将 $\textit{modSet}$ 任意重排为 $\textit{order}_1,\ldots,\textit{order}_{\textit{cnt}}$，从 $\textit{cur}_0=\textit{seed}$ 起依次执行

$$\textit{cur}_i = \textit{cur}_{i-1} \bmod \textit{order}_i \quad (1 \le i \le \textit{cnt})$$

求所有重排下 $\textit{cur}_{\textit{cnt}}$ 的最大可能值。

# 输入描述

每个测试文件包含多组测试数据。

- 第一行：整数 $T$（$1 \le T \le 2 \times 10^5$），测试组数。
- 每组数据：
  - 第一行：两个整数 $\textit{cnt},\,\textit{seed}$（$1 \le \textit{cnt} \le 2 \times 10^3$，$0 \le \textit{seed} \le 10^{18}$）；
  - 第二行：$\textit{cnt}$ 个正整数 $\textit{modSet}_1,\ldots,\textit{modSet}_{\textit{cnt}}$（$1 \le \textit{modSet}_i \le 2 \times 10^3$）。

单个测试文件中，所有组的 $\textit{cnt}$ 之和不超过 $5 \times 10^3$。

# 输出描述

每组数据输出一行一个整数，表示最大可能的 $\textit{cur}_{\textit{cnt}}$。

## 样例1

**输入**

```
2
2 10
3 7
3 22
5 8 11
```

**输出**

```
1
2
```

**说明**

- 第一组：最优重排下链式折减的最大余值为 $1$。
- 第二组：最优重排下链式折减的最大余值为 $2$。
