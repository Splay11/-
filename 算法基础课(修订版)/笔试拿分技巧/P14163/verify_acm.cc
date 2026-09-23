#include <iostream>
#include <sstream>
#include <vector>
using namespace std;

class Solution {
public:
    string solve(vector<int>& a) {
        ostringstream oss;
        for (int i = 0; i < (int)a.size(); ++i) {
            if (i > 0) {
                oss << ' ';
            }
            oss << a[i];
        }
        return oss.str();
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
