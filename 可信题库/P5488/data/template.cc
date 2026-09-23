#include "foo.cc"
#include <iostream>
#include <string>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    if (!getline(cin, line)) return 0;
    while (!line.empty() && (line.back() == '\r' || line.back() == '\n')) line.pop_back();
    string note;
    if (line.size() >= 2 && line.front() == '"' && line.back() == '"') {
        note = line.substr(1, line.size() - 2);
    }
    Solution sol;
    cout << sol.firstTasteLevel(note) << '\n';
    return 0;
}
