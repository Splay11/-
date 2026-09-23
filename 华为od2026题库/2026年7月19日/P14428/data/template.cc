#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
#include <cctype>
using namespace std;

// 返回从 start 处的 '[' 匹配的 ']' 的下标
static int matchBracket(const string& s, int start) {
    int depth = 0;
    for (int i = start; i < (int)s.size(); i++) {
        if (s[i] == '[') depth++;
        else if (s[i] == ']') {
            depth--;
            if (depth == 0) return i;
        }
    }
    return -1;
}

// 解析形如 [1, 2, -3] 的一维整型数组（忽略空格与括号）
static vector<int> parse1D(const string& s) {
    vector<int> res;
    int i = 0, n = (int)s.size();
    while (i < n) {
        if ((s[i] == '-' && i + 1 < n && isdigit((unsigned char)s[i + 1])) || isdigit((unsigned char)s[i])) {
            int sign = 1;
            if (s[i] == '-') { sign = -1; i++; }
            long long val = 0;
            while (i < n && isdigit((unsigned char)s[i])) { val = val * 10 + (s[i] - '0'); i++; }
            res.push_back((int)(sign * val));
        } else {
            i++;
        }
    }
    return res;
}

int main() {
    string line;
    getline(cin, line);

    // warehouses：第一个 [...] 数组
    int p1 = (int)line.find('[');
    int e1 = matchBracket(line, p1);
    vector<int> warehouses = parse1D(line.substr(p1, e1 - p1 + 1));

    // queries：第二个 [[...]] 数组，逐个内层 [..] 解析
    int p2 = (int)line.find('[', e1 + 1);
    int e2 = matchBracket(line, p2);
    string queriesStr = line.substr(p2, e2 - p2 + 1);
    vector<vector<int>> queries;
    int m = (int)queriesStr.size();
    int j = 1; // 跳过最外层 '['
    while (j < m) {
        if (queriesStr[j] == '[') {
            int k = matchBracket(queriesStr, j);
            queries.push_back(parse1D(queriesStr.substr(j, k - j + 1)));
            j = k + 1;
        } else {
            j++;
        }
    }

    // 末尾整数 numOfWarehouse
    int numOfWarehouse = stoi(line.substr(e2 + 1));

    Solution solution;
    vector<vector<int>> res = solution.getWarehouseReport(warehouses, queries, numOfWarehouse);

    // 紧凑输出 [[..],[..]]
    string out = "[";
    for (int a = 0; a < (int)res.size(); a++) {
        if (a) out += ",";
        out += "[";
        for (int b = 0; b < (int)res[a].size(); b++) {
            if (b) out += ",";
            out += to_string(res[a][b]);
        }
        out += "]";
    }
    out += "]";
    cout << out << endl;
    return 0;
}
