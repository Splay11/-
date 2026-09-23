#include <iostream>
#include <string>
#include <vector>
using namespace std;

// dp[i] 表示前 i 个字符有多少种解码方法
int solve(const string& s) {
    int n = (int)s.size();
    vector<int> dp(n + 1, 0);
    dp[0] = 1;
    for (int i = 1; i <= n; i++) {
        // 单独解码 s[i-1]
        if (s[i - 1] != '0') {
            dp[i] += dp[i - 1];
        }
        if (i >= 2) {
            // 把最后两位当成一个字母，必须是 10..26
            int x = (s[i - 2] - '0') * 10 + (s[i - 1] - '0');
            if (x >= 10 && x <= 26) {
                dp[i] += dp[i - 2];
            }
        }
    }
    return dp[n];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    // 一整行数字串
    string s;
    cin >> s;
    cout << solve(s) << '\n';
    return 0;
}
