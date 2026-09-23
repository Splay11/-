import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.*;

public class Main {
    static int n, k;
    static int[][] a;

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        // 读取n和k
        n = Integer.parseInt(br.readLine().trim());
        k = Integer.parseInt(br.readLine().trim());
        a = new int[n][n];
        // 读取迷宫的辐射值
        for (int i = 0; i < n; i++) {
            String[] parts = br.readLine().trim().split("\\s+");
            for (int j = 0; j < n; j++) {
                a[i][j] = Integer.parseInt(parts[j]);
            }
        }

        // 二分查找的初始边界
        int left = Math.max(a[0][0], a[n-1][n-1]);
        int right = Integer.MIN_VALUE;
        for (int[] row : a) {
            for (int val : row) {
                if (val > right) right = val;
            }
        }

        int answer = right;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (bfs(mid)) {
                answer = mid;
                right = mid - 1;
            } else {
                left = mid + 1;
            }
        }

        // 输出结果
        System.out.println(answer);
    }

    // BFS函数，检查是否可以在k步内到达终点，且所有经过的格子辐射值 ≤ val
    private static boolean bfs(int val) {
        // 检查起点和终点的辐射值是否符合
        if (a[0][0] > val || a[n-1][n-1] > val) return false;

        // 定义移动方向：右、左、下、上
        int[] dx = {0, 0, 1, -1};
        int[] dy = {1, -1, 0, 0};

        // 距离数组，记录每个格子的最短步数
        int[][] dist = new int[n][n];
        for (int[] row : dist) Arrays.fill(row, -1);
        dist[0][0] = 0;

        // 使用队列进行BFS
        Queue<int[]> queue = new LinkedList<>();
        queue.offer(new int[]{0, 0});

        while (!queue.isEmpty()) {
            int[] current = queue.poll();
            int x = current[0];
            int y = current[1];
            int steps = dist[x][y];

            // 如果到达终点，检查步数是否 ≤ K
            if (x == n-1 && y == n-1) {
                return steps <= k;
            }

            // 遍历四个方向
            for (int i = 0; i < 4; i++) {
                int nx = x + dx[i];
                int ny = y + dy[i];
                // 检查边界
                if (nx < 0 || nx >= n || ny < 0 || ny >= n) continue;
                // 检查辐射值和是否已访问
                if (a[nx][ny] > val || dist[nx][ny] != -1) continue;
                // 检查步数是否超过K
                if (steps + 1 > k) continue;
                // 更新步数并加入队列
                dist[nx][ny] = steps + 1;
                queue.offer(new int[]{nx, ny});
            }
        }

        // 如果无法到达终点
        return false;
    }
}
