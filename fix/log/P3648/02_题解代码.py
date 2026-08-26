## 解题思路

### 核心方法

* 标准化：将 `train` 与 `test` 按行拼接后，用 `StandardScaler` **一次性** `fit_transform`，得到标准化矩阵 `Z_all`（避免因分别拟合造成的数据偏移）。
* PCA降维与重构：在 `Z_all` 上用 `PCA(n_components=1, svd_solver="full", random_state=42)` 拟合，分别对 `Z_all` 做 `transform → inverse_transform` 得到重构矩阵 `Z_hat_all`。
* 误差与阈值：

  * 训练部分重构误差：对 `Z_all` 的训练行计算 $e_i=\sum_j (Z_{ij}-\hat Z_{ij})^2$。
  * 阈值 $T$：取训练误差的第 95 百分位数。
  * 判别：对测试样本误差 $e_{\text{test}}$ 若 $\le T$ 输出 `0`，否则输出 `1`。
* 输出：仅输出测试部分标签，单行 JSON 数组，如 `[0, 1]`（逗号后带空格）。


## 代码实现

### Python

```python
import sys, json
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def main():
    s = sys.stdin.read().strip()
    data = json.loads(s)
    train = np.array(data["train"], dtype=float)
    test = np.array(data["test"], dtype=float)

    # 基本校验：至少二维特征，且 train/test 维度一致
    assert train.ndim == 2 and test.ndim == 2
    assert train.shape[1] == test.shape[1] and train.shape[1] >= 2

    # 1) 拼接后一次性标准化
    X_all = np.vstack([train, test])
    scaler = StandardScaler()
    Z_all = scaler.fit_transform(X_all)  # 避免偏移：train+test 一次性 fit_transform

    # 2) PCA=1 维，拟合在拼接的标准化数据上
    pca = PCA(n_components=1, svd_solver="full", random_state=42)
    Z_proj = pca.fit_transform(Z_all)               # 在 Z_all 上 fit
    Z_hat_all = pca.inverse_transform(Z_proj)       # 标准化空间的重构

    # 3) 误差：在标准化空间计算
    errs = np.sum((Z_all - Z_hat_all) ** 2, axis=1)

    # 4) 阈值：训练部分的第95百分位
    n = train.shape[0]
    T = float(np.percentile(errs[:n], 95))  # 第95百分位

    # 5) 测试样本标签：e_test <= T -> 0，否则 1
    test_errs = errs[n:]
    y = (test_errs > T).astype(int).tolist()

    # 6) 输出：单行 JSON，逗号后带空格
    print(json.dumps(y, ensure_ascii=False))

if __name__ == "__main__":
    main()
```