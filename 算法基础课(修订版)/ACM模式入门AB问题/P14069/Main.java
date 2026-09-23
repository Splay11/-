import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int a = scanner.nextInt();  // 读入第一个整数
        int b = scanner.nextInt();  // 读入第二个整数
        System.out.println(a + b);  // 输出它们的和
        scanner.close();
    }
}
