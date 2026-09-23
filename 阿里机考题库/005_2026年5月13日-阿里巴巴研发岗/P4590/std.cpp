#include <iostream>
using namespace std;

// 快速 popcount（GCC 内建）
inline int popcount_ull(unsigned long long x) {
    return __builtin_popcountll(x);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while (T--) {
        long long a, b;     // a: 初始值, b: 目标值
        cin >> a >> b;
        unsigned long long diff = (unsigned long long)(b - a);  // 需增加的值
        int ans = popcount_ull(diff);  // 等于二进制中 1 的个数
        cout << ans << '\n';
    }
    return 0;
}
