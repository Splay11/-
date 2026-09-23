import java.util.Scanner;

public class Main {

    // 检查字符串是否是回文
    public static boolean isPalindrome(String str) {
        int left = 0, right = str.length() - 1;
        while (left < right) {
            if (str.charAt(left) != str.charAt(right)) {
                return false; // 如果不相等，返回 false
            }
            left++;
            right--;
        }
        return true; // 全部字符都匹配，返回 true
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // 输入字符串 A 和 B
        String A = scanner.next();
        String B = scanner.next();

        // 在字符串 A 的所有可能插入位置尝试插入 B
        // 包括开头和结尾的情况
        for (int i = 0; i <= A.length(); i++) {
            // 构造新字符串
            String newString = A.substring(0, i) + B + A.substring(i);
            
            // 检查新字符串是否为回文
            if (isPalindrome(newString)) {
                System.out.println("YES");
                return; // 找到一个回文，立即返回
            }
        }

        System.out.println("NO"); // 如果没有找到回文，输出 NO
    }
}
