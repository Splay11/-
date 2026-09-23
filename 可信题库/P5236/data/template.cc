#include "foo.cc"
#include <cctype>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

static string readAll() {
    string all, chunk;
    while (getline(cin, chunk)) all += chunk;
    while (!all.empty() && isspace((unsigned char)all.back())) all.pop_back();
    return all;
}

static void skipSpace(const string& s, size_t& i) {
    while (i < s.size() && isspace((unsigned char)s[i])) i++;
}

static int readInt(const string& s, size_t& i) {
    skipSpace(s, i);
    int sign = 1;
    if (i < s.size() && s[i] == '-') {
        sign = -1;
        i++;
    }
    long long v = 0;
    bool ok = false;
    while (i < s.size() && isdigit((unsigned char)s[i])) {
        ok = true;
        v = v * 10 + (s[i++] - '0');
    }
    if (!ok) exit(1);
    return (int)(sign * v);
}

static string readQuoted(const string& s, size_t& i) {
    skipSpace(s, i);
    if (i >= s.size() || s[i] != '"') exit(1);
    i++;
    string out;
    while (i < s.size() && s[i] != '"') {
        if (s[i] == '\\' && i + 1 < s.size()) {
            out.push_back(s[i + 1]);
            i += 2;
        } else
            out.push_back(s[i++]);
    }
    if (i >= s.size() || s[i] != '"') exit(1);
    i++;
    return out;
}

static vector<Cell> parseTable(const string& s) {
    size_t i = 0;
    skipSpace(s, i);
    if (i >= s.size() || s[i] != '[') exit(1);
    i++;
    vector<Cell> table;
    while (true) {
        skipSpace(s, i);
        if (i < s.size() && s[i] == ']') {
            i++;
            break;
        }
        if (i >= s.size() || s[i] != '[') exit(1);
        i++;
        int r = readInt(s, i);
        skipSpace(s, i);
        if (i >= s.size() || s[i] != ',') exit(1);
        i++;
        int c = readInt(s, i);
        skipSpace(s, i);
        if (i >= s.size() || s[i] != ',') exit(1);
        i++;
        string content = readQuoted(s, i);
        skipSpace(s, i);
        if (i >= s.size() || s[i] != ']') exit(1);
        i++;
        table.push_back(Cell(r, c, content));
        skipSpace(s, i);
        if (i < s.size() && s[i] == ']') {
            i++;
            break;
        }
        if (i >= s.size() || s[i] != ',') exit(1);
        i++;
    }
    return table;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string all = readAll();
    if (all.empty()) return 0;
    auto table = parseTable(all);
    Solution sol;
    auto ans = sol.transformTable(table);
    cout << '[';
    for (size_t i = 0; i < ans.size(); i++) {
        if (i) cout << ',';
        cout << '"';
        for (char ch : ans[i]) {
            if (ch == '\\' || ch == '"') cout << '\\';
            cout << ch;
        }
        cout << '"';
    }
    cout << "]\n";
    return 0;
}
