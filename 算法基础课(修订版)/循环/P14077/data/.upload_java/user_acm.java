import java.util.Scanner;

class Solution {
    public int solve(int[][] matrix, int x1, int y1, int x2, int y2) {
        // 请在这里实现
        return 0;
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        int n = scanner.nextInt();
        int m = scanner.nextInt();
        int[][] matrix = new int[n][m];

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                matrix[i][j] = scanner.nextInt();
            }
        }

        int q = scanner.nextInt();
        Solution solution = new Solution();
        while (q-- > 0) {
            int x1 = scanner.nextInt();
            int y1 = scanner.nextInt();
            int x2 = scanner.nextInt();
            int y2 = scanner.nextInt();
            System.out.println(solution.solve(matrix, x1, y1, x2, y2));
        }

        scanner.close();
    }
}
