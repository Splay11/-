#include <iostream>
#include <vector>
using namespace std;

const int MOD = 1e9 + 7;

int main() {
    int n;
    cin >> n;

    // 创建一个 (n+1) x (n+1) 的 dp 表
    vector<vector<int>> dp(n + 1, vector<int>(n + 1, 0));
    
    // 初始化 dp[0][0] = 1
    dp[0][0] = 1;

    // 动态规划求解
    for (int i = 1; i <= n; ++i) {
        for (int j = 0; j <= n; ++j) {
            dp[i][j] = dp[i - 1][j]; // 不使用当前数 i
            if (j >= i) {
                dp[i][j] = (dp[i][j] + dp[i][j - i]) % MOD; // 使用当前数 i
            }
        }
    }

    // 输出结果
    cout << dp[n][n] << endl;
    
    return 0;
}
