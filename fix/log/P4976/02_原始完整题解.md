## 解题思路

使用$scikit-learn$中的$Pipeline$把$StandardScaler$和线性$SVM$组合起来，保证交叉验证时每一折都只在当前训练折上进行标准化拟合，避免数据泄漏。

核心步骤如下：

1. 将训练数据拆分为特征$X$和标签$y$。
2. 使用$StandardScaler$进行特征标准化。
3. 使用$SVC$，固定$kernel = "linear"$，$random_state = 42$。
4. 使用$StratifiedKFold$进行$3$折分层交叉验证。
5. 使用$GridSearchCV$在$C \in {0.1, 1.0, 10.0}$中选择最优参数。
6. $GridSearchCV$设置$refit = True$，会自动使用最优参数在完整训练集上重新训练。
7. 对测试集进行预测并逐行输出结果。

## 复杂度分析

设训练样本数为$n$，特征维度为$m$，测试样本数为$q$。

网格中共有$3$个$C$，交叉验证为$3$折，因此需要训练$9$次模型，最后还会在完整训练集上重新训练$1$次。

线性$SVC$训练复杂度与实现有关，通常可近似记为$T_{svm}$，总时间复杂度约为：

$O(10 \times T_{svm} + q \times m)$

在本题$n \le 200$，$m \le 10$的数据范围下可以顺利运行。

空间复杂度主要来自训练数据、标准化后的数据以及模型存储，约为：

$O(n \times m + q \times m)$

## 代码实现

### Python

```python
import sys
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold, GridSearchCV


# 使用线性SVM和网格搜索完成训练与预测
def svm_predict(train_data, test_data):
    # 转为numpy数组，便于切分特征和标签
    train_arr = np.array(train_data, dtype=float)
    test_arr = np.array(test_data, dtype=float)

    # 前m列为特征，最后一列为标签
    X = train_arr[:, :-1]
    y = train_arr[:, -1].astype(int)

    # 构建标准化 + 线性SVM的流水线
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("svc", SVC(kernel="linear", random_state=42))
    ])

    # 设置C的搜索范围
    param_grid = {
        "svc__C": [0.1, 1.0, 10.0]
    }

    # 分层3折交叉验证
    cv = StratifiedKFold(
        n_splits=3,
        shuffle=True,
        random_state=42
    )

    # 使用GridSearchCV选择最佳C，并自动在完整训练集上重训
    grid = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        scoring="accuracy",
        cv=cv,
        refit=True
    )

    # 训练模型
    grid.fit(X, y)

    # 对测试集进行预测
    preds = grid.predict(test_arr)

    return preds.astype(int)


def main():
    # 读取全部输入
    data = sys.stdin.read().strip().split()
    idx = 0

    # 读取训练样本数n和特征维度m
    n = int(data[idx])
    idx += 1
    m = int(data[idx])
    idx += 1

    # 读取训练数据
    train_data = []
    for _ in range(n):
        row = []
        for _ in range(m + 1):
            row.append(float(data[idx]))
            idx += 1
        train_data.append(row)

    # 读取测试样本数q
    q = int(data[idx])
    idx += 1

    # 读取测试数据
    test_data = []
    for _ in range(q):
        row = []
        for _ in range(m):
            row.append(float(data[idx]))
            idx += 1
        test_data.append(row)

    # 调用外部函数完成预测
    preds = svm_predict(train_data, test_data)

    # 按要求逐行输出预测标签
    for p in preds:
        print(int(p))


if __name__ == "__main__":
    main()
```