import java.util.Scanner;

public class Main {
    public static String isSubsequence(int[] a, int[] b) {
        int i = 0, j = 0; // 初始化指针 i 和 j
        int n = a.length, m = b.length;

        // 使用双指针判断子序列
        while (i < n && j < m) {
            if (a[i] == b[j]) { // 如果匹配，移动 a 的指针
                i++;
            }
            j++; // 无论是否匹配，b 的指针都要移动
        }

        // 判断是否匹配完所有元素
        return (i == n) ? "YES" : "NO";
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // 读取序列的长度
        int n = scanner.nextInt();
        int m = scanner.nextInt();

        // 读取序列 a
        int[] a = new int[n];
        for (int i = 0; i < n; i++) {
            a[i] = scanner.nextInt();
        }

        // 读取序列 b
        int[] b = new int[m];
        for (int i = 0; i < m; i++) {
            b[i] = scanner.nextInt();
        }

        // 调用函数并输出结果
        System.out.println(isSubsequence(a, b));

        scanner.close();
    }
}
