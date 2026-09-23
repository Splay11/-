#include "foo.cc"
#include <cctype>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

static vector<string> parseStringList(const string& s) {
    size_t i = 0;
    while (i < s.size() && isspace((unsigned char)s[i])) i++;
    if (i >= s.size() || s[i] != '[') exit(1);
    i++;
    vector<string> out;
    while (true) {
        while (i < s.size() && isspace((unsigned char)s[i])) i++;
        if (i < s.size() && s[i] == ']') {
            i++;
            break;
        }
        if (i >= s.size() || s[i] != '"') exit(1);
        i++;
        string cur;
        while (i < s.size() && s[i] != '"') cur += s[i++];
        if (i >= s.size() || s[i] != '"') exit(1);
        i++;
        out.push_back(cur);
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

static void printAns(const vector<int>& ans) {
    cout << "[";
    for (size_t i = 0; i < ans.size(); i++) {
        if (i) cout << ",";
        cout << ans[i];
    }
    cout << "]\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    if (!getline(cin, line)) return 0;
    while (!line.empty() && isspace((unsigned char)line.back())) line.pop_back();
    auto commands = parseStringList(line);
    Solution sol;
    printAns(sol.processPacketCommands(commands));
    return 0;
}
