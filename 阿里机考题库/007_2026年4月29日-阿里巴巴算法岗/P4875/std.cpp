#include <bits/stdc++.h>
using namespace std;

const long long MOD = 1000000007LL;

// 计算补全方案数：动态规划，维护最后一段信号字符及其长度的奇偶性
long long countWays(const string& s) {
    // odd[c]：最后一段字符为 c，且长度为奇数的方案数
    // even[c]：最后一段字符为 c，且长度为偶数的方案数
    long long odd[2] = {0, 0};
    long long even[2] = {0, 0};

    // 初始化第一个字符
    for (int c = 0; c < 2; c++) {
        char ch = c == 0 ? 'A' : 'B';
        if (s[0] == '?' || s[0] == ch) {
            odd[c] = 1;
        }
    }

    // 从第二个字符开始动态规划
    for (int i = 1; i < (int)s.size(); i++) {
        long long newOdd[2] = {0, 0};
        long long newEven[2] = {0, 0};

        for (int c = 0; c < 2; c++) {
            char ch = c == 0 ? 'A' : 'B';
            if (s[i] != '?' && s[i] != ch) {
                continue;
            }

            // 继续放相同字符：当前段长度奇偶性翻转
            newOdd[c] = (newOdd[c] + even[c]) % MOD;
            newEven[c] = (newEven[c] + odd[c]) % MOD;

            // 放不同字符：上一段必须是奇数长度才能开启新段
            newOdd[c] = (newOdd[c] + odd[c ^ 1]) % MOD;
        }

        for (int c = 0; c < 2; c++) {
            odd[c] = newOdd[c];
            even[c] = newEven[c];
        }
    }

    // 最后一段必须是奇数长度
    return (odd[0] + odd[1]) % MOD;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int n;
        string s;
        cin >> n >> s;

        cout << countWays(s) << '\n';
    }

    return 0;
}
