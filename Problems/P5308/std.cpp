#include <iostream>
#include <vector>
using namespace std;

int solve(int r, int c, vector<vector<int> > d) {
  // dp[i][j]：走到 (i, j) 的最小调节能耗
  vector<vector<int> > dp(r, vector<int>(c, 0));
  // 先填第一行：只能一路向右
  for (int j = 1; j < c; j++) {
    dp[0][j] = dp[0][j - 1] + abs(d[0][j] - d[0][j - 1]);
  }
  // 再填第一列：只能一路向下
  for (int i = 1; i < r; i++) {
    dp[i][0] = dp[i - 1][0] + abs(d[i][0] - d[i - 1][0]);
  }
  // 其余格子取「从上走来」和「从左走来」的较小值
  for (int i = 1; i < r; i++) {
    for (int j = 1; j < c; j++) {
      int up = dp[i - 1][j] + abs(d[i][j] - d[i - 1][j]);
      int left = dp[i][j - 1] + abs(d[i][j] - d[i][j - 1]);
      dp[i][j] = min(up, left);
    }
  }
  return dp[r - 1][c - 1];
}

int main() {
  int r, c;
  cin >> r >> c;
  vector<vector<int> > d(r, vector<int>(c));
  for (int i = 0; i < r; i++) {
    for (int j = 0; j < c; j++) cin >> d[i][j];
  }
  cout << solve(r, c, d) << endl;
  return 0;
}
