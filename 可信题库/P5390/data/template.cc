#include "foo.cc"
#include <iostream>
#include <string>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s;
    if (!getline(cin, s)) return 0;
    cout << Solution().reviseMarks(s) << "\n";
    return 0;
}
