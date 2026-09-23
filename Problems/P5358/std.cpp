#include <iostream>
#include <queue>
#include <vector>
using namespace std;

int shortest(int h, int w, const vector<vector<int> >& a) {
    // 起点或终点是货架，直接到不了
    if (a[0][0] == 1 || a[h - 1][w - 1] == 1) {
        return -1;
    }
    // dist[i][j] 表示走到该格时已经踩过的格子数；0 表示还没访问
    vector<vector<int> > dist(h, vector<int>(w, 0));
    queue<pair<int, int> > q;
    dist[0][0] = 1;
    q.push(make_pair(0, 0));
    int dx[4] = {-1, 1, 0, 0};
    int dy[4] = {0, 0, -1, 1};
    while (!q.empty()) {
        int x = q.front().first;
        int y = q.front().second;
        q.pop();
        if (x == h - 1 && y == w - 1) {
            return dist[x][y];
        }
        for (int k = 0; k < 4; k++) {
            int nx = x + dx[k];
            int ny = y + dy[k];
            // 越界、货架、已经走过的格子都跳过
            if (nx < 0 || nx >= h || ny < 0 || ny >= w) {
                continue;
            }
            if (a[nx][ny] == 1 || dist[nx][ny] != 0) {
                continue;
            }
            dist[nx][ny] = dist[x][y] + 1;
            q.push(make_pair(nx, ny));
        }
    }
    return -1;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    int h, w;
    cin >> h >> w;
    vector<vector<int> > a(h, vector<int>(w));
    for (int i = 0; i < h; i++) {
        for (int j = 0; j < w; j++) {
            cin >> a[i][j];
        }
    }
    cout << shortest(h, w, a) << endl;
    return 0;
}
