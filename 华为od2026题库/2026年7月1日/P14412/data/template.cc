#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
using namespace std;

static vector<int> parseIntList(const string& s) {
    vector<int> res;
    int cur = 0;
    bool neg = false;
    bool hasNum = false;
    for (char c : s) {
        if (c == '-') {
            neg = true;
        } else if (c >= '0' && c <= '9') {
            cur = cur * 10 + (c - '0');
            hasNum = true;
        } else if (c == ',' || c == ']') {
            if (hasNum) {
                res.push_back(neg ? -cur : cur);
                cur = 0;
                neg = false;
                hasNum = false;
            }
        }
    }
    return res;
}

int main() {
    string line;
    getline(cin, line);

    // 解析数组 "[a1,a2,...,an]"
    vector<int> items = parseIntList(line);

    Solution solution;
    vector<int> result = solution.warehouseInventory(items);

    // 输出格式：[id1,id2,...]
    cout << "[";
    for (int i = 0; i < (int)result.size(); ++i) {
        if (i > 0) cout << ",";
        cout << result[i];
    }
    cout << "]" << endl;
    return 0;
}
