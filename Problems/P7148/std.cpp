#include <iostream>
#include <string>
using namespace std;

// 维护未匹配左括号数量的可能区间 [lo, hi]
bool solve(const string& s) {
    int lo = 0;
    int hi = 0;
    for (char c : s) {
        if (c == '(') {
            lo++;
            hi++;
        } else if (c == ')') {
            lo--;
            hi--;
        } else {
            // 星号：当右括号 / 空 / 左括号，区间向两边扩
            lo--;
            hi++;
        }
        if (hi < 0) {
            // 右括号已经多到星号也救不了
            return false;
        }
        if (lo < 0) {
            lo = 0;
        }
    }
    // 扫完后还要能把所有左括号配平
    return lo == 0;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    // 不含空格，整行就是 s
    string s;
    cin >> s;
    cout << (solve(s) ? "true" : "false") << '\n';
    return 0;
}
