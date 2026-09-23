import java.util.*;

public class Main {
    // 定义全局变量矩阵和距离矩阵
    public static int[][] mp; // 存储输入矩阵，表示小区和垃圾站的位置
    public static int[][] d;  // 存储每个点到最近垃圾站的最短距离
    public static int n, m;   // 行数和列数

    // 计算所有小区到垃圾站的最短距离之和
    public static int solve() {
        int ans = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                // 累加所有小区(值为1)的距离
                if (mp[i][j] == 1 && d[i][j] != -1) {
                    ans += d[i][j];
                }
            }
        }
        return ans;  // 返回总和
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        n = sc.nextInt();  // 读取行数
        m = sc.nextInt();  // 读取列数
        mp = new int[n][m];
        d = new int[n][m];

        // 初始化输入矩阵和距离矩阵
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                mp[i][j] = sc.nextInt();  // 读取矩阵元素
                d[i][j] = -1;  // 初始化距离为 -1
            }
        }

        // BFS 实现
        Queue<int[]> queue = new LinkedList<>();
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                if (mp[i][j] == 0) {  // 垃圾站
                    queue.offer(new int[]{i, j});
                    d[i][j] = 0;  // 垃圾站的距离为 0
                }
            }
        }

        // 定义四个方向的移动（右、左、下、上）
        int[] dx = {0, 0, 1, -1};
        int[] dy = {1, -1, 0, 0};

        // 执行 BFS
        while (!queue.isEmpty()) {
            int[] current = queue.poll();
            int x = current[0], y = current[1];
            for (int i = 0; i < 4; i++) {
                int nx = x + dx[i], ny = y + dy[i];
                if (nx >= 0 && nx < n && ny >= 0 && ny < m && d[nx][ny] == -1 && mp[nx][ny] != -1) {
                    d[nx][ny] = d[x][y] + 1;
                    queue.offer(new int[]{nx, ny});
                }
            }
        }

        // 输出结果
        System.out.println(solve());
    }
}
