#include <algorithm>
#include <cstdlib>
#include <iostream>
using namespace std;

typedef long long ll;

ll mul(ll a, ll b, ll mod) {
    a %= mod;
    b %= mod;
    ll r = 0;
    while (b) {
        if (b & 1) {
            r += a;
            if (r >= mod) r -= mod;
        }
        a += a;
        if (a >= mod) a -= mod;
        b >>= 1;
    }
    return r;
}

ll pow_mod(ll a, ll e, ll mod) {
    ll r = 1 % mod;
    while (e) {
        if (e & 1) r = mul(r, a, mod);
        a = mul(a, a, mod);
        e >>= 1;
    }
    return r;
}

bool is_prime(ll n) {
    if (n < 2) return false;
    static const int small[] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31};
    for (int i = 0; i < 11; i++) {
        if (n % small[i] == 0) return n == small[i];
    }
    ll d = n - 1;
    int s = 0;
    while ((d & 1) == 0) {
        d >>= 1;
        s++;
    }
    static const ll bases[] = {2, 325, 9375, 28178, 450775, 9780504, 1795265022};
    for (int t = 0; t < 7; t++) {
        ll a = bases[t] % n;
        if (a == 0) continue;
        ll x = pow_mod(a, d, n);
        if (x == 1 || x == n - 1) continue;
        bool ok = false;
        for (int i = 0; i < s - 1; i++) {
            x = mul(x, x, n);
            if (x == n - 1) {
                ok = true;
                break;
            }
        }
        if (!ok) return false;
    }
    return true;
}

ll gcd_ll(ll a, ll b) {
    if (a < 0) a = -a;
    while (b) {
        ll t = a % b;
        a = b;
        b = t;
    }
    return a;
}

ll pollard(ll n) {
    if (n % 2 == 0) return 2;
    if (is_prime(n)) return n;
    while (true) {
        ll x = (ll)rand() % (n - 2) + 2;
        ll y = x;
        ll c = (ll)rand() % (n - 1) + 1;
        ll d = 1;
        while (d == 1) {
            x = (mul(x, x, n) + c) % n;
            y = (mul(y, y, n) + c) % n;
            y = (mul(y, y, n) + c) % n;
            d = gcd_ll(x > y ? x - y : y - x, n);
        }
        if (d != n) return d;
    }
}

ll min_prime_factor(ll n) {
    if (n % 2 == 0) return 2;
    if (is_prime(n)) return n;
    ll f = pollard(n);
    return min(min_prime_factor(f), min_prime_factor(n / f));
}

ll smallest_odd_prime_factor(ll n) {
    // 剥掉全部因子 2；只剩 1 则是 2 的幂
    while (n % 2 == 0) n /= 2;
    if (n == 1) return -1;
    return min_prime_factor(n);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    srand(1);
    int q;
    cin >> q;
    for (int i = 0; i < q; i++) {
        ll x;
        cin >> x;
        cout << smallest_odd_prime_factor(x) << '\n';
    }
    return 0;
}
