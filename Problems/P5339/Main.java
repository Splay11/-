import java.util.ArrayDeque;
import java.util.Queue;
import java.util.Scanner;

public class Main {
    static int countClosed(char[][] grid) {
        int h = grid.length;
        int w = grid[0].length;
        boolean[][] vis = new boolean[h][w];
        Queue<int[]> q = new ArrayDeque<int[]>();

        // 从边界上的村庄出发，能走到的都是自由村庄
        for (int j = 0; j < w; j++) {
            add(grid, vis, q, 0, j);
            add(grid, vis, q, h - 1, j);
        }
        for (int i = 0; i < h; i++) {
            add(grid, vis, q, i, 0);
            add(grid, vis, q, i, w - 1);
        }

        int[] di = {1, -1, 0, 0};
        int[] dj = {0, 0, 1, -1};
        while (!q.isEmpty()) {
            int[] cur = q.poll();
            int i = cur[0];
            int j = cur[1];
            for (int k = 0; k < 4; k++) {
                add(grid, vis, q, i + di[k], j + dj[k]);
            }
        }

        int ans = 0;
        for (int i = 0; i < h; i++) {
            for (int j = 0; j < w; j++) {
                // 没被边界搜到的村庄就是封闭领地
                if (grid[i][j] == 'V' && !vis[i][j]) {
                    ans++;
                }
            }
        }
        return ans;
    }

    static void add(char[][] grid, boolean[][] vis, Queue<int[]> q, int i, int j) {
        int h = grid.length;
        int w = grid[0].length;
        if (i < 0 || i >= h || j < 0 || j >= w) {
            return;
        }
        if (grid[i][j] != 'V' || vis[i][j]) {
            return;
        }
        vis[i][j] = true;
        q.add(new int[] {i, j});
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int h = sc.nextInt();
        int w = sc.nextInt();
        char[][] grid = new char[h][w];
        for (int i = 0; i < h; i++) {
            String s = sc.next();
            grid[i] = s.toCharArray();
        }
        System.out.println(countClosed(grid));
        sc.close();
    }
}
