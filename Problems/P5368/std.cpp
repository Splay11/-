#include <iostream>
#include <string>
#include <vector>
using namespace std;

void farthest_posts(const vector<string>& grid, int& r1, int& c1, int& r2, int& c2) {
    // 曼哈顿距离 |r1-r2|+|c1-c2| 等于 max(|(r+c)之差|, |(r-c)之差|)
    // 扫一遍过道，记下两类极值点，取较差更大的那一对
    const int INF = 1000000000;
    int min_s = INF, max_s = -INF;
    int min_d = INF, max_d = -INF;
    int psr = 0, psc = 0, qsr = 0, qsc = 0;
    int pdr = 0, pdc = 0, qdr = 0, qdc = 0;
    for (int i = 0; i < (int)grid.size(); i++) {
        for (int j = 0; j < (int)grid[i].size(); j++) {
            if (grid[i][j] != '.') {
                continue;
            }
            int r = i + 1;
            int c = j + 1;
            int s = r + c;
            int d = r - c;
            if (s < min_s) {
                min_s = s;
                psr = r;
                psc = c;
            }
            if (s > max_s) {
                max_s = s;
                qsr = r;
                qsc = c;
            }
            if (d < min_d) {
                min_d = d;
                pdr = r;
                pdc = c;
            }
            if (d > max_d) {
                max_d = d;
                qdr = r;
                qdc = c;
            }
        }
    }
    // r+c 全相同则两个和值点重合，必须改用 r-c
    if ((psr != qsr || psc != qsc) && max_s - min_s >= max_d - min_d) {
        r1 = psr;
        c1 = psc;
        r2 = qsr;
        c2 = qsc;
    } else {
        r1 = pdr;
        c1 = pdc;
        r2 = qdr;
        c2 = qdc;
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    int h, w;
    cin >> h >> w;
    vector<string> grid(h);
    for (int i = 0; i < h; i++) {
        cin >> grid[i];
    }
    int r1, c1, r2, c2;
    farthest_posts(grid, r1, c1, r2, c2);
    cout << r1 << " " << c1 << " " << r2 << " " << c2 << "\n";
    return 0;
}
