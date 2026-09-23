#include "foo.cc"
#include <iostream>
#include <string>
using namespace std;

int main() {
    string s;
    getline(cin, s);

    // 去掉首尾空白
    while (!s.empty() && (s.back() == '\n' || s.back() == '\r' || s.back() == ' ' || s.back() == '\t')) s.pop_back();
    int l = 0, r = (int)s.size() - 1;
    while (l <= r && (s[l] == ' ' || s[l] == '\t')) l++;
    s = s.substr(l, r - l + 1);

    // 兼容输入带双引号的情况，如 "uuuua"
    if (s.size() >= 2 && s.front() == '"' && s.back() == '"') {
        s = s.substr(1, s.size() - 2);
    }

    Solution solution;
    auto ans = solution.countKeys(s);

    cout << "[";
    for (int i = 0; i < (int)ans.size(); i++) {
        if (i > 0) cout << ",";
        cout << "[" << ans[i][0] << "," << ans[i][1] << "]";
    }
    cout << "]";
    return 0;
}
