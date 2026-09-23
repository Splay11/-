#include <iostream>
#include <vector>
#include <utility>
using namespace std;

class Solution {
public:
    int solve(vector<vector<int>>& matrix, int x1, int y1, int x2, int y2) {
        // 请在这里实现
        return 0;
    }
};

int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<int>> matrix(n, vector<int>(m));

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            cin >> matrix[i][j];
        }
    }

    int q;
    cin >> q;

    Solution solution;
    while (q--) {
        int x1, y1, x2, y2;
        cin >> x1 >> y1 >> x2 >> y2;
        cout << solution.solve(matrix, x1, y1, x2, y2) << endl;
    }

    return 0;
}
