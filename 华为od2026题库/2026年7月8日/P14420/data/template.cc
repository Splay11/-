#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
#include <cctype>
using namespace std;

// 按最外层逗号切分字符串
static vector<string> splitTopLevel(const string& s) {
    vector<string> parts;
    int depth = 0;
    string cur;
    for (char c : s) {
        if (c == '[') { depth++; cur += c; }
        else if (c == ']') { depth--; cur += c; }
        else if (c == ',' && depth == 0) { parts.push_back(cur); cur.clear(); }
        else cur += c;
    }
    parts.push_back(cur);
    return parts;
}

// 提取字符串中的所有整数（支持负数）
static vector<int> extractInts(const string& s) {
    vector<int> res;
    size_t i = 0;
    while (i < s.size()) {
        if (isdigit((unsigned char)s[i]) || s[i] == '-') {
            size_t j = i;
            if (s[i] == '-') j++;
            while (j < s.size() && isdigit((unsigned char)s[j])) j++;
            res.push_back(stoi(s.substr(i, j - i)));
            i = j;
        } else {
            i++;
        }
    }
    return res;
}

int main() {
    string line;
    getline(cin, line);

    vector<string> parts = splitTopLevel(line);
    int n = stoi(parts[0]);

    // edges：每两个整数为一条无向边
    vector<int> eints = extractInts(parts[1]);
    vector<vector<int>> edges;
    for (size_t i = 0; i + 1 < eints.size(); i += 2)
        edges.push_back({eints[i], eints[i + 1]});

    int startA = stoi(parts[2]);
    vector<int> patrolPath = extractInts(parts[3]);

    Solution solution;
    cout << solution.minMeetRounds(n, edges, startA, patrolPath) << endl;
    return 0;
}
