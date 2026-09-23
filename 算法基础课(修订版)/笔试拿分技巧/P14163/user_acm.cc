#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    string solve(vector<int>& a) {
        // 请在这里实现
        return "";
    }
};

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; ++i) {
        cin >> a[i];
    }

    Solution solution;
    cout << solution.solve(a);
    return 0;
}
