#include <iostream>
#include <vector>
using namespace std;

// dp[i][j] 表示走到 (i,j) 的最小路径和
int solve(vector<vector<int> >& dp, int m, int n) {
    // 第一列只能一直往下
    for (int i = 1; i < m; i++) {
        dp[i][0] += dp[i - 1][0];
    }
    // 第一行只能一直往右
    for (int j = 1; j < n; j++) {
        dp[0][j] += dp[0][j - 1];
    }
    for (int i = 1; i < m; i++) {
        for (int j = 1; j < n; j++) {
            // 只能从上或从左走来
            int up = dp[i - 1][j];
            int left = dp[i][j - 1];
            dp[i][j] += (up < left ? up : left);
        }
    }
    return dp[m - 1][n - 1];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int m, n;
    cin >> m >> n;
    vector<vector<int> > grid(m, vector<int>(n));
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            cin >> grid[i][j];
        }
    }
    cout << solve(grid, m, n) << '\n';
    return 0;
}
