#include <iostream>
#include <string>
#include <vector>
using namespace std;

vector<vector<int>> parseLists(const string& s) {
    string inner = s.substr(1, (int)s.size() - 2);
    vector<vector<int>> lists;
    int n = (int)inner.size();
    int i = 0;
    while (i < n) {
        if (inner[i] == ',') {
            i++;
            continue;
        }
        int j = i + 1;
        while (j < n && inner[j] != '}') j++;
        string body = inner.substr(i + 1, j - i - 1);
        vector<int> cur;
        if (!body.empty()) {
            int x = 0;
            bool inNum = false;
            for (char c : body) {
                if (c == ',') {
                    cur.push_back(x);
                    x = 0;
                    inNum = false;
                } else {
                    x = x * 10 + (c - '0');
                    inNum = true;
                }
            }
            if (inNum) cur.push_back(x);
        }
        lists.push_back(cur);
        i = j + 1;
    }
    return lists;
}

vector<int> mergeRev(const vector<vector<int>>& lists) {
    vector<int> out;
    for (int i = (int)lists.size() - 1; i >= 0; i--) {
        out.insert(out.end(), lists[i].begin(), lists[i].end());
    }
    return out;
}

string formatList(const vector<int>& vals) {
    if (vals.empty()) return "{}";
    string s = "{";
    for (int i = 0; i < (int)vals.size(); i++) {
        if (i) s += ',';
        s += to_string(vals[i]);
    }
    s += '}';
    return s;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    getline(cin, line);
    if (!line.empty() && line.back() == '\r') line.pop_back();
    cout << formatList(mergeRev(parseLists(line))) << '\n';
    return 0;
}
