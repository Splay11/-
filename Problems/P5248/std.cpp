#include <bits/stdc++.h>
using namespace std;

const int ODDS[] = {3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41};
const int ODDS_N = 12;

int gcd_int(int a, int b) {
    while (b) {
        int t = a % b;
        a = b;
        b = t;
    }
    return a;
}

bool impossible(int n) {
    return n <= 9 || n == 11 || n == 13 || n == 17;
}

bool solve(int n, int& x, int& y, int& z) {
    if (impossible(n)) {
        return false;
    }
    if (n % 2 == 0) {
        if (n % 6 != 2) {
            x = 2;
            y = 3;
            z = n - 5;
        } else {
            x = 3;
            y = 4;
            z = n - 7;
        }
        return true;
    }
    for (int i = 0; i < ODDS_N; ++i) {
        int a = ODDS[i];
        for (int j = i; j < ODDS_N; ++j) {
            int b = ODDS[j];
            if (gcd_int(a, b) != 1) {
                continue;
            }
            int c = n - a - b;
            if (c >= 2 && gcd_int(a, c) == 1 && gcd_int(b, c) == 1) {
                x = a;
                y = b;
                z = c;
                return true;
            }
        }
    }
    return false;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    while (q--) {
        int n;
        cin >> n;
        int x, y, z;
        if (!solve(n, x, y, z)) {
            cout << -1 << '\n';
        } else {
            cout << x << ' ' << y << ' ' << z << '\n';
        }
    }
    return 0;
}
