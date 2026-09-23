#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
using namespace std;

// 解析 JSON 字符串列表，如 ["a","b","c"]
static vector<string> parseStringList(const string& s) {
    vector<string> res;
    string cur;
    bool inString = false;
    for (char c : s) {
        if (c == '"') {
            if (inString) {
                res.push_back(cur);
                cur.clear();
            }
            inString = !inString;
        } else if (inString) {
            cur += c;
        }
    }
    return res;
}

int main() {
    string line;
    getline(cin, line);

    vector<string> versions = parseStringList(line);

    Solution solution;
    string result = solution.findLatestVersion(versions);
    cout << "\"" << result << "\"" << endl;
    return 0;
}
