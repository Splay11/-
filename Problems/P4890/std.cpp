#include <bits/stdc++.h>
using namespace std;

string divideByTwo(const string &s) {
    string q;
    int carry = 0;
    for (char ch : s) {
        int cur = carry * 10 + (ch - '0');
        if (!q.empty() || cur / 2 != 0) {
            q.push_back(char('0' + cur / 2));
        }
        carry = cur % 2;
    }
    return q.empty() ? "0" : q;
}

int solve(string n) {
    // 每除以 2 一次，相当于右移一位；除到 0 前的次数就是二进制位数。
    int bits = 0;
    while (n != "0") {
        n = divideByTwo(n);
        ++bits;
    }
    return bits - 1;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string n;
    cin >> n;
    cout << solve(n) << '\n';
    return 0;
}
