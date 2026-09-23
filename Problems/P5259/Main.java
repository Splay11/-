import java.util.ArrayList;
import java.util.Scanner;

public class Main {
    static final int MOD = 1000000007;
    static final int MAXA = 100000;
    static int[] phi = new int[MAXA + 1];

    static void initPhi() {
        for (int i = 0; i <= MAXA; i++) phi[i] = i;
        boolean[] vis = new boolean[MAXA + 1];
        for (int i = 2; i <= MAXA; i++) {
            if (vis[i]) continue;
            for (int j = i; j <= MAXA; j += i) {
                vis[j] = true;
                phi[j] = phi[j] / i * (i - 1);
            }
        }
    }

    static ArrayList<Integer> divisors(int d) {
        ArrayList<Integer> out = new ArrayList<Integer>();
        for (int t = 1; (long) t * t <= d; t++) {
            if (d % t == 0) {
                out.add(t);
                if (t * t != d) out.add(d / t);
            }
        }
        return out;
    }

    static int prefix(long n, int d) {
        if (n <= 0) return 0;
        long s = 0;
        for (int x : divisors(d)) {
            s += (long) phi[x] % MOD * ((n / x) % MOD) % MOD;
            s %= MOD;
        }
        return (int) s;
    }

    static int solve(int x, int y, long left, long right) {
        int d = Math.abs(x - y);
        if (d == 0) {
            long cnt = (right - left + 1) % MOD;
            long term = ((2L * x) % MOD + left % MOD + right % MOD) % MOD;
            return (int) (cnt * term % MOD * ((MOD + 1) / 2) % MOD);
        }
        long lo = (long) x + left;
        long hi = (long) x + right;
        int ans = prefix(hi, d) - prefix(lo - 1, d);
        if (ans < 0) ans += MOD;
        return ans;
    }

    public static void main(String[] args) {
        initPhi();
        Scanner sc = new Scanner(System.in);
        int k = sc.nextInt();
        for (int i = 0; i < k; i++) {
            int x = sc.nextInt();
            int y = sc.nextInt();
            long left = sc.nextLong();
            long right = sc.nextLong();
            System.out.println(solve(x, y, left, right));
        }
        sc.close();
    }
}
