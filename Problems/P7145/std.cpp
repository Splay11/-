#include <iostream>
#include <string>
#include <vector>
using namespace std;

// 单调栈贪心：每个字母只留一次，字典序尽量小
string solve(const string& s) {
    int last[26];
    for (int k = 0; k < 26; k++) {
        last[k] = -1;
    }
    int n = (int)s.size();
    for (int i = 0; i < n; i++) {
        // 记下每个字母最后一次出现的下标
        last[s[i] - 'a'] = i;
    }
    vector<char> stack;
    bool used[26] = {};
    for (int i = 0; i < n; i++) {
        int x = s[i] - 'a';
        if (used[x]) {
            // 已经选过，不能再出现
            continue;
        }
        while (!stack.empty()) {
            int top = stack.back() - 'a';
            // 栈顶更大且后面还会出现，才能弹掉换更小前缀
            if (stack.back() > s[i] && last[top] > i) {
                used[top] = false;
                stack.pop_back();
            } else {
                break;
            }
        }
        stack.push_back(s[i]);
        used[x] = true;
    }
    return string(stack.begin(), stack.end());
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    // 不含空格，整行就是字符串 s
    string s;
    cin >> s;
    cout << solve(s) << '\n';
    return 0;
}
