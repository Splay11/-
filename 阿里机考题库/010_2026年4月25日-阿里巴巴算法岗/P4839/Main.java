import java.io.*;
import java.util.*;

public class Main {
    static final long MOD = 1000000007L;

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        int T = Integer.parseInt(br.readLine());
        int[] lens = new int[T];
        String[] tokens = new String[T];
        int maxL = 0;

        // 读入每组目标编码长度与 token（评测按原题 I/O）
        for (int i = 0; i < T; i++) {
            lens[i] = Integer.parseInt(br.readLine());
            tokens[i] = br.readLine();
            maxL = Math.max(maxL, lens[i]);
        }

        // 预处理阶乘：L 次任意位置插入的序列数恒为 L!
        long[] fact = new long[maxL + 1];
        fact[0] = 1;
        for (int i = 1; i <= maxL; i++) {
            fact[i] = fact[i - 1] * i % MOD;
        }

        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < T; i++) {
            sb.append(fact[lens[i]]).append('\n');
        }
        System.out.print(sb.toString());
    }
}
