## 解题思路

本题是一个基于 K-最近邻的元学习（Meta-Learning）问题，核心思想是“借鉴相似任务的经验来选择超参数”。

整体流程分为四步：

1. **特征构造**：计算当前任务的元向量
   $$
   \mathbf{m}*{ctr} = \left[n,\ d,\ \frac{|n*{pos}-n_{neg}|}{n}\right].
   $$

2. **KNN 检索**：计算 $\mathbf{m}_{ctr}$ 到每条历史元向量的欧氏距离 $\ell_2$，按“距离、行次序”升序排序，取前 $K=3$ 条。

3. **聚合选 $C^*$**：对这 $3$ 条邻居出现过的每个 $C$，仅在“出现该 $C$ 的邻居”上取 $\text{score}$ 均值；选均值最大者；并列时取较小的 $C$。

4. **训练与预测**：用 $\text{LogisticRegression}(C=C^*)$ 拟合训练集并预测测试集。

关键细节：距离并列时按行次序决定，因此使用稳定排序或按 $(\text{距离}, \text{索引})$ 联合键排序；$C$ 的均值只在其实际出现的邻居上计算，而不是补零平均。

## 复杂度分析

设 $H$ 为历史条目数，$n$ 为训练样本数，$d$ 为特征维度，$m$ 为测试样本数。

* 时间复杂度：
  $$
  O(H \cdot 3 + H\log H + T \cdot n \cdot d^2),
  $$
  其中 $T$ 为 LR 迭代次数；由于 $n \le 60,\ d \le 4$，开销极小。

* 空间复杂度：
  $$
  O(H + n \cdot d).
  $$

## 代码实现

### Python

```python
import sys, json
import numpy as np
from sklearn.linear_model import LogisticRegression

def solve(data):
    # 统一列数：取最短行作为 d（防止样例中的列数不一致笔误）
    train_X_raw = data["train_X"]
    test_X_raw  = data["test_X"]
    d = min(min(len(r) for r in train_X_raw),
            min(len(r) for r in test_X_raw))
    X_tr = np.array([r[:d] for r in train_X_raw], dtype=float)
    X_te = np.array([r[:d] for r in test_X_raw],  dtype=float)
    y_tr = np.array(data["train_y"], dtype=int)
    history = data["history"]

    # 1. 构造当前任务的元特征
    n = len(y_tr)
    n_pos = int((y_tr == 1).sum())
    imb = abs(2 * n_pos - n) / n
    m_ctr = np.array([n, d, imb], dtype=float)

    # 2. 计算 L2 距离，按 (距离, 行次序) 升序取前 3
    items = []
    for i, h in enumerate(history):
        dist = np.linalg.norm(m_ctr - np.array(h["meta"], dtype=float))
        items.append((dist, i, h["C"], h["score"]))
    items.sort(key=lambda x: (x[0], x[1]))
    top3 = items[:3]

    # 3. 统计每个 C 的平均分；升序遍历 + 严格大于 => 并列取最小 C
    c_scores = {}
    for _, _, c, s in top3:
        c_scores.setdefault(c, []).append(s)
    best_c, best_avg = None, -1.0
    for c in sorted(c_scores.keys()):
        avg = sum(c_scores[c]) / len(c_scores[c])
        if avg > best_avg:
            best_avg, best_c = avg, c

    # 4. 训练 LR 并预测
    model = LogisticRegression(penalty="l2", C=best_c, solver="lbfgs",
                               max_iter=1000, random_state=42)
    model.fit(X_tr, y_tr)
    pred = model.predict(X_te).astype(int).tolist()
    return {"C_star": best_c, "pred": pred}

if __name__ == "__main__":
    data = json.loads(sys.stdin.read())
    print(json.dumps(solve(data)))

```