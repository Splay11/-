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

static vector<string> parseStringArray(const string& line) {
    string s = trim(line);
    vector<string> out;
    if (s.empty() || s[0] != '[') exit(1);
    size_t i = 1;
    while (true) {
        while (i < s.size() && isspace((unsigned char)s[i])) i++;
        if (i < s.size() && s[i] == ']') {
            i++;
            break;
        }
        if (i >= s.size() || s[i] != '"') exit(1);
        i++;
        string cur;
        while (i < s.size() && s[i] != '"') {
            cur.push_back(s[i]);
            i++;
        }
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

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line1, line2;
    if (!getline(cin, line1)) return 0;
    if (!getline(cin, line2)) return 0;
    auto charMatrix = parseStringArray(line1);
    auto words = parseStringArray(line2);
    Solution sol;
    cout << sol.countMatchedWords(charMatrix, words) << "\n";
    return 0;
}
