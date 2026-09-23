#include <iostream>
#include <string>
using namespace std;

// 用栈消除相邻相同字母
string solve(const string& s) {
    string stack;
    for (char c : s) {
        if (!stack.empty() && stack.back() == c) {
            // 相邻相同，成对删除
            stack.pop_back();
        } else {
            stack.push_back(c);
        }
    }
    return stack;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    // 不含空格，整行就是 s
    string s;
    cin >> s;
    cout << solve(s) << '\n';
    return 0;
}
