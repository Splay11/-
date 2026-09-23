#include <bits/stdc++.h>
using namespace std;
using int64 = long long;

// 计算不超过 n 的 v 的所有因子
static vector<int64> divisors_leq(int64 v, int64 n) {
    vector<int64> res;
    for (int64 i = 1; i * i <= v; ++i) {
        if (v % i == 0) {
            if (i <= n) res.push_back(i);
            int64 j = v / i;
            if (j != i && j <= n) res.push_back(j);
        }
    }
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n, x, y;
    if (!(cin >> n >> x >> y)) return 0;

    // 先处理 |A ∪ B|
    long long g = std::gcd(x, y);
    __int128 lcm128 = (__int128)(x / g) * y; // lcm 可能达到 1e18，用 __int128 保守计算
    long long both = 0;
    if (lcm128 <= (__int128)n) {
        both = (long long)((__int128)n / lcm128);
    } // 否则 both 保持为 0
    long long M = n / x + n / y - both;

    // 枚举 x 与 y 的因子（不超过 n），去重
    unordered_set<long long> S;
    auto dx = divisors_leq(x, n);
    auto dy = divisors_leq(y, n);
    for (auto d : dx) S.insert(d);
    for (auto d : dy) S.insert(d);

    // 统计需要额外补计的因子（不属于 A ∪ B）
    long long extra = 0;
    for (auto d : S) {
        if (d % x != 0 && d % y != 0) ++extra;
    }

    cout << (M + extra) << "\n";
    return 0;
}
