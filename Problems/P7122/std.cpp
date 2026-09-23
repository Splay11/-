#include <iostream>
#include <vector>
using namespace std;

// 返回 {r1, c1, r2, c2}，表示元素总和最大的子矩阵的左上角与右下角坐标
vector<int> maxSubmatrix(const vector<vector<int>>& matrix) {
    int n = (int)matrix.size();
    int m = (int)matrix[0].size();

    // best 记录目前找到的最大总和；br1/bc1/br2/bc2 是它对应的四个坐标
    long long best = 0;
    bool has = false;
    int br1 = 0, bc1 = 0, br2 = 0, bc2 = 0;

    // 枚举子矩阵的上下边界 r1、r2（共 O(n^2) 对）
    for (int r1 = 0; r1 < n; r1++) {
        // col[j] 表示第 j 列在第 r1 行到当前 r2 行之间的元素之和
        vector<long long> col(m, 0);
        for (int r2 = r1; r2 < n; r2++) {
            for (int j = 0; j < m; j++) {
                col[j] += matrix[r2][j];
            }

            // 行区间固定后，问题变成一维的「最大子段和」，用 Kadane 求列区间
            long long cur = 0;   // 当前连续列的累加和
            int cStart = 0;      // 当前连续列的起点
            for (int j = 0; j < m; j++) {
                if (cur <= 0) {
                    // 前面的累加和不为正，留着只会拖累结果，从当前列重新开始
                    cur = col[j];
                    cStart = j;
                } else {
                    cur += col[j];
                }
                // 比当前最优更大才更新，保证并列时取先找到的那一个
                if (!has || cur > best) {
                    has = true;
                    best = cur;
                    br1 = r1; bc1 = cStart; br2 = r2; bc2 = j;
                }
            }
        }
    }

    // 返回最优子矩阵的左上角与右下角坐标
    return {br1, bc1, br2, bc2};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // 第一行：矩阵行数 N 和列数 M
    int n, m;
    cin >> n >> m;
    // 接下来 N 行，每行 M 个整数
    vector<vector<int>> matrix(n, vector<int>(m));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            cin >> matrix[i][j];
        }
    }

    vector<int> ans = maxSubmatrix(matrix);
    // 输出四个整数：r1 c1 r2 c2
    cout << ans[0] << " " << ans[1] << " " << ans[2] << " " << ans[3] << "\n";
    return 0;
}
