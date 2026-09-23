// 偶数长度窗口上 0/1 数量相等：交错串 0101... 一定合法
#include <iostream>
#include <string>
using namespace std;

string buildBalanced01(int k) {
    // 灯位从 1 开始：奇数位放 0，偶数位放 1
    string t;
    t.resize(k);
    for (int i = 1; i <= k; i++) {
        t[i - 1] = (i % 2 == 1) ? '0' : '1';
    }
    return t;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int k, q;
    // 第一行灯带长度，第二行窗口条数
    cin >> k >> q;
    // 窗口写成 a,b，交错串对所有窗口都成立，读掉即可
    for (int i = 0; i < q; i++) {
        int a, b;
        char comma;
        cin >> a >> comma >> b;
    }
    cout << buildBalanced01(k) << "\n";
    return 0;
}
