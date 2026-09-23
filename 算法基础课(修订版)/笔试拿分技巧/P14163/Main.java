import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        
        int n = sc.nextInt();  // 输入整数 n
        int[] a = new int[n];
        
        // 输入 n 个整数到数组 a 中
        for (int i = 0; i < n; i++) {
            a[i] = sc.nextInt();
        }

        // 输出数组 a 的所有元素，空格分隔
        for (int i = 0; i < n; i++) {
            System.out.print(a[i]);  // 输出元素
            if (i != n - 1) {
                System.out.print(" ");  // 避免最后一个元素后有空格
            }
        }
    }
}
