#include "foo.cc"
#include <iostream>
#include <string>
using namespace std;

int main() {
    string s;
    getline(cin, s);
    Solution solution;
    cout << solution.compress(s) << endl;
    return 0;
}
