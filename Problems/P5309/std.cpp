#include <algorithm>
#include <iostream>
#include <queue>
#include <vector>
using namespace std;

vector<pair<int, int> > solve(int r, int c, int sx, int sy, vector<vector<int> > a) {
  vector<pair<int, int> > empty;
  // 起点是陆地，无法逃生
  if (a[sx][sy] == 1) return empty;
  const int inf = 1000000000;
  vector<vector<int> > dist(r, vector<int>(c, inf));
  vector<vector<int> > rsum(r, vector<int>(c, 0));
  vector<vector<int> > csum(r, vector<int>(c, 0));
  vector<vector<int> > px(r, vector<int>(c, -1));
  vector<vector<int> > py(r, vector<int>(c, -1));
  dist[sx][sy] = 0;
  rsum[sx][sy] = sx;
  csum[sx][sy] = sy;
  queue<pair<int, int> > q;
  q.push(make_pair(sx, sy));
  int dx[4] = {-1, 1, 0, 0};
  int dy[4] = {0, 0, -1, 1};
  while (!q.empty()) {
    int x = q.front().first, y = q.front().second;
    q.pop();
    for (int k = 0; k < 4; k++) {
      int nx = x + dx[k], ny = y + dy[k];
      if (nx < 0 || nx >= r || ny < 0 || ny >= c) continue;
      if (a[nx][ny] != 0) continue;
      int nd = dist[x][y] + 1;
      int nrs = rsum[x][y] + nx;
      int ncs = csum[x][y] + ny;
      // 更短，或者同样短但行号和/列号和更优，则更新
      if (nd < dist[nx][ny]) {
        dist[nx][ny] = nd;
        rsum[nx][ny] = nrs;
        csum[nx][ny] = ncs;
        px[nx][ny] = x;
        py[nx][ny] = y;
        q.push(make_pair(nx, ny));
      } else if (nd == dist[nx][ny]) {
        if (nrs < rsum[nx][ny] || (nrs == rsum[nx][ny] && ncs < csum[nx][ny])) {
          rsum[nx][ny] = nrs;
          csum[nx][ny] = ncs;
          px[nx][ny] = x;
          py[nx][ny] = y;
        }
      }
    }
  }
  int bestD = inf, ei = -1, ej = -1;
  for (int i = 0; i < r; i++) {
    for (int j = 0; j < c; j++) {
      if (dist[i][j] >= inf) continue;
      // 边界水域才算出岛
      if (i == 0 || i == r - 1 || j == 0 || j == c - 1) {
        if (ei < 0 || dist[i][j] < bestD || (dist[i][j] == bestD && (i < ei || (i == ei && j < ej)))) {
          bestD = dist[i][j];
          ei = i;
          ej = j;
        }
      }
    }
  }
  if (ei < 0) return empty;
  vector<pair<int, int> > path;
  int cx = ei, cy = ej;
  while (cx >= 0) {
    path.push_back(make_pair(cx, cy));
    int tx = px[cx][cy];
    int ty = py[cx][cy];
    cx = tx;
    cy = ty;
  }
  reverse(path.begin(), path.end());
  return path;
}

int main() {
  int r, c, sx, sy;
  cin >> r >> c >> sx >> sy;
  vector<vector<int> > a(r, vector<int>(c));
  for (int i = 0; i < r; i++) {
    for (int j = 0; j < c; j++) cin >> a[i][j];
  }
  vector<pair<int, int> > path = solve(r, c, sx, sy, a);
  if (path.empty()) {
    cout << -1 << endl;
  } else {
    cout << (int)path.size() - 1 << endl;
    for (int i = 0; i < (int)path.size(); i++) {
      cout << path[i].first << " " << path[i].second << endl;
    }
  }
  return 0;
}
