#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

long long max_aesthetic_value(int n, int m, const vector<int>& a, const vector<int>& b, const vector<int>& c) {
    vector<vector<int>> idx(m + 1);
    
    for (int i = 0; i < n; ++i) {
        idx[a[i]].push_back(i);
    }

    long long total_value = 0;
    for (const auto& lst : idx) {
        if (lst.empty()) continue;

        vector<int> sorted_lst = lst;
        sort(sorted_lst.begin(), sorted_lst.end(), [&c, &b](int x, int y) {
            return c[x] - b[x] < c[y] - b[y];
        });

        total_value += max(b[sorted_lst[0]], c[sorted_lst[0]]);
        for (size_t i = 1; i < sorted_lst.size(); ++i) {
            total_value += c[sorted_lst[i]];
        }
    }

    return total_value;
}

int main() {
    int n, m;
    cin >> n >> m;

    vector<int> a(n), b(n), c(n);
    for (int i = 0; i < n; ++i) {
        cin >> a[i];
    }
    for (int i = 0; i < n; ++i) {
        cin >> b[i];
    }
    for (int i = 0; i < n; ++i) {
        cin >> c[i];
    }
    long long result = max_aesthetic_value(n, m, a, b, c);
    cout << result << endl;
    return 0;
}
