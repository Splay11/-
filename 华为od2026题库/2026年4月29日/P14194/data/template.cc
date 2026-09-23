#include "foo.cc"
#include <bits/stdc++.h>
using namespace std;

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

static void printStringList(const vector<string>& a) {
    cout << "[";
    for (int i = 0; i < (int)a.size(); i++) {
        if (i > 0) cout << ",";
        cout << "\"" << a[i] << "\"";
    }
    cout << "]";
}

int main() {
    string line;
    getline(cin, line);

    vector<string> logs = parseStringList(line);

    Solution solution;
    vector<string> ans = solution.findAnomalyLogs(logs);

    if (ans.empty()) {
        cout << "NONE";
    } else {
        printStringList(ans);
    }
    return 0;
}
