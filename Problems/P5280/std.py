import json
import numpy as np


def solve(obj):
  # 训练集最后一列是标签，测试集只有特征
  train = np.asarray(obj["train"], dtype=float)
  test = np.asarray(obj["test"], dtype=float)
  T = int(obj["n_estimators"])
  mfeat = int(obj["max_features"])
  seed = int(obj["seed"])
  X = train[:, :-1]
  y = train[:, -1].astype(int)
  n, d = X.shape
  labels = sorted(set(y.tolist()))

  # 必须用固定种子的 RandomState，且调用顺序不能改
  rg = np.random.RandomState(seed)
  features = []
  bootstraps = []
  tree_pred = []

  for _ in range(T):
    idx = rg.randint(0, n, size=n)
    feat = rg.choice(d, size=mfeat, replace=False)
    feat = np.sort(feat)
    features.append([int(v) for v in feat])
    bootstraps.append([int(v) for v in idx])

    Xb = X[idx][:, feat]
    yb = y[idx]
    Xt = test[:, feat]
    mus = []
    for c in labels:
      mask = yb == c
      if np.any(mask):
        # bootstrap 里出现过：用当前采样的均值
        mu = Xb[mask].mean(axis=0)
      else:
        # 缺失类别：改用全训练集、同一特征子集上的全局质心
        gmask = y == c
        mu = X[gmask][:, feat].mean(axis=0)
      mus.append(mu)
    mus = np.asarray(mus)
    # 平方欧氏距离，并列取更小的类别号
    diff = Xt[:, None, :] - mus[None, :, :]
    dist = np.sum(diff * diff, axis=2)
    pred_t = []
    for i in range(Xt.shape[0]):
      mind = dist[i].min()
      cands = [labels[j] for j in range(len(labels)) if dist[i, j] == mind]
      pred_t.append(min(cands))
    tree_pred.append(pred_t)

  # 多数投票，票数并列也取更小类别号
  pred = []
  ntest = test.shape[0]
  for i in range(ntest):
    cnt = {}
    for t in range(T):
      c = tree_pred[t][i]
      cnt[c] = cnt.get(c, 0) + 1
    best = max(cnt.values())
    cands = [c for c, v in cnt.items() if v == best]
    pred.append(min(cands))

  return {
    "features": features,
    "bootstraps": bootstraps,
    "pred": pred,
  }


if __name__ == "__main__":
  obj = json.loads(input())
  ans = solve(obj)
  print(json.dumps(ans, separators=(",", ":")))
