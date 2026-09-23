#include <iostream>
#include <vector>
#include <string>
using namespace std;

class Solution {
public:
    string solve(vector<int>& leftWeights, vector<int>& rightWeights) {
        // 请在这里实现
        return "";
    }
};

int main() {
    int n, m;
    cin >> n >> m;

    vector<int> leftWeights(n);
    vector<int> rightWeights(m);

    for (int i = 0; i < n; ++i) {
        cin >> leftWeights[i];
    }
    for (int i = 0; i < m; ++i) {
        cin >> rightWeights[i];
    }

    Solution solution;
    cout << solution.solve(leftWeights, rightWeights) << endl;

    return 0;
}
