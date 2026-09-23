#include <bits/stdc++.h>
using namespace std;

const int MAXM = 2000;
const int THRESH = 500;

int main() {
  int n;
  cin >> n;
  vector<int> w(n), a(n), b(n);
  for (int i = 0; i < n; i++) cin >> w[i] >> a[i] >> b[i];

  vector<long long> prefixB(n + 1, 0), suffixB(n + 1, 0);
  for (int i = 0; i < n; i++) prefixB[i + 1] = prefixB[i] + b[i];
  for (int i = n - 1; i >= 0; i--) suffixB[i] = suffixB[i + 1] + b[i];

  vector<vector<long long>> f(n + 1, vector<long long>(MAXM));
  for (int m = 0; m < MAXM; m++) f[n][m] = m;

  for (int i = n - 1; i >= 0; i--) {
  for (int m = 0; m < MAXM; m++) {
    long long nm;
    if (w[i] < m) {
      nm = m - b[i];
      if (nm < 0) nm = 0;
    } else {
      nm = m + a[i];
    }
    if (nm >= MAXM) {
      if (nm - suffixB[i + 1] > THRESH) {
        f[i][m] = nm - suffixB[i + 1];
      } else {
        int j = i;
        long long cur = nm;
        while (j < n && cur > THRESH) {
          cur -= b[j];
          j++;
        }
        if (j >= n) f[i][m] = cur;
        else f[i][m] = f[j][cur];
      }
    } else {
      f[i][m] = f[i + 1][nm];
    }
  }
  }

  auto applyFrom = [&](int i, long long money) -> long long {
    if (i >= n) return money;
    if (money > THRESH && money - suffixB[i] > THRESH) return money - suffixB[i];
    if (money < MAXM) return f[i][money];
    int j = i;
    long long cur = money;
    while (j < n && cur > THRESH) {
      cur -= b[j];
      j++;
    }
    if (j >= n) return cur;
    return f[j][cur];
  };

  auto answer = [&](long long x) -> long long {
    if (x < MAXM) return f[0][x];
    if (x - suffixB[0] > THRESH) return x - suffixB[0];
    int lo = 0, hi = n;
    while (lo < hi) {
      int mid = (lo + hi + 1) / 2;
      if (x - prefixB[mid] > THRESH) lo = mid;
      else hi = mid - 1;
    }
    int i = lo;
    long long money = x - prefixB[i];
    if (i >= n) return money;
    return applyFrom(i, money);
  };

  int q;
  cin >> q;
  while (q--) {
    long long x;
    cin >> x;
    cout << answer(x) << "\n";
  }
  return 0;
}
