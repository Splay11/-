import java.util.Scanner;

public class Main {
    static final long MOD = 998244353L;

    // 快速幂：计算 a^b % MOD
    static long qpow(long a, long b) {
        long res = 1;
        a %= MOD;
        while (b > 0) {
            if ((b & 1) == 1) {
                res = res * a % MOD;
            }
            a = a * a % MOD;
            b >>= 1;
        }
        return res;
    }

    // 计算长度为 n 的所有数字的洞数总和
    static long solve(long n) {
        // 特判：n=1 时，0 也算一个一位数
        if (n == 1) {
            return 6;
        }
        // n>=2 时使用推导公式
        long part = qpow(10, n - 2);
        long temp = (54 * (n % MOD) - 4 + MOD) % MOD;
        return part * temp % MOD;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int T = sc.nextInt();
        while (T-- > 0) {
            long n = sc.nextLong();
            System.out.println(solve(n));
        }
        sc.close();
    }
}
