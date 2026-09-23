import java.util.Scanner;

public class Main {
    // 递归函数计算斐波那契数列的第n项
    public static int fibonacci(int n) {
        if (n == 0) {
            return 0; // 斐波那契数列的第0项
        }
        if (n == 1) {
            return 1; // 斐波那契数列的第1项
        }
        return fibonacci(n - 1) + fibonacci(n - 2); // 递归计算F(n)
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt(); // 输入整数n
        System.out.println(fibonacci(n)); // 输出斐波那契数列的第n项
        scanner.close();
    }
}
