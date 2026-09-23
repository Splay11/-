#include <bits/stdc++.h>
using namespace std;

int solve(int n, const vector<int>& a) {
  // 从左到右扫：左边按过的次数决定当前位被翻转了几次
  int ans = 0, flip = 0;
  for (int i = 0; i < n; i++) {
    // 当前实际状态 = 初值异或「左边已按次数的奇偶」
    int cur = a[i] ^ flip;
    if (cur == 0) {
      // 离开前必须按一次，否则这盏灯再也改不回来
      ans++;
      flip ^= 1;
    }
  }
  return ans;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  // 第一行长度，第二行 0/1 序列
  int n;
  cin >> n;
  vector<int> a(n);
  for (int i = 0; i < n; i++) cin >> a[i];
  cout << solve(n, a) << "\n";
  return 0;
}
