import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in); // 创建 Scanner 对象读取输入
        int n = scanner.nextInt(); // 读取正整数 n
        int count = 0; // 初始化满足条件的整数计数

        // 遍历 1 到 n 的每个整数
        for (int i = 1; i <= n; i++) {
            int sumOfDigits = 0; // 当前数字 i 的各位数字之和
            int num = i; // 复制 i，用于提取各位数字

            // 计算各位数字之和
            while (num > 0) {
                sumOfDigits += num % 10; // 提取当前数字的个位并累加到 sumOfDigits
                num /= 10; // 去掉当前数字的个位
            }

            // 计算末尾数字 d(i)
            int lastDigit = i % 10;

            // 检查是否满足 S(i) mod 10 == d(i)
            if (sumOfDigits % 10 == lastDigit) {
                count++; // 如果满足条件，计数加一
            }
        }

        System.out.println(count); // 输出满足条件的整数个数
    }
}
