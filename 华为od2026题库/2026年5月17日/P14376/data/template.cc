#include <bits/stdc++.h>
using namespace std;

#include "foo.cc"

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // 读取一行 IPv4 地址，保留除换行符以外的原始内容
    string ip;
    getline(cin, ip);
    if (!ip.empty() && ip.back() == '\r') {
        ip.pop_back();
    }

    // 调用用户实现的函数并输出结果
    Solution solution;
    cout << solution.classifyIPv4(ip);

    return 0;
}
