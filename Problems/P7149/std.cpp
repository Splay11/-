#include <iostream>
#include <string>
#include <vector>
using namespace std;

// 用栈解码嵌套的 k[串]
string solve(const string& s) {
    vector<string> strs;
    vector<int> nums;
    string cur;
    int num = 0;
    for (char c : s) {
        if (c >= '0' && c <= '9') {
            // k 可能有多位，例如 300
            num = num * 10 + (c - '0');
        } else if (c == '[') {
            // 进入新一层括号，外层结果先存起来
            strs.push_back(cur);
            nums.push_back(num);
            cur.clear();
            num = 0;
        } else if (c == ']') {
            int k = nums.back();
            nums.pop_back();
            string prev = strs.back();
            strs.pop_back();
            // 内层解码结果重复 k 次，再接到外层后面
            string inner;
            inner.reserve(cur.size() * (size_t)k);
            for (int i = 0; i < k; i++) {
                inner += cur;
            }
            cur = prev + inner;
        } else {
            cur.push_back(c);
        }
    }
    return cur;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    // 不含空格，整行就是编码串
    string s;
    cin >> s;
    cout << solve(s) << '\n';
    return 0;
}
