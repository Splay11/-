#include <bits/stdc++.h>
using namespace std;

int solve(int n, const string& s, int m) {
  // 统计 26 种类型各自出现次数
  int cnt[26] = {0};
  for (char ch : s) cnt[ch - 'A']++;
  // 出现次数最多的那种，以及并列最多的种类数
  int mx = 0;
  for (int i = 0; i < 26; i++) mx = max(mx, cnt[i]);
  int kinds = 0;
  for (int i = 0; i < 26; i++) {
    if (cnt[i] == mx) kinds++;
  }
  // 用最多种类搭框架：(mx-1) 个完整「处理+冷却」段，最后再放下 kinds 个
  // 若其它单据足够填满空档，答案就是总张数 n
  int frame = (mx - 1) * (m + 1) + kinds;
  return max(n, frame);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  // 第一行张数，第二行类型串，第三行冷却长度
  int n, m;
  string s;
  cin >> n >> s >> m;
  cout << solve(n, s, m) << "\n";
  return 0;
}
