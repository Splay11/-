### 思路

* **初始化**: 用 `train` 的前 3 行作为质心 `c0,c1,c2`。
* **迭代(≤100轮)**:

  * 计算每个训练样本到 3 个质心的欧氏距离，按最小距离分配簇（并列取索引小者）。
  * 逐簇取均值作为新质心；若簇空则质心不变。
  * 收敛判定：所有质心各坐标变化量的最大绝对值 < 1e-6 即停止。
* **重映射**: 将 3 个质心按坐标字典序升序排序，并据此将质心编号重置为 0/1/2。
* **预测**: 用排序后的质心对 `test` 逐行取最近质心编号，输出 JSON 数组。

### Python 实现

```python
import sys
import json
import numpy as np

def kmeans_predict(train, test, k=3, max_iter=100, tol=1e-6):
    X = np.asarray(train, dtype=float)
    T = np.asarray(test, dtype=float)

    # 初始化质心：前3行
    centroids = X[:k].copy()

    for _ in range(max_iter):
        # 计算距离并分配簇（并列索引最小者优先由 argmin 保证）
        dists = np.linalg.norm(X[:, None, :] - centroids[None, :, :], axis=2)
        labels = np.argmin(dists, axis=1)

        # 备份质心用于收敛判断
        old = centroids.copy()

        # 重新计算质心；空簇保持不变
        for i in range(k):
            mask = (labels == i)
            if np.any(mask):
                centroids[i] = X[mask].mean(axis=0)

        # 收敛判断：所有坐标变化量 < tol
        if np.max(np.abs(centroids - old)) < tol:
            break

    # 质心排序（按第一维、再第二维... 升序），并重置编号为 0/1/2
    order = np.lexsort(centroids.T[::-1])
    centroids_sorted = centroids[order]

    # 用最终质心为 test 打标签
    tdists = np.linalg.norm(T[:, None, :] - centroids_sorted[None, :, :], axis=2)
    preds = np.argmin(tdists, axis=1)
    return preds.tolist()

def main():
    data = json.loads(sys.stdin.read())
    train = data["train"]
    test = data["test"]
    preds = kmeans_predict(train, test, k=3, max_iter=100, tol=1e-6)
    sys.stdout.write(json.dumps(preds, separators=(',', ':')))

if __name__ == "__main__":
    main()
```

* 读取单行 JSON，按要求进行 K-Means（初始化、空簇处理、收敛阈值 1e-6、最多 100 轮），质心按字典序排序后对测试集输出 `[0,1,2]` 标签。