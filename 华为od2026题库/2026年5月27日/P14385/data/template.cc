#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
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

int main() {
    string line;
    getline(cin, line);

    int comma = findTopLevelComma(line);
    string studentsStr = line.substr(0, comma);
    string votesStr = line.substr(comma + 1);

    vector<string> students = parseStringList(studentsStr);
    vector<string> votes = parseStringList(votesStr);

    Solution solution;
    cout << "\"" << solution.electMonitor(students, votes) << "\"" << endl;
    return 0;
}
