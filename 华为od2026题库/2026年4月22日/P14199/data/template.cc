#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
using namespace std;

// 去掉首尾空白字符，包括空格、\r、\n、\t
static string trim(const string& s) {
    int l = 0, r = (int)s.size() - 1;

    while (l <= r && (s[l] == ' ' || s[l] == '\r' || s[l] == '\n' || s[l] == '\t')) {
        l++;
    }

    while (l <= r && (s[r] == ' ' || s[r] == '\r' || s[r] == '\n' || s[r] == '\t')) {
        r--;
    }

    if (l > r) return "";
    return s.substr(l, r - l + 1);
}

int main() {
    string line;
    getline(cin, line);

    // 先去掉可能存在的 \r、空格等
    line = trim(line);

    // 再去掉题面输入中的外层双引号
    if (line.size() >= 2 && line[0] == '"' && line[(int)line.size() - 1] == '"') {
        line = line.substr(1, line.size() - 2);
    }

    Solution solution;
    vector<int> ans = solution.timeClassification(line);

    // 严格输出 [a,b,c]，不能有空格
    cout << "[";
    for (int i = 0; i < (int)ans.size(); i++) {
        if (i > 0) cout << ",";
        cout << ans[i];
    }
    cout << "]";

    return 0;
}
