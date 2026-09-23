#include <iostream>
#include <vector>
#include <utility>
using namespace std;

class Solution {
public:
    pair<int, vector<int>> solve(vector<int>& arr, int l, int r) {
        l--;
        r--;
        int maxValue = arr[l];
        vector<int> maxIndices = {l + 1};
        for (int i = l + 1; i <= r; ++i) {
            if (arr[i] > maxValue) {
                maxValue = arr[i];
                maxIndices.clear();
                maxIndices.push_back(i + 1);
            } else if (arr[i] == maxValue) {
                maxIndices.push_back(i + 1);
            }
        }
        return {maxValue, maxIndices};
    }
};

int main() {
    int n;
    cin >> n;
    vector<int> arr(n);
    for (int i = 0; i < n; ++i) {
        cin >> arr[i];
    }

    int q;
    cin >> q;

    Solution solution;
    while (q--) {
        int l, r;
        cin >> l >> r;
        auto result = solution.solve(arr, l, r);
        cout << result.first << endl;
        for (int i = 0; i < (int)result.second.size(); ++i) {
            cout << result.second[i] << (i + 1 == (int)result.second.size() ? "" : " ");
        }
        cout << endl;
    }

    return 0;
}
