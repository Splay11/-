#include <bits/stdc++.h>
using namespace std;

vector<string> MAP = {
    "", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"
};

void dfs(const string &d, int idx, string &path, vector<string> &res) {
    if (idx == d.size()) {
        res.push_back(path);
        return;
    }
    string &letters = MAP[d[idx] - '0'];
    for (char c : letters) {
        path.push_back(c);    // 选择
        dfs(d, idx + 1, path, res);
        path.pop_back();      // 撤销
    }
}

vector<string> comb(const string &digits) {
    vector<string> res;
    if (digits.empty()) return res;
    string path;
    dfs(digits, 0, path, res);
    return res;
}

int main() {
    string s;
    getline(cin, s);
    auto ans = comb(s);
    for (auto &t : ans) {
        cout << t << "\n";
    }
    return 0;
}
