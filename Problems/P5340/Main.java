import java.util.Scanner;

public class Main {
    // 由序号构造前半段，镜像成回文后再转成十进制
    static long kthPalindrome(int r, int n, int t) {
        // 前半段长度：奇数时中间那一位也算在前半段里
        int h = (n + 1) / 2;
        int[] half = new int[h];
        long x = t - 1L;
        // 从右往左填前半段的低位，每一位都是 0 到 r-1
        for (int i = h - 1; i > 0; i--) {
            half[i] = (int) (x % r);
            x /= r;
        }
        // 最高位不能为 0，所以在余下的数上再加 1
        half[0] = (int) x + 1;
        int[] digits = new int[n];
        // 左右对称写下完整的 n 位
        for (int i = 0; i < h; i++) {
            digits[i] = half[i];
            digits[n - 1 - i] = half[i];
        }
        long val = 0;
        // 按 r 进制 Horner 法则转成十进制
        for (int i = 0; i < n; i++) {
            val = val * r + digits[i];
        }
        return val;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int r = sc.nextInt();
        int n = sc.nextInt();
        int t = sc.nextInt();
        System.out.println(kthPalindrome(r, n, t));
        sc.close();
    }
}
