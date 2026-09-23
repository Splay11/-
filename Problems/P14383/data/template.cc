#include "foo.cc"
#include <cctype>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

static vector<int> parseArray1d(const string& s) {
    size_t i = 0;
    while (i < s.size() && isspace((unsigned char)s[i])) i++;
    if (i >= s.size() || s[i] != '[') exit(1);
    i++;
    vector<int> vals;
    while (true) {
        while (i < s.size() && isspace((unsigned char)s[i])) i++;
        if (i < s.size() && s[i] == ']') {
            i++;
            break;
        }
        int sign = 1;
        if (i < s.size() && s[i] == '-') {
            sign = -1;
            i++;
        }
        int v = 0;
        bool ok = false;
        while (i < s.size() && isdigit((unsigned char)s[i])) {
            ok = true;
            v = v * 10 + (s[i] - '0');
            i++;
        }
        if (!ok) exit(1);
        vals.push_back(sign * v);
        while (i < s.size() && isspace((unsigned char)s[i])) i++;
        if (i < s.size() && s[i] == ']') {
            i++;
            break;
        }
        if (i >= s.size() || s[i] != ',') exit(1);
        i++;
    }
    return vals;
}

static pair<vector<int>, int> parseLine(const string& line) {
    int d = 0, end = -1;
    for (int i = 0; i < (int)line.size(); i++) {
        if (line[i] == '[') d++;
        else if (line[i] == ']') {
            d--;
            if (d == 0) {
                end = i;
                break;
            }
        }
    }
    if (end < 0) exit(1);
    string arrStr = line.substr(0, end + 1);
    string tail = line.substr(end + 1);
    size_t p = 0;
    while (p < tail.size() && isspace((unsigned char)tail[p])) p++;
    if (p >= tail.size() || tail[p] != ',') exit(1);
    int k = stoi(tail.substr(p + 1));
    return {parseArray1d(arrStr), k};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    if (!getline(cin, line)) return 0;
    auto pk = parseLine(line);
    Solution sol;
    cout << sol.countValidPlans(pk.first, pk.second) << "\n";
    return 0;
}
