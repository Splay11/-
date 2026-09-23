#include <iostream>
using namespace std;

const long long MOD = 998244353;

// 快速幂：计算 a^e % mod
long long fastPow(long long a, long long e, long long mod) {
    long long res = 1;
    a %= mod;
    while (e > 0) {
        if (e & 1) res = res * a % mod;
        a = a * a % mod;
        e >>= 1;
    }
    return res;
}

long long solve(int m) {
    // 指数 e = 2^m - 1
    long long e = (1LL << m) - 1;
    return fastPow(2, e, MOD);
}

int main() {
    int m;
    cin >> m;
    cout << solve(m) << endl;
    return 0;
}
