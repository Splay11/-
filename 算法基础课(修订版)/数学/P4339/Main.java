import java.io.*;
import java.util.*;

public class Main {
    static final long MOD = 1_000_000_007L;
    static final long INV2 = 500_000_004L; // 2 的逆元

    // S(m) = (m(m+1)/2)^2  (mod MOD)
    static long sumCubes(long m) {
        if (m <= 0) return 0;
        m %= MOD;
        long t = m * ((m + 1) % MOD) % MOD; // m(m+1)
        t = t * INV2 % MOD;                 // /2
        return t * t % MOD;                 // 平方
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n = Long.parseLong(br.readLine().trim());

        long ans = 0, L = 1;
        while (L <= n) {
            long q = n / L;        // 当前商
            long R = n / q;        // 该商的最右端
            long seg = (sumCubes(R) - sumCubes(L - 1)) % MOD; // 区间立方和
            if (seg < 0) seg += MOD;
            ans = (ans + seg * (q % MOD)) % MOD;              // 加权累加
            L = R + 1;             // 下一段
        }
        System.out.println(ans % MOD);
    }
}
