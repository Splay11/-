#include <iostream>
#include <string>
#include <vector>
using namespace std;

// 用栈按段处理 Unix 路径
string solve(const string& path) {
    vector<string> stack;
    int n = (int)path.size();
    int i = 0;
    while (i < n) {
        // 跳过斜杠，连续多个 / 只当一个
        while (i < n && path[i] == '/') {
            i++;
        }
        if (i >= n) {
            break;
        }
        int j = i;
        while (j < n && path[j] != '/') {
            j++;
        }
        string part = path.substr(i, j - i);
        i = j;
        if (part == ".") {
            // 当前目录，忽略
            continue;
        }
        if (part == "..") {
            // 已经在根目录时不能再往上走
            if (!stack.empty()) {
                stack.pop_back();
            }
        } else {
            // ... 等其他名字都是普通目录
            stack.push_back(part);
        }
    }
    if (stack.empty()) {
        return "/";
    }
    string ans;
    for (int k = 0; k < (int)stack.size(); k++) {
        ans.push_back('/');
        ans += stack[k];
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    // 路径不含空格，整行就是一个绝对路径
    string path;
    cin >> path;
    // 输出规范路径，末尾换行
    cout << solve(path) << '\n';
    return 0;
}
