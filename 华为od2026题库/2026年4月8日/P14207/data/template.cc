#include "foo.cc"
#include <cctype>
#include <iostream>
#include <regex>
#include <string>
#include <vector>
using namespace std;

static vector<vector<int>> parseGuards(const string& rest) {
    vector<vector<int>> guards;
    regex re("\\(\\s*(\\d+)\\s*,\\s*(\\d+)\\s*\\)");
    for (sregex_iterator it(rest.begin(), rest.end(), re), ed; it != ed; ++it) {
        smatch const& m = *it;
        guards.push_back({stoi(m[1].str()), stoi(m[2].str())});
    }
    return guards;
}

static void printAns(const vector<int>& a) { cout << "[" << a[0] << "," << a[1] << "]\n"; }

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    getline(cin, line);
    size_t k = 0;
    while (k < line.size() && isspace(static_cast<unsigned char>(line[k]))) k++;
    size_t t = k;
    while (t < line.size() && isdigit(static_cast<unsigned char>(line[t]))) t++;
    if (t == k) return 1;
    int n = stoi(line.substr(k, t - k));
    while (t < line.size() && (isspace(static_cast<unsigned char>(line[t])) || line[t] == ',')) t++;
    string rest = line.substr(t);
    vector<vector<int>> guards = parseGuards(rest);
    Solution sol;
    vector<int> ans = sol.countShortestPaths(n, guards);
    printAns(ans);
    return 0;
}
