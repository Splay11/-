import java.util.Scanner;

public class Main {

    static final long MOD = 998244353L;

    // 快速幂：计算 a^e % mod
    static long fastPow(long a, long e, long mod) {
        long res = 1L;
        a %= mod;
        while (e > 0) {
            if ((e & 1) != 0) res = res * a % mod;
            a = a * a % mod;
            e >>= 1;
        }
        return res;
    }

    // 返回使方案1胜出概率最大的初始编排数，对 998244353 取模
    static long solve(int m) {
        long e = (1L << m) - 1;  // 指数 = 2^m - 1
        return fastPow(2, e, MOD);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int m = sc.nextInt();
        System.out.println(solve(m));
        sc.close();
    }
}
