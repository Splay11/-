import java.util.ArrayDeque;
import java.util.Queue;
import java.util.Scanner;

public class Main {
    static int shortest(int h, int w, int[][] a) {
        // 起点或终点是货架，直接到不了
        if (a[0][0] == 1 || a[h - 1][w - 1] == 1) {
            return -1;
        }
        // dist[i][j] 表示走到该格时已经踩过的格子数；0 表示还没访问
        int[][] dist = new int[h][w];
        Queue<int[]> q = new ArrayDeque<int[]>();
        dist[0][0] = 1;
        q.add(new int[] {0, 0});
        int[] dx = {-1, 1, 0, 0};
        int[] dy = {0, 0, -1, 1};
        while (!q.isEmpty()) {
            int[] cur = q.poll();
            int x = cur[0];
            int y = cur[1];
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
                q.add(new int[] {nx, ny});
            }
        }
        return -1;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int h = sc.nextInt();
        int w = sc.nextInt();
        int[][] a = new int[h][w];
        for (int i = 0; i < h; i++) {
            for (int j = 0; j < w; j++) {
                a[i][j] = sc.nextInt();
            }
        }
        System.out.println(shortest(h, w, a));
        sc.close();
    }
}
