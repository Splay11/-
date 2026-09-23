#include <bits/stdc++.h>
using namespace std;

int main() {
  int n;
  string s;
  // 读入长度与报文
  cin >> n >> s;
  int i = 0;
  // 跳过前缀 z：这些位已经最大，再后继会变成 a
  while (i < n && s[i] == 'z') i++;
  if (i == n) {
    // 全是 z，无法变大
    cout << s << "\n";
    return 0;
  }
  // 第一个非 z 要抬成 z，整段共用这个步数
  int k = 'z' - s[i];
  int j = i;
  // 只纳入后继后仍不超过 z 的字符，保证不会绕回成很小的字母
  while (j < n && s[j] + k <= 'z') j++;
  for (int p = i; p < j; p++) {
    // 对闭区间 [i, j-1] 同时后继 k 次
    s[p] = char('a' + (s[p] - 'a' + k) % 26);
  }
  cout << s << "\n";
  return 0;
}
