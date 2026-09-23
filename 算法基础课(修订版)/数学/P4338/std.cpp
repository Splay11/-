#include <iostream>
using namespace std;

const long long MOD = 998244353LL;

// 快速幂：计算 a^b % MOD
long long qpow(long long a, long long b) {
    long long res = 1;
    a %= MOD;
    while (b > 0) {
        if (b & 1) {
            res = res * a % MOD;
        }
        a = a * a % MOD;
        b >>= 1;
    }
    return res;
}

// 计算长度为 n 的所有数字的洞数总和
long long solve(long long n) {
    // 特判：n=1 时，0 也算一个一位数
    if (n == 1) {
        return 6;
    }
    // n>=2 时使用推导公式
    long long part = qpow(10, n - 2);
    long long temp = (54 * (n % MOD) - 4 + MOD) % MOD;
    return part * temp % MOD;
}

int main() {
    int T;
    cin >> T;
    while (T--) {
        long long n;
        cin >> n;
        cout << solve(n) << '\n';
    }
    return 0;
}
