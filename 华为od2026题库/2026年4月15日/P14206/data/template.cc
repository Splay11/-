// HydroOJ 函数题模式 C++ 模板文件
// 说明：
// 1. 本文件负责输入解析、调用用户实现的函数、输出结果
// 2. 用户需要在 user.cc 中实现 Solution 类的 mergeLogs 方法
// 3. 输入格式示例：
//    ["/api/user","/api/user","/api/order"],[100,200,150]

#include <bits/stdc++.h>
#include "foo.cc"
using namespace std;
// 声明用户实现的 Solution 类（只声明，不实现）

// 解析字符串数组，例如：["/a","/b","/c"]
static vector<string> parseStringArray(const string& s) {
    vector<string> result;
    int n = (int)s.size();
    int i = 0;

    // 跳过空白
    while (i < n && isspace((unsigned char)s[i])) {
        i++;
    }

    // 跳过左括号
    if (i < n && s[i] == '[') {
        i++;
    }

    while (i < n) {
        // 跳过空白和逗号
        while (i < n && (isspace((unsigned char)s[i]) || s[i] == ',')) {
            i++;
        }

        // 遇到右括号结束
        if (i < n && s[i] == ']') {
            break;
        }

        // 解析一个字符串
        if (i < n && s[i] == '"') {
            i++;
            string cur;

            while (i < n) {
                char c = s[i];

                // 处理转义字符
                if (c == '\\' && i + 1 < n) {
                    char next = s[i + 1];
                    if (next == '"' || next == '\\' || next == '/') {
                        cur.push_back(next);
                        i += 2;
                    } else if (next == 'n') {
                        cur.push_back('\n');
                        i += 2;
                    } else if (next == 't') {
                        cur.push_back('\t');
                        i += 2;
                    } else if (next == 'r') {
                        cur.push_back('\r');
                        i += 2;
                    } else {
                        cur.push_back(next);
                        i += 2;
                    }
                } else if (c == '"') {
                    i++;
                    break;
                } else {
                    cur.push_back(c);
                    i++;
                }
            }

            result.push_back(cur);
        } else {
            // 容错处理
            i++;
        }
    }

    return result;
}

// 解析整数数组，例如：[100,200,150]
static vector<int> parseIntArray(string s) {
    vector<int> result;

    // 去掉首尾空白
    int l = 0, r = (int)s.size() - 1;
    while (l <= r && isspace((unsigned char)s[l])) {
        l++;
    }
    while (r >= l && isspace((unsigned char)s[r])) {
        r--;
    }

    if (l > r) {
        return result;
    }

    s = s.substr(l, r - l + 1);
    if (s == "[]") {
        return result;
    }

    // 去掉首尾方括号
    if (!s.empty() && s.front() == '[') {
        s.erase(s.begin());
    }
    if (!s.empty() && s.back() == ']') {
        s.pop_back();
    }

    // 将逗号替换为空格，再用输入流读取整数
    for (char& c : s) {
        if (c == ',') {
            c = ' ';
        }
    }

    stringstream ss(s);
    int x;
    while (ss >> x) {
        result.push_back(x);
    }

    return result;
}

// 将整体输入拆成两个数组片段
static pair<string, string> splitTwoParts(const string& input) {
    int n = (int)input.size();
    int level = 0;
    bool inString = false;
    int splitPos = -1;

    for (int i = 0; i < n; i++) {
        char c = input[i];

        // 处理字符串中的转义，避免误判引号
        if (c == '\\' && inString && i + 1 < n) {
            i++;
            continue;
        }

        if (c == '"') {
            inString = !inString;
        } else if (!inString) {
            if (c == '[') {
                level++;
            } else if (c == ']') {
                level--;
            } else if (c == ',' && level == 0) {
                splitPos = i;
                break;
            }
        }
    }

    if (splitPos == -1) {
        return {"[]", "[]"};
    }

    string part1 = input.substr(0, splitPos);
    string part2 = input.substr(splitPos + 1);
    return {part1, part2};
}

// 格式化输出二维数组
static string format2DIntArray(const vector<vector<int>>& arr) {
    stringstream out;
    out << "[";

    for (int i = 0; i < (int)arr.size(); i++) {
        if (i > 0) {
            out << ",";
        }
        out << "[";
        for (int j = 0; j < (int)arr[i].size(); j++) {
            if (j > 0) {
                out << ",";
            }
            out << arr[i][j];
        }
        out << "]";
    }

    out << "]";
    return out.str();
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // 读取全部输入
    string line;
    string input;
    while (getline(cin, line)) {
        input += line;
    }

    auto parts = splitTwoParts(input);
    vector<string> paths = parseStringArray(parts.first);
    vector<int> responseTimes = parseIntArray(parts.second);
    Solution solution;
    // 调用用户实现
    vector<vector<int>> ans = solution.mergeLogs(paths, responseTimes);


    // 输出结果
    cout << format2DIntArray(ans);
    return 0;
}
