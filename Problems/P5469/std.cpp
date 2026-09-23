#include <algorithm>
#include <iostream>
#include <set>
#include <string>
#include <vector>
using namespace std;

// 按当前波次的标签增量贪心挑主机；增量打平时取更小的 nid
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int p, d;
    cin >> p >> d;
    vector<int> nid(p);
    vector<vector<string> > tags(p, vector<string>(d));
    for (int i = 0; i < p; i++) {
        cin >> nid[i];
        for (int j = 0; j < d; j++) {
            cin >> tags[i][j];
        }
    }
    int b;
    cin >> b;

    // 前 (b-r) 波容量 q，最后 r 波容量 q+1
    int base = p / b;
    int extra = p % b;
    vector<int> sizes;
    for (int i = 0; i < b - extra; i++) {
        sizes.push_back(base);
    }
    for (int i = 0; i < extra; i++) {
        sizes.push_back(base + 1);
    }

    vector<char> used(p, 0);
    for (int w = 0; w < b; w++) {
        int cap = sizes[w];
        vector<int> wave;
        // 每个维度各自维护「本波次已出现过的标签」
        vector<set<string> > seen(d);
        for (int t = 0; t < cap; t++) {
            int best_inc = -1;
            int best_pos = -1;
            for (int i = 0; i < p; i++) {
                if (used[i]) {
                    continue;
                }
                // 增量：该机各维标签里，本波次还没出现过的个数
                int inc = 0;
                for (int j = 0; j < d; j++) {
                    if (!seen[j].count(tags[i][j])) {
                        inc++;
                    }
                }
                // 增量更大优先；打平则 nid 更小优先
                if (inc > best_inc ||
                    (inc == best_inc && (best_pos == -1 || nid[i] < nid[best_pos]))) {
                    best_inc = inc;
                    best_pos = i;
                }
            }
            used[best_pos] = 1;
            wave.push_back(nid[best_pos]);
            for (int j = 0; j < d; j++) {
                seen[j].insert(tags[best_pos][j]);
            }
        }
        // 同一波次内 nid 按升序输出
        sort(wave.begin(), wave.end());
        for (int i = 0; i < (int)wave.size(); i++) {
            if (i) {
                cout << ' ';
            }
            cout << wave[i];
        }
        cout << '\n';
    }
    return 0;
}
