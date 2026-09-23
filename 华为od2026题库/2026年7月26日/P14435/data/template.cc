#include <iostream>
#include <vector>
#include <string>
using namespace std;
#include "foo.cc"

int main() {
    string s;
    getline(cin, s);

    // 统计 n：数 '[' 的数量减 1（最外层方括号）
    int n = 0;
    for (char c : s) if (c == '[') n++;
    n--;

    vector<vector<int>> grid(n, vector<int>(n));
    int depth = 0, row = 0, col = 0, num = 0;
    bool inNum = false;

    for (char c : s) {
        if (c == '[') {
            depth++;
            if (depth == 2) col = 0;  // 进入新一行，列号归零
        } else if (c == ']') {
            if (inNum) { grid[row][col++] = num; num = 0; inNum = false; }
            if (depth == 2) row++;    // 当前行结束，行号加一
            depth--;
        } else if (c >= '0' && c <= '9') {
            num = num * 10 + (c - '0');
            inNum = true;
        } else if (c == ',' && inNum && depth == 2) {
            // 行内逗号分隔，结算当前数字
            grid[row][col++] = num;
            num = 0; inNum = false;
        }
    }

    Solution sol;
    cout << sol.countMinefields(grid) << endl;
    return 0;
}
