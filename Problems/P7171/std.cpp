#include <iostream>
using namespace std;

long long gcd(long long a, long long b) {
    // 辗转相除求最大公约数
    while (b) {
        long long t = a % b;
        a = b;
        b = t;
    }
    return a;
}

// 1..n 的最小公倍数：每步 lcm(ans, i) = ans / gcd * i
long long solve(int n) {
    long long ans = 1;
    for (int i = 1; i <= n; i++) {
        long long g = gcd(ans, i);
        ans = ans / g * i;
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    cout << solve(n) << '\n';
    return 0;
}
