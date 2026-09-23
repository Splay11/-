#include <iostream>
using namespace std;

// 负数不是回文；翻转后半段数字再和前半段比较，避免整型溢出
bool solve(int x) {
    if (x < 0) {
        return false;
    }
    if (x != 0 && x % 10 == 0) {
        return false;
    }
    int rev = 0;
    while (x > rev) {
        rev = rev * 10 + x % 10;
        x /= 10;
    }
    // 偶数位两半相等；奇数位丢掉中间那位
    return x == rev || x == rev / 10;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int x;
    cin >> x;
    cout << (solve(x) ? "true" : "false") << '\n';
    return 0;
}
