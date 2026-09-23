#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
using namespace std;

// 解析二维整型数组 [[p,w],[p,w],...]
static vector<vector<int>> parse2DArray(const string& s) {
    vector<vector<int>> res;
    size_t start = s.find('[');
    size_t end = s.rfind(']');
    if (start == string::npos || end == string::npos || end <= start) return res;
    string inner = s.substr(start + 1, end - start - 1);  // 去掉外层 [ ]
    if (inner.empty()) return res;
    size_t pos = 0;
    while (pos < inner.size()) {
        size_t lb = inner.find('[', pos);
        if (lb == string::npos) break;
        size_t rb = inner.find(']', lb);
        string pairStr = inner.substr(lb + 1, rb - lb - 1);  // "p,w"
        size_t comma = pairStr.find(',');
        int p = stoi(pairStr.substr(0, comma));
        int w = stoi(pairStr.substr(comma + 1));
        res.push_back({p, w});
        pos = rb + 1;
    }
    return res;
}

int main() {
    string line;
    getline(cin, line);

    vector<vector<int>> packets = parse2DArray(line);
    vector<int> ans = Solution().findPacket(packets);

    // 按题面样例格式输出：[id1,id2,...]（无空格）
    cout << '[';
    for (size_t i = 0; i < ans.size(); i++) {
        cout << ans[i];
        if (i + 1 < ans.size()) cout << ',';
    }
    cout << ']' << endl;
    return 0;
}
