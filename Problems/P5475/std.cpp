#include <algorithm>
#include <iomanip>
#include <iostream>
#include <vector>
using namespace std;

// 按分数升序赋平均名次，再用 Mann-Whitney U 还原 AUC
double auc_from_ranks(const vector<int>& labels, const vector<double>& scores) {
    int m = (int)labels.size();
    vector<int> order(m);
    for (int i = 0; i < m; i++) {
        order[i] = i;
    }
    // 按下标稳定排序，保证同分时相对顺序确定
    sort(order.begin(), order.end(), [&](int a, int b) {
        if (scores[a] != scores[b]) {
            return scores[a] < scores[b];
        }
        return a < b;
    });
    vector<double> rank(m, 0.0);
    int i = 0;
    while (i < m) {
        int j = i;
        // 向右扩到同一分数的最后一笔
        while (j + 1 < m && scores[order[j + 1]] == scores[order[i]]) {
            j++;
        }
        // 名次从 1 起，区间 [i+1, j+1]
        double avg = (i + 1 + j + 1) / 2.0;
        for (int k = i; k <= j; k++) {
            rank[order[k]] = avg;
        }
        i = j + 1;
    }
    int k_pos = 0;
    double s_pos = 0.0;
    for (int t = 0; t < m; t++) {
        if (labels[t] == 1) {
            k_pos++;
            s_pos += rank[t];
        }
    }
    int k_neg = m - k_pos;
    // U 统计量：正类名次和减去「全排在最前」时的最小名次和
    double u = s_pos - k_pos * (k_pos + 1) / 2.0;
    return u / (k_pos * k_neg);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int m;
    cin >> m;
    vector<int> labels(m);
    vector<double> scores(m);
    for (int i = 0; i < m; i++) {
        cin >> labels[i];
    }
    for (int i = 0; i < m; i++) {
        cin >> scores[i];
    }
    cout << fixed << setprecision(6) << auc_from_ranks(labels, scores) << '\n';
    return 0;
}
