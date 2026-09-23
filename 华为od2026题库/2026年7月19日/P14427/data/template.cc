#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    string line;
    getline(cin, line);

    // 去掉字符串两端的引号
    string record;
    if (line.size() >= 2 && line[0] == '"' && line.back() == '"') {
        record = line.substr(1, line.size() - 2);
    } else {
        record = line;
    }

    Solution solution;
    vector<char> res = solution.findRepeatedServiceTypes(record);

    // 按 [r,g,m] 格式输出
    cout << '[';
    for (int i = 0; i < (int)res.size(); i++) {
        if (i) cout << ',';
        cout << res[i];
    }
    cout << ']' << endl;
    return 0;
}
