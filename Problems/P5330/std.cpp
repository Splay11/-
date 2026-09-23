#include <iostream>
#include <string>
#include <vector>
using namespace std;

int szn;
vector<int> mx, mn, lz;

void app(int i, int v) {
  // 整段加上延迟标记
  mx[i] += v;
  mn[i] += v;
  lz[i] += v;
}

void push(int i) {
  if (lz[i] != 0) {
    app(i * 2, lz[i]);
    app(i * 2 + 1, lz[i]);
    lz[i] = 0;
  }
}

void pull(int i) {
  mx[i] = max(mx[i * 2], mx[i * 2 + 1]);
  mn[i] = min(mn[i * 2], mn[i * 2 + 1]);
}

void add(int l, int r, int v, int i, int L, int R) {
  // 区间 [l,r] 上的 h 全部加 v
  if (r < L || R < l) return;
  if (l <= L && R <= r) {
    app(i, v);
    return;
  }
  push(i);
  int mid = (L + R) >> 1;
  add(l, r, v, i * 2, L, mid);
  add(l, r, v, i * 2 + 1, mid + 1, R);
  pull(i);
}

int qmax(int l, int r, int i, int L, int R) {
  if (r < L || R < l) return -1e9;
  if (l <= L && R <= r) return mx[i];
  push(i);
  int mid = (L + R) >> 1;
  return max(qmax(l, r, i * 2, L, mid), qmax(l, r, i * 2 + 1, mid + 1, R));
}

int leftEq(int l, int r, int val, int i, int L, int R) {
  // [l,r] 里最左的、h 恰好等于 val 的位置；没有则返回 -1
  if (r < L || R < l || mx[i] < val || mn[i] > val) return -1;
  if (L == R) return mx[i] == val ? L : -1;
  push(i);
  int mid = (L + R) >> 1;
  int a = leftEq(l, r, val, i * 2, L, mid);
  if (a != -1) return a;
  return leftEq(l, r, val, i * 2 + 1, mid + 1, R);
}

string solve(int k, const vector<int> &p, const vector<int> &q) {
  // 共有 k+1 个窗。装满段不能留空；某段人比窗多则全是 0
  int m = k + 1;
  vector<vector<int> > byR(m + 2);
  for (int i = 0; i < k; i++) byR[q[i]].push_back(p[i]);

  szn = 1;
  while (szn < m + 2) szn *= 2;
  mx.assign(szn * 2, 0);
  mn.assign(szn * 2, 0);
  lz.assign(szn * 2, 0);
  for (int i = 1; i <= m + 1; i++) {
    mx[szn + i] = i;
    mn[szn + i] = i;
  }
  for (int i = szn - 1; i >= 1; i--) {
    mx[i] = max(mx[i * 2], mx[i * 2 + 1]);
    mn[i] = min(mn[i * 2], mn[i * 2 + 1]);
  }

  int total = 0;
  bool overflow = false;
  vector<int> diff(m + 3, 0);
  vector<int> freq(m + 2, 0), touched(m + 2, 0);
  for (int R = 1; R <= m; R++) {
    // 右端点等于 R 的人加入；相同左端点合并成一次区间加
    if (byR[R].empty()) continue;
    int nt = 0;
    for (int x : byR[R]) {
      if (freq[x] == 0) touched[nt++] = x;
      freq[x]++;
    }
    for (int i = 0; i < nt; i++) {
      int x = touched[i];
      int c = freq[x];
      freq[x] = 0;
      total += c;
      if (x + 1 <= m) add(x + 1, m, -c, 1, 0, szn - 1);
    }
    if (overflow) continue;
    int gmx = qmax(1, R, 1, 0, szn - 1) + total - (R + 1);
    if (gmx > 0) {
      overflow = true;
    } else if (gmx == 0) {
      int target = (R + 1) - total;
      int L = leftEq(1, R, target, 1, 0, szn - 1);
      if (L != -1) {
        diff[L]++;
        diff[R + 1]--;
      }
    }
  }
  if (overflow) return string(m, '0');
  string ans;
  ans.resize(m);
  int s = 0;
  for (int t = 1; t <= m; t++) {
    s += diff[t];
    ans[t - 1] = (s > 0 ? '0' : '1');
  }
  return ans;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(0);
  int k;
  cin >> k;
  vector<int> p(k), q(k);
  for (int i = 0; i < k; i++) cin >> p[i] >> q[i];
  cout << solve(k, p, q) << "\n";
  return 0;
}
