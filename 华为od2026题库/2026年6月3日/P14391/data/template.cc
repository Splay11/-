#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
#include <cctype>
using namespace std;

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

static vector<int> parseIntList(const string& s) {
    vector<int> res;
    long long num = 0;
    int sign = 1;
    bool inNum = false;

    for (char c : s) {
        if (c == '-') {
            sign = -1;
            num = 0;
            inNum = true;
        } else if (isdigit((unsigned char)c)) {
            if (!inNum) {
                sign = 1;
                num = 0;
                inNum = true;
            }
            num = num * 10 + (c - '0');
        } else {
            if (inNum) {
                res.push_back((int)(sign * num));
                inNum = false;
                num = 0;
                sign = 1;
            }
        }
    }

    if (inNum) {
        res.push_back((int)(sign * num));
    }
    return res;
}

static int findTopLevelComma(const string& s) {
    bool inString = false;
    int bracket = 0;
    for (int i = 0; i < (int)s.size(); i++) {
        char c = s[i];
        if (c == '"') {
            inString = !inString;
        } else if (!inString) {
            if (c == '[') bracket++;
            else if (c == ']') bracket--;
            else if (c == ',' && bracket == 0) return i;
        }
    }
    return -1;
}

static void printVector(const vector<int>& ans) {
    cout << "[";
    for (int i = 0; i < (int)ans.size(); i++) {
        if (i) cout << ",";
        cout << ans[i];
    }
    cout << "]";
}

int main() {
    string line, part;
    while (getline(cin, part)) {
        line += part;
    }

    int comma = findTopLevelComma(line);
    string opsStr = line.substr(0, comma);
    string valsStr = line.substr(comma + 1);

    vector<string> ops = parseStringList(opsStr);
    vector<int> vals = parseIntList(valsStr);

    Solution solution;
    vector<int> ans = solution.monitor(ops, vals);
    printVector(ans);
    return 0;
}
