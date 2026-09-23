#include <iostream>
#include <vector>
using namespace std;

const int MOD = 1000000007;

int main() {
    string s;
    cin >> s;
    int n = s.length();
    
    // dp[i][j] 代表前i+1个字符中以j为结尾的相邻两两不同的子序列个数
    vector<vector<long long>> dp(n, vector<long long>(10, 0));

    // 初始化
    dp[0][s[0] - '0'] = 1;
    
    for (int i = 1; i < n; ++i) {
        long long tot = 0; // 总数
        int now = s[i] - '0'; // 当前字符
        
        // 遍历前一个位置的所有字符
        for (int j = 0; j < 10; ++j) {
            // 如果不是当前字符 . 直接等于上一个字符的个数
            if (j != now) {
                dp[i][j] = dp[i - 1][j];
            }
            tot = (tot + dp[i - 1][j]) % MOD;
        }
        
        // 对于当前字符，我们需要重新计算
        dp[i][now] = (tot - dp[i - 1][now] + 1 + MOD) % MOD;
    }

    // 输出所有结尾位置的子序列个数的和
    long long result = 0;
    for (int j = 0; j < 10; ++j) {
        result = (result + dp[n - 1][j]) % MOD;
    }

    cout << result << endl;
    return 0;
}
