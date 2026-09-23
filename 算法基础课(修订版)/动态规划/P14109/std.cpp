#include <iostream>
#include <algorithm>
using namespace std;

int main() {
    int n;
    cin >> n;  // 输入序列长度
    int a[n];
    for (int i = 0; i < n; ++i) {
        cin >> a[i];  // 输入序列的每个元素
    }

    // 初始化 dp 数组
    int dp[n];
    dp[0] = a[0];  // 第一个元素的最大子段和就是它本身
    int max_sum = a[0];  // 最大子段和

    // 动态规划计算 dp 数组
    for (int i = 1; i < n; ++i) {
        dp[i] = max(dp[i - 1] + a[i], a[i]);  // 状态转移方程
        max_sum = max(max_sum, dp[i]);  // 更新最大子段和
    }

    cout << max_sum << endl;  // 输出最大子段和
    return 0;
}
