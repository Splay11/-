#include "foo.cc"
#include <iostream>
#include <string>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    if (!getline(cin, line)) return 0;
    Solution sol;
    cout << sol.parsePacketHeader(line) << "\n";
    return 0;
}
