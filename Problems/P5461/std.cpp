#include <iostream>
using namespace std;

// 0 到 n 的连续异或。n<0 时为空区间，返回 0
int xor_pref(int n) {
    if (n < 0) {
        return 0;
    }
    // 连续整数异或每 4 个一循环：n, 1, n+1, 0
    int r = n % 4;
    if (r == 0) {
        return n;
    }
    if (r == 1) {
        return 1;
    }
    if (r == 2) {
        return n + 1;
    }
    return 0;
}

// 找最小 q>=p 使得 p⊕...⊕q = w；不存在返回 -1
int min_right(int p, int w) {
    int need = w ^ xor_pref(p - 1);
    // 前缀异或只能取到：0、1、模 4 余 0 的数、模 4 余 3 的数
    if (need == 0) {
        if (p == 0) {
            return 0;
        }
        return p + (3 - p % 4) % 4;
    }
    if (need == 1) {
        return p + (1 - p % 4) % 4;
    }
    if (need % 4 == 0) {
        return (need >= p) ? need : -1;
    }
    if (need % 4 == 3) {
        int q = need - 1;
        return (q >= p) ? q : -1;
    }
    return -1;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    // 四级协议：第一行校验字 w，第二行左端点 p
    int w, p;
    cin >> w >> p;
    cout << min_right(p, w) << '\n';
    return 0;
}
