import java.util.Scanner;

public class Main {

    // 递归函数：计算从 (x, y) 出发到右下角的路径数
    public static int uniquePaths(int x, int y, int n) {
        // 基本情况：到达右下角 (n-1, n-1)，返回 1
        if (x == n - 1 && y == n - 1) {
            return 1;
        }

        int paths = 0;

        // 向下走
        if (x < n - 1) {
            paths += uniquePaths(x + 1, y, n);
        }

        // 向右走
        if (y < n - 1) {
            paths += uniquePaths(x, y + 1, n);
        }

        return paths;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt(); // 输入网格的大小

        // 从 (0, 0) 出发计算路径数
        System.out.println(uniquePaths(0, 0, n));

        scanner.close();
    }
}
