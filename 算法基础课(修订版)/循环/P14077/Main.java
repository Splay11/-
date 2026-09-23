import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        int n, m;
        n = scanner.nextInt();
        m = scanner.nextInt();  // 输入矩阵的行和列
        int[][] matrix = new int[n][m];
        
        // 输入矩阵元素
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                matrix[i][j] = scanner.nextInt();
            }
        }
        
        int q = scanner.nextInt();  // 输入查询次数
        
        while (q-- > 0) {
            int x1 = scanner.nextInt();
            int y1 = scanner.nextInt();
            int x2 = scanner.nextInt();
            int y2 = scanner.nextInt();  // 输入查询的坐标
            
            // 转换为 0-indexed
            x1--; y1--; x2--; y2--;
            
            int maxVal = matrix[x1][y1];  // 初始化最大值
            
            // 遍历子矩阵寻找最大值
            for (int i = x1; i <= x2; i++) {
                for (int j = y1; j <= y2; j++) {
                    if (matrix[i][j] > maxVal) {
                        maxVal = matrix[i][j];
                    }
                }
            }
            
            System.out.println(maxVal);  // 输出结果
        }
        
        scanner.close();
    }
}
