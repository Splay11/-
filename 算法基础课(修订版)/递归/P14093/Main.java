import java.util.Scanner;

public class Main{
    // 全局变量：记录路径数
    static int countPaths = 0;

    // 四个方向：上、下、左、右
    static int[] dx = {-1, 1, 0, 0};
    static int[] dy = {0, 0, -1, 1};

    // 递归函数：DFS计算路径数
    // x , y 代表当前所在的行和列
    // steps 记录当前走的步数
    // ex , ey 代表目的地所在的行和列
    // k 代表最多能走多少步
    public static void dfs(int x, int y, int steps, int n, int ex, int ey, int k) {
        // 如果当前坐标是终点，则路径计数加一
        if (x == ex && y == ey) {
            countPaths++;
        }

        // 如果已经达到最大步数，停止递归
        if (steps == k) {
            return;
        }

        // 尝试四个方向移动
        for (int dir = 0; dir < 4; dir++) {
            int newX = x + dx[dir];
            int newY = y + dy[dir];

            // 检查新位置是否在网格内
            if (newX >= 1 && newX <= n && newY >= 1 && newY <= n) {
                dfs(newX, newY, steps + 1, n, ex, ey, k);
            }
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // 输入网格大小
        int n = scanner.nextInt();

        // 输入起点和终点坐标 (sx, sy) 和 (ex, ey)
        int sx = scanner.nextInt();
        int sy = scanner.nextInt();
        int ex = scanner.nextInt();
        int ey = scanner.nextInt();

        // 输入最大步数
        int k = scanner.nextInt();

        // 调用DFS，初始步数为 0
        dfs(sx, sy, 0, n, ex, ey, k);

        // 输出路径总数
        System.out.println(countPaths);

        scanner.close();
    }
}
