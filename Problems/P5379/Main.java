import java.math.BigInteger;
import java.util.Random;
import java.util.Scanner;

public class Main {
    static final long[] MR_BASES = {2, 325, 9375, 28178, 450775, 9780504, 1795265022L};
    static final Random RNG = new Random(1);

    static long mul(long a, long b, long mod) {
        return BigInteger.valueOf(a).multiply(BigInteger.valueOf(b)).mod(BigInteger.valueOf(mod)).longValue();
    }

    static long powMod(long a, long e, long mod) {
        long r = 1 % mod;
        while (e > 0) {
            if ((e & 1) == 1) {
                r = mul(r, a, mod);
            }
            a = mul(a, a, mod);
            e >>= 1;
        }
        return r;
    }

    static boolean isPrime(long n) {
        if (n < 2) {
            return false;
        }
        int[] small = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31};
        for (int p : small) {
            if (n % p == 0) {
                return n == p;
            }
        }
        long d = n - 1;
        int s = 0;
        while ((d & 1) == 0) {
            d >>= 1;
            s++;
        }
        for (long base : MR_BASES) {
            long a = base % n;
            if (a == 0) {
                continue;
            }
            long x = powMod(a, d, n);
            if (x == 1 || x == n - 1) {
                continue;
            }
            boolean ok = false;
            for (int i = 0; i < s - 1; i++) {
                x = mul(x, x, n);
                if (x == n - 1) {
                    ok = true;
                    break;
                }
            }
            if (!ok) {
                return false;
            }
        }
        return true;
    }

    static long gcd(long a, long b) {
        if (a < 0) {
            a = -a;
        }
        while (b != 0) {
            long t = a % b;
            a = b;
            b = t;
        }
        return a;
    }

    static long pollard(long n) {
        if (n % 2 == 0) {
            return 2;
        }
        if (isPrime(n)) {
            return n;
        }
        while (true) {
            long x = (RNG.nextLong() & Long.MAX_VALUE) % (n - 2) + 2;
            long y = x;
            long c = (RNG.nextLong() & Long.MAX_VALUE) % (n - 1) + 1;
            long d = 1;
            while (d == 1) {
                x = (mul(x, x, n) + c) % n;
                y = (mul(y, y, n) + c) % n;
                y = (mul(y, y, n) + c) % n;
                long diff = x > y ? x - y : y - x;
                d = gcd(diff, n);
            }
            if (d != n) {
                return d;
            }
        }
    }

    static long minPrimeFactor(long n) {
        if (n % 2 == 0) {
            return 2;
        }
        if (isPrime(n)) {
            return n;
        }
        long f = pollard(n);
        return Math.min(minPrimeFactor(f), minPrimeFactor(n / f));
    }

    static long smallestOddPrimeFactor(long n) {
        // 剥掉全部因子 2；只剩 1 则是 2 的幂
        while (n % 2 == 0) {
            n /= 2;
        }
        if (n == 1) {
            return -1;
        }
        return minPrimeFactor(n);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int q = sc.nextInt();
        for (int i = 0; i < q; i++) {
            long x = sc.nextLong();
            System.out.println(smallestOddPrimeFactor(x));
        }
        sc.close();
    }
}
