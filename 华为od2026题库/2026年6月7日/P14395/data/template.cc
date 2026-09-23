#include "foo.cc"
#include <cctype>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

static vector<string> parseStringArray(const string& s) {
    vector<string> out;
    size_t i = 0;
    while (i < s.size() && isspace((unsigned char)s[i])) i++;
    if (i >= s.size() || s[i] != '[') exit(1);
    i++;
    while (true) {
        while (i < s.size() && isspace((unsigned char)s[i])) i++;
        if (i < s.size() && s[i] == ']') {
            i++;
            break;
        }
        if (i >= s.size() || s[i] != '"') exit(1);
        i++;
        string val;
        while (i < s.size() && s[i] != '"') val += s[i++];
        if (i >= s.size() || s[i] != '"') exit(1);
        i++;
        out.push_back(val);
        while (i < s.size() && isspace((unsigned char)s[i])) i++;
        if (i < s.size() && s[i] == ']') {
            i++;
            break;
        }
        if (i >= s.size() || s[i] != ',') exit(1);
        i++;
    }
    return out;
}

static void printAns(const vector<string>& ans) {
    cout << "[";
    for (size_t i = 0; i < ans.size(); i++) {
        if (i) cout << ",";
        cout << '"' << ans[i] << '"';
    }
    cout << "]\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    if (!getline(cin, line)) return 0;
    while (!line.empty() && isspace((unsigned char)line.back())) line.pop_back();
    vector<string> ips = parseStringArray(line);
    Solution sol;
    printAns(sol.filterValidAClassIPs(ips));
    return 0;
}
