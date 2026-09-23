#include <iostream>
#include <string>
#include <vector>
using namespace std;

const long long INF = 1000000000000000005LL;

long long add(long long a, long long b) {
  if (a > INF - b) return INF;
  return a + b;
}

string solve(int m, long long q, string b) {
  // ways0/ways1：定长、定开头色的交错子序列个数
  vector<long long> ways0(m + 1), ways1(m + 1), pre0(m + 1), pre1(m + 1);
  for (int i = 0; i < m; i++) {
    vector<long long> cur(m + 1);
    cur[1] = 1;
    if (b[i] == '0') {
      for (int L = 2; L <= i + 1; L++) cur[L] = pre1[L - 1];
    } else {
      for (int L = 2; L <= i + 1; L++) cur[L] = pre0[L - 1];
    }
    for (int L = 1; L <= i + 1; L++) {
      char start = (L % 2 == 1) ? b[i] : (b[i] == '0' ? '1' : '0');
      if (start == '0') ways0[L] = add(ways0[L], cur[L]);
      else ways1[L] = add(ways1[L], cur[L]);
    }
    if (b[i] == '0') {
      for (int L = 1; L <= i + 1; L++) pre0[L] = add(pre0[L], cur[L]);
    } else {
      for (int L = 1; L <= i + 1; L++) pre1[L] = add(pre1[L], cur[L]);
    }
  }
  q -= 1;
  for (int L = 1; L <= m; L++) {
    long long cnts[2] = {ways0[L], ways1[L]};
    for (int start = 0; start <= 1; start++) {
      if (q <= cnts[start]) {
        string t = "";
        int bit = start;
        for (int j = 0; j < L; j++) {
          t += char('0' + bit);
          bit = 1 - bit;
        }
        return t;
      }
      q -= cnts[start];
    }
  }
  return "-1";
}

int main() {
  int m;
  long long q;
  string b;
  cin >> m >> q >> b;
  cout << solve(m, q, b) << "\n";
  return 0;
}
