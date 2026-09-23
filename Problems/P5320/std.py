import json
import numpy as np


def solve(train, test):
  # 标签 0/1 映到 -1/+1，特征前面补 1 当作偏置
  X = []
  y = []
  for feat, lab in train:
    X.append([1.0] + [float(v) for v in feat])
    y.append(-1.0 if lab == 0 else 1.0)
  X = np.array(X, dtype=float)
  y = np.array(y, dtype=float)
  # 权向量从全 0 开始，学习率 1，固定走 10 轮
  h = np.zeros(X.shape[1], dtype=float)
  for _ in range(10):
    for i in range(len(X)):
      score = float(np.dot(h, X[i]))
      pred = 1.0 if score >= 0.0 else -1.0
      # 分错才更新：权向量沿正确方向加一刀
      if pred != y[i]:
        h = h + y[i] * X[i]
  ans = []
  for feat in test:
    xb = np.array([1.0] + [float(v) for v in feat], dtype=float)
    score = float(np.dot(h, xb))
    pred = 1.0 if score >= 0.0 else -1.0
    ans.append(1 if pred == 1.0 else 0)
  return ans


raw = input()
# 标准输入可能是多行 JSON，继续读完
more = []
try:
  while True:
    line = input()
    more.append(line)
except EOFError:
  pass
if more:
  raw = raw + "\n" + "\n".join(more)
obj = json.loads(raw)
print(json.dumps(solve(obj["train"], obj["test"])))
