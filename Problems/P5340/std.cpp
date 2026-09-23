#include <iostream>
#include <vector>
using namespace std;

// 由序号构造前半段，镜像成回文后再转成十进制
long long kth_palindrome(int r, int n, int t) {
    // 前半段长度：奇数时中间那一位也算在前半段里
    int h = (n + 1) / 2;
    vector<int> half(h, 0);
    long long x = t - 1;
    // 从右往左填前半段的低位，每一位都是 0 到 r-1
    for (int i = h - 1; i > 0; i--) {
        half[i] = (int)(x % r);
        x /= r;
    }
    // 最高位不能为 0，所以在余下的数上再加 1
    half[0] = (int)x + 1;
    vector<int> digits(n, 0);
    // 左右对称写下完整的 n 位
    for (int i = 0; i < h; i++) {
        digits[i] = half[i];
        digits[n - 1 - i] = half[i];
    }
    long long val = 0;
    // 按 r 进制 Horner 法则转成十进制
    for (int i = 0; i < n; i++) {
        val = val * r + digits[i];
    }
    return val;
}

int main() {
    int r, n, t;
    cin >> r >> n >> t;
    cout << kth_palindrome(r, n, t) << endl;
    return 0;
}
