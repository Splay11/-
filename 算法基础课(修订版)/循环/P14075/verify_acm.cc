#include <iostream>
#include <vector>
#include <utility>
#include <algorithm>
using namespace std;

class Solution {
public:
    pair<int, vector<int>> solve(vector<int>& arr) {
        int maxValue = arr[0];
        for (int x : arr) maxValue = max(maxValue, x);
        vector<int> indices;
        for (int i = 0; i < (int)arr.size(); ++i) {
            if (arr[i] == maxValue) indices.push_back(i);
        }
        return {maxValue, indices};
    }
};

int main() {
    int n;
    cin >> n;

    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }

    Solution solution;
    auto result = solution.solve(arr);

    cout << result.first << endl;
    for (int i = 0; i < (int)result.second.size(); i++) {
        cout << result.second[i] << (i + 1 == (int)result.second.size() ? "" : " ");
    }
    cout << endl;

    return 0;
}
