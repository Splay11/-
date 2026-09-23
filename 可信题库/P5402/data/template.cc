#include "foo.cc"
#include <cctype>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

static string trim(const string& s) {
    size_t a = 0;
    while (a < s.size() && isspace((unsigned char)s[a])) a++;
    size_t b = s.size();
    while (b > a && isspace((unsigned char)s[b - 1])) b--;
    return s.substr(a, b - a);
}

static vector<vector<string>> parseBoard(const string& line) {
    string s = trim(line);
    size_t i = 0;
    if (i >= s.size() || s[i] != '[') exit(1);
    i++;
    vector<vector<string>> board;
    while (i < s.size()) {
        while (i < s.size() && (isspace((unsigned char)s[i]) || s[i] == ',')) i++;
        if (i < s.size() && s[i] == ']') break;
        if (i >= s.size() || s[i] != '[') exit(1);
        i++;
        vector<string> row;
        while (i < s.size()) {
            while (i < s.size() && (isspace((unsigned char)s[i]) || s[i] == ',')) i++;
            if (i < s.size() && s[i] == ']') {
                i++;
                break;
            }
            if (i >= s.size() || s[i] != '"') exit(1);
            i++;
            string cell;
            while (i < s.size() && s[i] != '"') cell += s[i++];
            if (i >= s.size()) exit(1);
            i++;
            row.push_back(cell);
        }
        board.push_back(row);
    }
    return board;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string l1, l2;
    if (!getline(cin, l1)) return 0;
    if (!getline(cin, l2)) l2 = "[]";
    auto tray = parseBoard(l1);
    auto stamp = parseBoard(l2);
    vector<int> ans = Solution().findStampPos(tray, stamp);
    int r = ans.size() >= 2 ? ans[0] : -1;
    int c = ans.size() >= 2 ? ans[1] : -1;
    cout << "[" << r << ", " << c << "]\n";
    return 0;
}
