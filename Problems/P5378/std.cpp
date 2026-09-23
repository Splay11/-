#include <iostream>
using namespace std;

const int MOD = 1000000007;
const int MAXN = 200000;

// f1/f2/f3：长度为 i、末尾恰好连续 1/2/3 个相同字母的方案数
int f1[MAXN + 1];
int f2[MAXN + 1];
int f3[MAXN + 1];
int ans[MAXN + 1];

void precompute() {
    // 长度为 1：26 种字母，末尾连续段长度只能是 1
    f1[1] = 26;
    ans[1] = 26;
    for (int i = 2; i <= MAXN; i++) {
        // 换一个与末尾不同的字母，连续段变成 1，有 25 种选择
        f1[i] = (int)((f1[i - 1] * 1LL + f2[i - 1] + f3[i - 1]) % MOD * 25 % MOD);
        // 再重复一次末尾字母：只能接在「恰好 1 个」后面
        f2[i] = f1[i - 1];
        // 再重复一次：只能接在「恰好 2 个」后面
        f3[i] = f2[i - 1];
        ans[i] = (int)((f1[i] * 1LL + f2[i] + f3[i]) % MOD);
    }
}

int count_str(int m) {
    return ans[m];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    precompute();
    int q;
    cin >> q;
    while (q--) {
        int m;
        cin >> m;
        cout << count_str(m) << "\n";
    }
    return 0;
}
