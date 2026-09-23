#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    // 创建一个 n x n 的 DP 数组
    vector<vector<int>> dp(n, vector<int>(n, 0));

    // 初始条件：起点 (0, 0) 只有一种路径
    dp[0][0] = 1;

    // 动态规划填充表格
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            // 如果不是起点 (0, 0)，则计算当前点的路径数
            if (i > 0) dp[i][j] += dp[i - 1][j];  // 从上方来
            if (j > 0) dp[i][j] += dp[i][j - 1];  // 从左方来
        }
    }

    // 输出结果，终点 (n-1, n-1) 的路径数
    cout << dp[n - 1][n - 1] << endl;

    return 0;
}
