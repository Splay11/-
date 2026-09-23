import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    static long gcd(long a, long b) {
        // 辗转相除求最大公约数
        while (b != 0) {
            long t = a % b;
            a = b;
            b = t;
        }
        return a;
    }

    // 1..n 的最小公倍数：每步 lcm(ans, i) = ans / gcd * i
    static long solve(int n) {
        long ans = 1;
        for (int i = 1; i <= n; i++) {
            long g = gcd(ans, i);
            ans = ans / g * i;
        }
        return ans;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        System.out.println(solve(n));
    }
}
