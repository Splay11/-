import java.util.*;
import java.io.*;

public class Main {
    // 计算两个数的最大公约数（辗转相除）
    static long gcd(long x, long y) {
        while (y != 0) {
            long t = x % y;
            x = y;
            y = t;
        }
        return x;
    }

    public static void main(String[] args) throws Exception {
        // 使用 Scanner 读取
        Scanner sc = new Scanner(System.in);
        long a = sc.nextLong();
        long b = sc.nextLong();
        long c = sc.nextLong();
        long d = sc.nextLong();
        sc.close();

        // 比例相等 -> 空白为 0/1
        if (a * d == b * c) {
            System.out.println("0/1");
            return;
        }

        long p, q; // 画作占屏幕面积的分子分母
        if (a * d > b * c) {
            // 屏幕更宽：以高贴合
            p = c * b;
            q = a * d;
        } else {
            // 屏幕更窄：以宽贴合
            p = a * d;
            q = b * c;
        }

        long num = q - p; // 空白面积的分子
        long den = q;     // 空白面积的分母
        long g = gcd(num, den);
        num /= g;
        den /= g;

        System.out.println(num + "/" + den);
    }
}
