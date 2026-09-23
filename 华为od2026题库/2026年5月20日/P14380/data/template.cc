#include <bits/stdc++.h>
#include "foo.cc"
using namespace std;

int main() {
    int n;
    if (!(cin >> n)) return 0;

    Solution solution;
    cout << solution.equalDistanceBinary(n) << endl;
    return 0;
}
