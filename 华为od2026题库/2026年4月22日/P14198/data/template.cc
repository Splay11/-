
#include <iostream>
#include <vector>
#include <string>
using namespace std;
#include "foo.cc"
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

int main() {
    string line;
    getline(cin, line);

    size_t split = line.find("],[");
    string namesStr = line.substr(0, split + 1);
    string ballotStr = line.substr(split + 2);

    vector<string> names = parseStringList(namesStr);
    vector<string> ballotTickets = parseStringList(ballotStr);

    Solution solution;
    cout << "\"" << solution.getClassMonitor(names, ballotTickets) << "\"" << endl;
    return 0;
}
