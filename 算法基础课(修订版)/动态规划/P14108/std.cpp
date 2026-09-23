#include <iostream>
#include <vector>

using namespace std;

int main() {
    // 读取输入
    int n;
    cin >> n; // 输入序列的长度
    vector<int> a(n); // 存储整数序列
    for (int i = 0; i < n; ++i) {
        cin >> a[i]; // 输入序列中的每个整数
    }

    // 动态规划数组 dp，dp[i] 表示前缀和 S_i
    vector<int> dp(n + 1, 0); // 初始化 dp 数组，dp[0] = 0

    // 根据动态规划的状态转移公式计算前缀和
    for (int i = 1; i <= n; ++i) {
        dp[i] = dp[i - 1] + a[i - 1]; // dp[i] = dp[i-1] + a[i-1]
        cout << dp[i] << endl; // 输出前缀和
    }

    return 0;
}
