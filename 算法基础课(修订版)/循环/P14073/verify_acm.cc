#include <iostream>
#include <vector>
#include <string>
using namespace std;

class Solution {
public:
    string solve(vector<int>& leftWeights, vector<int>& rightWeights) {
        int leftTotal = 0;
        int rightTotal = 0;
        for (int w : leftWeights) leftTotal += w;
        for (int w : rightWeights) rightTotal += w;
        return leftTotal == rightTotal ? "Equal" : "Not Equal";
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
