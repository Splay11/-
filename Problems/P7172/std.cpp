#include <iostream>
#include <vector>
using namespace std;

// 按题面公式：最高位符号位贡献 -2^(n-1)，其余位按正权
int solve(const vector<int>& bits) {
    int n = (int)bits.size();
    int ans = 0;
    if (bits[0] == 1) {
        ans -= (1 << (n - 1));
    }
    for (int i = 1; i < n; i++) {
        if (bits[i] == 1) {
            ans += (1 << (n - 1 - i));
        }
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> bits(n);
    for (int i = 0; i < n; i++) {
        cin >> bits[i];
    }
    cout << solve(bits) << '\n';
    return 0;
}
