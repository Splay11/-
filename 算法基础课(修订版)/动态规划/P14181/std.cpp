#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
using namespace std;

int main() {
    int t;
    cin >> t;  // 读取测试用例数量
    vector<long long> results;  // 使用 long long 存储结果

    while (t--) {
        int n, k;
        cin >> n >> k;  // 读取每个测试用例的n和k
        
        vector<int> a(n);
        for (int i = 0; i < n; ++i) {
            cin >> a[i];  // 读取数组a
        }

        // 初始化必要的变量
        const long long MIN_VALUE = 0-1e18;
        vector<long long> dp(n + 2, MIN_VALUE);   // 用于存储最大子段和的数组
        vector<long long> pre(n + 2, MIN_VALUE);  // 前缀最大值
        vector<long long> udp(n + 2, MIN_VALUE);  // 后缀最大值
        vector<long long> suf(n + 2, MIN_VALUE);  // 存储最大后缀值

        // 计算最大子段和（前缀）
        for (int i = 1; i <= n; ++i) {
            dp[i] = max((long long)a[i - 1], dp[i - 1] + a[i - 1]);
        }

        // 计算最大子段和的前缀最大值
        for (int i = 1; i <= n; ++i) {
            pre[i] = max(dp[i], pre[i - 1]);
        }

        // 计算最大子段和（后缀）
        for (int i = n; i >= 1; --i) {
            udp[i] = max((long long)a[i - 1], udp[i + 1] + a[i - 1]);
        }

        // 计算最大子段和（后缀部分）
        for (int i = n; i >= 1; --i) {
            suf[i] = max(suf[i + 1], udp[i]);
        }

        // 计算最终结果
        long long res = MIN_VALUE;
        for (int i = 1; i <= n - k; ++i) {
            res = max(res, pre[i] + suf[i + k + 1]);
        }

        results.push_back(res);  // 将结果保存
    }

    // 输出所有结果
    for (long long result : results) {
        cout << result << endl;
    }

    return 0;
}
