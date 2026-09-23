#include <bits/stdc++.h>
using namespace std;

const long long MOD = 1000000007LL;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    vector<int> lens(T);
    vector<string> tokens(T);
    int maxL = 0;

    // 读入每组目标编码长度与 token（评测按原题 I/O）
    for (int i = 0; i < T; i++) {
        cin >> lens[i];
        cin >> tokens[i];
        maxL = max(maxL, lens[i]);
    }

    // 预处理阶乘：L 次任意位置插入的序列数恒为 L!
    vector<long long> fact(maxL + 1, 1);
    for (int i = 1; i <= maxL; i++) {
        fact[i] = fact[i - 1] * i % MOD;
    }

    for (int i = 0; i < T; i++) {
        cout << fact[lens[i]] << '\n';
    }

    return 0;
}
