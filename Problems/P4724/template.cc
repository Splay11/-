#include "foo.cc"
#include <iostream>
#include <string>
#include <vector>
using namespace std;

static string parseLeadingQuotedString(const string& s, size_t& pos) {
    string out;
    if (pos >= s.size() || s[pos] != '"') return out;
    ++pos;
    while (pos < s.size()) {
        char c = s[pos++];
        if (c == '\\') {
            if (pos < s.size()) out += s[pos++];
        } else if (c == '"') {
            break;
        } else {
            out += c;
        }
    }
    return out;
}

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

static bool splitTwoTopArrays(const string& rest, string& first, string& second) {
    size_t i = 0;
    while (i < rest.size() && (rest[i] == ' ' || rest[i] == '\t')) ++i;
    if (i >= rest.size() || rest[i] != '[') return false;
    int depth = 0;
    bool inStr = false;
    bool esc = false;
    for (; i < rest.size(); ++i) {
        char c = rest[i];
        if (esc) {
            esc = false;
            continue;
        }
        if (inStr) {
            if (c == '\\') {
                esc = true;
                continue;
            }
            if (c == '"') inStr = false;
            continue;
        }
        if (c == '"') {
            inStr = true;
            continue;
        }
        if (c == '[')
            ++depth;
        else if (c == ']') {
            --depth;
            if (depth == 0) {
                first = rest.substr(0, i + 1);
                size_t j = i + 1;
                while (j < rest.size() && (rest[j] == ' ' || rest[j] == '\t')) ++j;
                if (j >= rest.size() || rest[j] != ',') return false;
                ++j;
                while (j < rest.size() && (rest[j] == ' ' || rest[j] == '\t')) ++j;
                second = rest.substr(j);
                return true;
            }
        }
    }
    return false;
}

static vector<int> parseIntList(const string& s) {
    vector<int> res;
    size_t i = 0;
    while (i < s.size() && (s[i] == ' ' || s[i] == '\t')) ++i;
    if (i >= s.size() || s[i] != '[') return res;
    ++i;
    while (i < s.size()) {
        while (i < s.size() && (s[i] == ' ' || s[i] == '\t' || s[i] == ',')) {
            if (s[i] == ']') return res;
            ++i;
        }
        if (i >= s.size() || s[i] == ']') break;
        size_t j = i;
        while (j < s.size() && (isdigit(static_cast<unsigned char>(s[j])) || s[j] == '-')) ++j;
        res.push_back(stoi(s.substr(i, j - i)));
        i = j;
    }
    return res;
}

static void printJsonStringArray(const vector<string>& v) {
    cout << "[";
    for (size_t i = 0; i < v.size(); ++i) {
        if (i) cout << ", ";
        cout << '"';
        for (char c : v[i]) {
            if (c == '"' || c == '\\') cout << '\\';
            cout << c;
        }
        cout << '"';
    }
    cout << "]" << endl;
}

int main() {
    string line;
    getline(cin, line);
    size_t pos = 0;
    while (pos < line.size() && (line[pos] == ' ' || line[pos] == '\t')) ++pos;
    string target = parseLeadingQuotedString(line, pos);
    while (pos < line.size() && (line[pos] == ' ' || line[pos] == '\t')) ++pos;
    if (pos >= line.size() || line[pos] != ',') return 1;
    ++pos;
    while (pos < line.size() && (line[pos] == ' ' || line[pos] == '\t')) ++pos;
    string rest = line.substr(pos);
    string filesStr, sizesStr;
    if (!splitTwoTopArrays(rest, filesStr, sizesStr)) return 1;
    vector<string> files = parseStringList(filesStr);
    vector<int> sizes = parseIntList(sizesStr);
    Solution solution;
    vector<string> ans = solution.findMaxOccupiedPaths(target, files, sizes);
    printJsonStringArray(ans);
    return 0;
}
