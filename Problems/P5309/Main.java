import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;

public class Main {
  static ArrayList<int[]> solve(int r, int c, int sx, int sy, int[][] a) {
    // 起点是陆地，无法逃生
    if (a[sx][sy] == 1) return null;
    int inf = 1000000000;
    int[][] dist = new int[r][c];
    int[][] rsum = new int[r][c];
    int[][] csum = new int[r][c];
    int[][] px = new int[r][c];
    int[][] py = new int[r][c];
    for (int i = 0; i < r; i++) {
      for (int j = 0; j < c; j++) {
        dist[i][j] = inf;
        px[i][j] = -1;
        py[i][j] = -1;
      }
    }
    dist[sx][sy] = 0;
    rsum[sx][sy] = sx;
    csum[sx][sy] = sy;
    ArrayDeque<int[]> q = new ArrayDeque<int[]>();
    q.add(new int[] {sx, sy});
    int[] dx = {-1, 1, 0, 0};
    int[] dy = {0, 0, -1, 1};
    while (!q.isEmpty()) {
      int[] cur = q.poll();
      int x = cur[0], y = cur[1];
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
          q.add(new int[] {nx, ny});
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
    if (ei < 0) return null;
    ArrayList<int[]> path = new ArrayList<int[]>();
    int cx = ei, cy = ej;
    while (cx >= 0) {
      path.add(new int[] {cx, cy});
      int tx = px[cx][cy];
      int ty = py[cx][cy];
      cx = tx;
      cy = ty;
    }
    Collections.reverse(path);
    return path;
  }

  public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
    int r = sc.nextInt();
    int c = sc.nextInt();
    int sx = sc.nextInt();
    int sy = sc.nextInt();
    int[][] a = new int[r][c];
    for (int i = 0; i < r; i++) {
      for (int j = 0; j < c; j++) a[i][j] = sc.nextInt();
    }
    ArrayList<int[]> path = solve(r, c, sx, sy, a);
    if (path == null) {
      System.out.println(-1);
    } else {
      System.out.println(path.size() - 1);
      for (int i = 0; i < path.size(); i++) {
        System.out.println(path.get(i)[0] + " " + path.get(i)[1]);
      }
    }
    sc.close();
  }
}
