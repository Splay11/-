import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        long num;
        long sum = 0;
        while (scanner.hasNextLong()) {  // 只要能读取到长整数，就继续累加
            num = scanner.nextLong();
            sum += num;
        }
        System.out.println(sum);  // 输出最终的和
        scanner.close();           // 关闭Scanner
    }
}
