#include "foo.cc"
#include <iostream>
#include <string>
#include <vector>

using namespace std;

static void skipSpace(const string &t, size_t &i) {
    while (i < t.size() && (t[i] == ' ' || t[i] == '\t' || t[i] == '\r' || t[i] == '\n')) {
        ++i;
    }
}

static void parseInput(const string &t, vector<string> &commands, string &prefix) {
    commands.clear();
    prefix.clear();
    size_t i = 0;
    skipSpace(t, i);
    if (i >= t.size() || t[i] != '[') return;
    ++i;
    while (true) {
        skipSpace(t, i);
        if (i < t.size() && t[i] == ']') {
            ++i;
            break;
        }
        if (i >= t.size() || t[i] != '"') return;
        ++i;
        size_t st = i;
        while (i < t.size() && t[i] != '"') ++i;
        commands.push_back(t.substr(st, i - st));
        if (i < t.size() && t[i] == '"') ++i;
        skipSpace(t, i);
        if (i < t.size() && t[i] == ']') {
            ++i;
            break;
        }
        if (i < t.size() && t[i] == ',') {
            ++i;
            continue;
        }
        return;
    }
    skipSpace(t, i);
    if (i >= t.size() || t[i] != ',') return;
    ++i;
    skipSpace(t, i);
    if (i >= t.size() || t[i] != '"') return;
    ++i;
    size_t st = i;
    while (i < t.size() && t[i] != '"') ++i;
    prefix = t.substr(st, i - st);
}

static string formatOutput(const vector<string> &ans) {
    string o = "[";
    for (size_t k = 0; k < ans.size(); ++k) {
        if (k) o += ",";
        o += "\"";
        o += ans[k];
        o += "\"";
    }
    o += "]";
    return o;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string input((istreambuf_iterator<char>(cin)), istreambuf_iterator<char>());
    vector<string> commands;
    string prefix;
    parseInput(input, commands, prefix);
    Solution solution;
    vector<string> ans = solution.FindNextKeywords(commands, prefix);
    cout << formatOutput(ans) << "\n";
    return 0;
}
