#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
using namespace std;

static int findTopLevelComma(const string& s) {
    int bracket = 0;
    for (int i = 0; i < (int)s.size(); i++) {
        char c = s[i];
        if (c == '[') bracket++;
        else if (c == ']') bracket--;
        else if (c == ',' && bracket == 0) return i;
    }
    return -1;
}

static vector<vector<int>> parse2DArray(const string& s) {
    vector<vector<int>> res;
    int i = 0, n = (int)s.size();
    // 跳过外层 [
    while (i < n && s[i] != '[') i++;
    i++; // 跳过第一个 [
    while (i < n) {
        while (i < n && s[i] != '[') i++;
        if (i >= n) break;
        i++; // 跳过内层 [
        int t = 0, sign = 1;
        if (s[i] == '-') { sign = -1; i++; }
        while (i < n && isdigit(s[i])) { t = t * 10 + (s[i] - '0'); i++; }
        t *= sign;
        i++; // 跳过逗号
        int v = 0;
        sign = 1;
        if (s[i] == '-') { sign = -1; i++; }
        while (i < n && isdigit(s[i])) { v = v * 10 + (s[i] - '0'); i++; }
        v *= sign;
        res.push_back({t, v});
        i++; // 跳过内层 ]
        if (i < n && s[i] == ']') break; // 遇到外层 ] 结束
    }
    return res;
}

int main() {
    string line;
    getline(cin, line);

    int comma = findTopLevelComma(line);
    string dataStr = line.substr(0, comma);
    int interval = stoi(line.substr(comma + 1));

    vector<vector<int>> data = parse2DArray(dataStr);

    Solution solution;
    vector<int> result = solution.getMaxValues(data, interval);

    cout << "[";
    for (int i = 0; i < (int)result.size(); i++) {
        if (i > 0) cout << ",";
        cout << result[i];
    }
    cout << "]" << endl;
    return 0;
}
