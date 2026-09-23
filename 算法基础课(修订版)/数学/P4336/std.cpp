#include <bits/stdc++.h>
using namespace std;

long long GCD(long long x, long long y) {
    // 辗转相除法
    while (y) {
        long long t = x % y;
        x = y;
        y = t;
    }
    return x;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long a, b, c, d;
    // 读取四个正整数
    if (!(cin >> a >> b >> c >> d)) return 0;

    // 比例完全匹配：无空白
    if (a * d == b * c) {
        cout << "0/1\n";
        return 0;
    }

    long long p, q; // 画作占屏幕面积的分子与分母
    if (a * d > b * c) {
        // 屏幕更宽：以高贴合
        p = c * b;
        q = a * d;
    } else {
        // 屏幕更窄：以宽贴合
        p = a * d;
        q = b * c;
    }

    // 空白面积比例 = (q - p) / q，最后约分
    long long num = q - p, den = q;
    long long g = GCD(num, den);
    num /= g; den /= g;

    cout << num << "/" << den << "\n";
    return 0;
}
