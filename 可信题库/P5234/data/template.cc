#include "foo.cc"
#include <iostream>
#include <string>

using namespace std;

static string parseQuoted(const string& line) {
    size_t a = line.find('"');
    size_t b = line.rfind('"');
    if (a == string::npos || b == string::npos || b <= a) exit(1);
    return line.substr(a + 1, b - a - 1);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    if (!getline(cin, line)) return 0;
    Solution sol;
    cout << '"' << sol.sortLetter(parseQuoted(line)) << '"' << '\n';
    return 0;
}
