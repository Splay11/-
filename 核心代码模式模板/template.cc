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
    int month = stoi(line.substr(0, comma));

    string rest = line.substr(comma + 1);
    int split = rest.find("],[");
    string employeesStr = rest.substr(0, split + 1);
    string birthdaysStr = rest.substr(split + 2);

    vector<string> employees = parseStringList(employeesStr);
    vector<string> birthdays = parseStringList(birthdaysStr);

    Solution solution;
    cout << solution.countBirthdayGifts(month, employees, birthdays) << endl;
    return 0;
}
