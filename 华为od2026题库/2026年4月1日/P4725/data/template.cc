#include <bits/stdc++.h>
#include "foo.cc"

using namespace std;

int main() {
    Solution solution;

    int M, N;
    char ch;
    cin >> M >> ch >> N;

    cout << solution.getNthValue(M, N);

    return 0;
}