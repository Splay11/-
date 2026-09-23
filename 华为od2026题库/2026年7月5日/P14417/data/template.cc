#include "foo.cc"
#include <iostream>
#include <string>
using namespace std;

// 解析 JSON 字符串（提取引号内容）
static string parseQuoted(const string& s, int& pos) {
    while (pos < (int)s.size() && s[pos] != '"') pos++;
    pos++;  // 跳过左引号
    string res;
    while (pos < (int)s.size() && s[pos] != '"') {
        if (s[pos] == '\\' && pos + 1 < (int)s.size()) {
            pos++;
            res += s[pos];
        } else {
            res += s[pos];
        }
        pos++;
    }
    pos++;  // 跳过右引号
    return res;
}

int main() {
    string line;
    getline(cin, line);

    int pos = 0;
    string treeLevelOrder = parseQuoted(line, pos);
    string frm = parseQuoted(line, pos);
    string to = parseQuoted(line, pos);

    Solution solution;
    cout << solution.minJumps(treeLevelOrder, frm, to) << endl;
    return 0;
}
