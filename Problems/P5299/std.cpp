#include <bits/stdc++.h>
using namespace std;

int n;
vector<int> distv;

// 把左边 p 个三进制位倒过来，对应前缀反转
int rev_prefix(int x, int p) {
  int d[13];
  int t = x;
  // 低位在物理右边，先拆出从左到右的各位
  for (int i = n - 1; i >= 0; i--) {
    d[i] = t % 3;
    t /= 3;
  }
  int i = 0, j = p - 1;
  while (i < j) {
    swap(d[i], d[j]);
    i++;
    j--;
  }
  int y = 0;
  for (int k = 0; k < n; k++) y = y * 3 + d[k];
  return y;
}

void build() {
  int tot = 1;
  for (int i = 0; i < n; i++) tot *= 3;
  distv.assign(tot, -1);
  queue<int> q;
  // 所有「AAA...BBB...CCC...」作为距离 0 的源点
  for (int na = 0; na <= n; na++) {
    for (int nb = 0; nb <= n - na; nb++) {
      int nc = n - na - nb;
      int x = 0;
      for (int i = 0; i < na; i++) x = x * 3 + 0;
      for (int i = 0; i < nb; i++) x = x * 3 + 1;
      for (int i = 0; i < nc; i++) x = x * 3 + 2;
      distv[x] = 0;
      q.push(x);
    }
  }
  // 前缀反转是对合，从有序串 BFS 得到任意串的最少反转次数
  while (!q.empty()) {
    int x = q.front();
    q.pop();
    int d0 = distv[x];
    for (int p = 2; p <= n; p++) {
      int y = rev_prefix(x, p);
      if (distv[y] < 0) {
        distv[y] = d0 + 1;
        q.push(y);
      }
    }
  }
}

int encode(const string& s) {
  int x = 0;
  for (char c : s) x = x * 3 + (c - 'A');
  return x;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int qn;
  // 读入串长和询问条数
  cin >> n >> qn;
  build();
  while (qn--) {
    string s;
    cin >> s;
    cout << distv[encode(s)] << "\n";
  }
  return 0;
}
