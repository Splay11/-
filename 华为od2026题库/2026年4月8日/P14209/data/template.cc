#include "foo.cc"
#include <iostream>
#include <string>
using namespace std;

int main() {
    string rules;
    getline(cin, rules);
    Solution s;
    cout << s.getErrorCount(rules) << endl;
    return 0;
}
