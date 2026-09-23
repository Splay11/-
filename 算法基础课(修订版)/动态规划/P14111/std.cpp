#include <iostream>
#include <vector>
#include <algorithm>
#include <climits> // 用于 INT_MAX
using namespace std;

int coinChange(vector<int>& coins, int amount) {
    vector<int> dp(amount + 1, INT_MAX); // 初始化 dp 数组，值为 INT_MAX
    dp[0] = 0; // 基础情况：金额为 0 时需要 0 个硬币

    for (int i = 1; i <= amount; ++i) { // 遍历金额从 1 到 amount
        for (int coin : coins) { // 遍历每种硬币面额
            if (i >= coin && dp[i - coin] != INT_MAX) { 
                dp[i] = min(dp[i], dp[i - coin] + 1); // 转移方程：选择硬币后的最优解
            }
        }
    }

    return dp[amount] == INT_MAX ? -1 : dp[amount]; // 检查是否能凑出目标金额
}

int main() {
    // 输入硬币的种类数
    int n;
    cin >> n;

    // 输入每种硬币的面额
    vector<int> coins(n);
    for (int i = 0; i < n; ++i) {
        cin >> coins[i];
    }

    // 输入目标金额
    int amount;
    cin >> amount;

    // 计算结果并输出
    int result = coinChange(coins, amount);
    cout << result << endl;

    return 0;
}
