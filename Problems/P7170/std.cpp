#include <iostream>
#include <climits>
using namespace std;

// 按位弹出个位接到答案后面；乘 10 前检查 32 位溢出
int solve(int x) {
    int rev = 0;
    while (x != 0) {
        int pop = x % 10;
        x /= 10;
        // 再乘 10 就会超过 INT_MAX
        if (rev > INT_MAX / 10 || (rev == INT_MAX / 10 && pop > 7)) {
            return 0;
        }
        // 再乘 10 就会低于 INT_MIN
        if (rev < INT_MIN / 10 || (rev == INT_MIN / 10 && pop < -8)) {
            return 0;
        }
        rev = rev * 10 + pop;
    }
    return rev;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int x;
    cin >> x;
    cout << solve(x) << '\n';
    return 0;
}
