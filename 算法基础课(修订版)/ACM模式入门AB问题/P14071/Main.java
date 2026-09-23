import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        long a = scanner.nextLong();  // 读入第一个长整数
        long b = scanner.nextLong();  // 读入第二个长整数
        System.out.println(a + b);    // 输出它们的和
        scanner.close();              // 关闭Scanner
    }
}
