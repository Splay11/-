# 题解

## 题面描述

给定一个包含 $N$ 个用户对 $M$ 部电影评分的矩阵，评分范围为 $1$ 到 $5$ 的整数，未评分用 $0$ 表示。要求对指定的目标用户 $U$，基于用户协同过滤算法，推荐其尚未评分的电影中最可能喜欢的前 $T$ 部电影。

- 输入：
  1. 第一行包含两个整数 $N$ 和 $M$，分别表示用户数量和电影数量。
  2. 接下来的 $N$ 行，每行包含 $M$ 个整数，表示用户对每部电影的评分，未评分记为 $0$。
  3. 接下来一行包含一个整数 $U$，表示目标用户的编号（从 $0$ 开始）。
  4. 最后一行包含一个整数 $T$，表示需要推荐的电影数量。

- 输出：

  输出一行，包含 $T$ 个电影编号（从 $0$ 开始），按照预测评分从高到低依次排列，若预测评分相同则按电影编号从小到大排序。

默认选取与目标用户最相似的前 $K=3$ 个用户参与预测。

---

## 算法思路

1. **计算用户平均评分**  
   对每个用户 $u$，计算其对已评分电影的平均评分：

   ![image](/file/2/qGE2Ft7Ral5G5T_xpnwoA.png) 
   
   其中 $I_u$ 是用户 $u$ 已评分的电影集合。

2. **计算用户相似度（Pearson 相关系数）**  
   对用户 $u$ 和 $v$，首先找出它们都评分过的电影集合 $I_{uv}$，然后计算：
   
   ![image](/file/2/a3Xmmb75luoTPXj4uasyS.png) 

   若 $I_{uv}$ 为空或分母为 $0$，则令 $\text{sim}(u,v)=0$。

3. **选取最相似的用户**  
   根据上述相似度，将其他所有用户与目标用户排序，取前 $K=3$ 个最相似的用户构成集合 $K_u$。

4. **预测评分**  
   对于目标用户 $u$ 未评分的电影 $j$，根据相似用户的评分预测其评分：
   
   ![image](/file/2/AxuoBcfbNB8N1hOT2yIaC.png) 

5. **生成推荐列表**  
   对所有预测评分 $\hat r_{u,j}$ 按从大到小排序，若相同则按电影编号从小到大排序，取前 $T$ 个电影编号作为推荐结果。

---

## 代码实现

```python
import numpy as np


def recommend(ratings, U, T, K=3):
    # ratings: 大小为 (N, M) 的评分矩阵
    # U: 目标用户编号
    # T: 推荐电影数量
    # K: 最相似用户的数量，默认 3

    N, M = ratings.shape

    # 计算每个用户的平均评分（仅对已评分电影）
    user_avg = np.zeros(N)
    for u in range(N):
        rated = ratings[u] > 0
        if np.any(rated):
            user_avg[u] = ratings[u, rated].mean()
        else:
            user_avg[u] = 0.0

    # 计算目标用户 U 与其他用户的 Pearson 相似度
    sims = np.zeros(N)
    for v in range(N):
        if v == U:
            continue
        # 找到共同评分的电影索引
        mask = (ratings[U] > 0) & (ratings[v] > 0)
        if not np.any(mask):
            sims[v] = 0.0
            continue
        # 提取评分并去中心化
        ru = ratings[U, mask] - user_avg[U]
        rv = ratings[v, mask] - user_avg[v]
        denom = np.sqrt(np.sum(ru ** 2)) * np.sqrt(np.sum(rv ** 2))
        if denom == 0:
            sims[v] = 0.0
        else:
            sims[v] = np.sum(ru * rv) / denom

    # 选取与 U 最相似的前 K 个用户
    top_k = np.argsort(-sims)[:K]

    # 对 U 未评分的电影进行评分预测
    preds = np.zeros(M)
    for j in range(M):
        if ratings[U, j] > 0:
            # 已评分电影跳过
            preds[j] = -np.inf
            continue
        # 收集相似用户对电影 j 的评分偏差
        num = 0.0
        den = 0.0
        for v in top_k:
            if sims[v] == 0:
                continue
            if ratings[v, j] > 0:
                num += sims[v] * (ratings[v, j] - user_avg[v])
                den += abs(sims[v])
        # 如果没有用户提供评分，则使用目标用户的平均评分
        if den == 0.0:
            preds[j] = user_avg[U]
        else:
            preds[j] = user_avg[U] + num / den

    # 按预测评分排序，取前 T 个电影编号
    # 若预测相同，则电影编号小的优先
    recs = np.argsort(-preds, kind='stable')[:T]
    return recs


if __name__ == '__main__':
    # 读入数据
    N, M = map(int, input().split())
    ratings = np.array([list(map(int, input().split())) for _ in range(N)])
    U = int(input().strip())
    T = int(input().strip())

    # 调用推荐函数并输出结果
    recommendations = recommend(ratings, U, T)
    print(' '.join(map(str, recommendations)))
```