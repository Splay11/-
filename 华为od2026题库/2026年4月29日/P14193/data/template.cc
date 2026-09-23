#include <bits/stdc++.h>
#include "foo.cc"
using namespace std;

class Parser {
public:
    string s;
    int i;

    Parser(const string& str) {
        s = str;
        i = 0;
    }

    void skip() {
        while (i < (int)s.size() && isspace((unsigned char)s[i])) {
            i++;
        }
    }

    string parseString() {
        skip();

        // 跳过左双引号
        if (i < (int)s.size() && s[i] == '"') {
            i++;
        }

        string res;

        while (i < (int)s.size()) {
            char c = s[i++];

            if (c == '\\') {
                // 处理转义字符
                if (i < (int)s.size()) {
                    res.push_back(s[i++]);
                }
            } else if (c == '"') {
                // 读到右双引号，字符串结束
                break;
            } else {
                res.push_back(c);
            }
        }

        return res;
    }

    vector<vector<string>> parse() {
        vector<vector<string>> res;

        skip();

        // 跳过最外层左中括号
        if (i < (int)s.size() && s[i] == '[') {
            i++;
        }

        while (i < (int)s.size()) {
            skip();

            if (i >= (int)s.size()) {
                break;
            }

            // 最外层数组结束
            if (s[i] == ']') {
                i++;
                break;
            }

            // 跳过逗号
            if (s[i] == ',') {
                i++;
                continue;
            }

            vector<string> one;

            // 跳过单条命令的左中括号
            if (s[i] == '[') {
                i++;
            }

            while (i < (int)s.size()) {
                skip();

                // 当前命令数组结束
                if (i < (int)s.size() && s[i] == ']') {
                    i++;
                    break;
                }

                // 跳过逗号
                if (i < (int)s.size() && s[i] == ',') {
                    i++;
                    continue;
                }

                // 读取字符串
                if (i < (int)s.size() && s[i] == '"') {
                    one.push_back(parseString());
                } else {
                    // 非预期字符，跳过，防止死循环
                    i++;
                }
            }

            res.push_back(one);
        }

        return res;
    }
};

string escapeJsonString(const string& str) {
    string res;

    for (char c : str) {
        if (c == '\\') {
            res += "\\\\";
        } else if (c == '"') {
            res += "\\\"";
        } else if (c == '\n') {
            res += "\\n";
        } else if (c == '\r') {
            res += "\\r";
        } else if (c == '\t') {
            res += "\\t";
        } else {
            res.push_back(c);
        }
    }

    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string input;
    string line;

    while (getline(cin, line)) {
        input += line;
    }

    Parser parser(input);
    vector<vector<string>> command = parser.parse();

    Solution solution;
    string ans = solution.execute_command(command);

    // 字符串输出统一加双引号
    cout << "\"" << escapeJsonString(ans) << "\"";

    return 0;
}
