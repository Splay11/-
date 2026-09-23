#include<bits/stdc++.h>
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

    vector<string> docs = parseStringList(line);

    Solution solution;
    cout << solution.featureExtraction(docs) << endl;
    return 0;
}
