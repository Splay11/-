import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        String A = scanner.next();
        String B = scanner.next(); // 输入字符串 A 和 B
        
        // 计算 A 和 B 的长度
        int lenA = A.length();
        int lenB = B.length();
        
        // 判断 B 的长度是否是 A 的整数倍
        if (lenB % lenA != 0) {
            System.out.println("No"); // 如果不是，输出 "No"
            scanner.close();
            return;
        }
        
        // 计算重复的次数
        int k = lenB / lenA;
        StringBuilder constructed = new StringBuilder(); // 构造字符串
        for (int i = 0; i < k; i++) {
            constructed.append(A); // 将 A 重复 k 次
        }
        
        // 比较构造的字符串和 B
        if (constructed.toString().equals(B)) {
            System.out.println("Yes"); // 如果相等，输出 "Yes"
        } else {
            System.out.println("No"); // 否则，输出 "No"
        }
        
        scanner.close();
    }
}
