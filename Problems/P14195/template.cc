#include "foo.cc"
#include <cctype>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

static void skipWs(const string& s, size_t& p) {
    while (p < s.size() && isspace(static_cast<unsigned char>(s[p]))) p++;
}

static void expect(const string& s, size_t& p, char c) {
    skipWs(s, p);
    if (p >= s.size() || s[p] != c) exit(1);
    p++;
}

static string readString(const string& s, size_t& p) {
    skipWs(s, p);
    expect(s, p, '"');
    string out;
    while (p < s.size() && s[p] != '"') {
        if (s[p] == '\\' && p + 1 < s.size()) p++;
        out.push_back(s[p++]);
    }
    expect(s, p, '"');
    return out;
}

static vector<string> parseStringArray(const string& t) {
    size_t p = 0;
    skipWs(t, p);
    expect(t, p, '[');
    vector<string> out;
    while (true) {
        skipWs(t, p);
        if (p < t.size() && t[p] == ']') {
            p++;
            break;
        }
        out.push_back(readString(t, p));
        skipWs(t, p);
        if (p < t.size() && t[p] == ',') {
            p++;
            continue;
        }
        if (p < t.size() && t[p] == ']') {
            p++;
            break;
        }
        exit(1);
    }
    return out;
}

static vector<vector<string>> parsePairArray(const string& t) {
    size_t p = 0;
    skipWs(t, p);
    expect(t, p, '[');
    vector<vector<string>> out;
    while (true) {
        skipWs(t, p);
        if (p < t.size() && t[p] == ']') {
            p++;
            break;
        }
        expect(t, p, '[');
        string a = readString(t, p);
        skipWs(t, p);
        expect(t, p, ',');
        string b = readString(t, p);
        skipWs(t, p);
        expect(t, p, ']');
        out.push_back({a, b});
        skipWs(t, p);
        if (p < t.size() && t[p] == ',') {
            p++;
            continue;
        }
        if (p < t.size() && t[p] == ']') {
            p++;
            break;
        }
        exit(1);
    }
    return out;
}

static pair<string, string> splitTwoTopLevelArrays(const string& line) {
    size_t i = 0;
    while (i < line.size() && isspace(static_cast<unsigned char>(line[i]))) i++;
    if (i >= line.size() || line[i] != '[') exit(1);
    int depth = 0;
    size_t start = i;
    for (; i < line.size(); ++i) {
        char c = line[i];
        if (c == '[')
            depth++;
        else if (c == ']') {
            depth--;
            if (depth == 0) {
                string first = line.substr(start, i - start + 1);
                i++;
                while (i < line.size() && isspace(static_cast<unsigned char>(line[i]))) i++;
                if (i < line.size() && line[i] == ',') i++;
                while (i < line.size() && isspace(static_cast<unsigned char>(line[i]))) i++;
                string second = line.substr(i);
                while (!second.empty() && isspace(static_cast<unsigned char>(second.back()))) second.pop_back();
                return {first, second};
            }
        }
    }
    exit(1);
}

static string jsonEscape(const string& x) {
    string r;
    for (char c : x) {
        if (c == '\\' || c == '"') r.push_back('\\');
        r.push_back(c);
    }
    return r;
}

static void printAns(const vector<string>& ans) {
    cout << '[';
    for (size_t i = 0; i < ans.size(); i++) {
        if (i) cout << ',';
        cout << '"' << jsonEscape(ans[i]) << '"';
    }
    cout << "]\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    getline(cin, line);
    if (line.empty()) return 0;
    while (!line.empty() && isspace(static_cast<unsigned char>(line.front()))) line.erase(line.begin());
    while (!line.empty() && isspace(static_cast<unsigned char>(line.back()))) line.pop_back();
    if (line.empty()) return 0;
    auto pr = splitTwoTopLevelArrays(line);
    vector<string> modules = parseStringArray(pr.first);
    vector<vector<string>> deps = parsePairArray(pr.second);
    Solution sol;
    vector<string> ans = sol.allBuildOrders(modules, deps);
    printAns(ans);
    return 0;
}
