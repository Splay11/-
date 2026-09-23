#include <iostream>
#include <string>
#include <vector>
using namespace std;

bool can_clear(const string& s) {
    // 每次核销都同时去掉一个 0 和一个 1
    // 只要两种字符都还在，串里一定存在相邻的 01 或 10
    // 所以能删空当且仅当 0 和 1 的个数相等
    int c0 = 0, c1 = 0;
    for (size_t i = 0; i < s.size(); i++) {
        if (s[i] == '0') {
            c0++;
        } else {
            c1++;
        }
    }
    return c0 == c1;
}

int count_clearable(const vector<string>& strs) {
    int ans = 0;
    for (size_t i = 0; i < strs.size(); i++) {
        if (can_clear(strs[i])) {
            ans++;
        }
    }
    return ans;
}

int main() {
    // 总长度可能到 500000，关闭同步以免读入超时
    ios::sync_with_stdio(false);
    cin.tie(0);
    int m;
    cin >> m;
    vector<string> strs(m);
    for (int i = 0; i < m; i++) {
        cin >> strs[i];
    }
    cout << count_clearable(strs) << endl;
    return 0;
}
