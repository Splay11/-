import java.io.*;
import java.util.*;

public class Main {
    static class FastScanner {
        private final InputStream in;
        private final byte[] buffer = new byte[1 << 16];
        private int ptr = 0, len = 0;
        FastScanner(InputStream is) { in = is; }
        private int read() throws IOException {
            if (ptr >= len) {
                len = in.read(buffer);
                ptr = 0;
                if (len <= 0) return -1;
            }
            return buffer[ptr++];
        }
        int nextInt() throws IOException {
            int c, sgn = 1, x = 0;
            do { c = read(); } while (c <= 32);
            if (c == '-') { sgn = -1; c = read(); }
            while (c > 32) {
                x = x * 10 + (c - '0');
                c = read();
            }
            return x * sgn;
        }
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner(System.in);
        int n = fs.nextInt();
        int m = fs.nextInt();
        final int U = 500000;

        int[] freq = new int[U + 1];
        for (int i = 0; i < n; i++) {
            int a = fs.nextInt();
            freq[a]++; // 统计每个分数出现次数
        }

        int[] divCnt = new int[U + 1];
        int[] mulCnt = new int[U + 1];

        // 预处理 divCnt[x] = ∑_{d|x} freq[d]
        for (int d = 1; d <= U; d++) {
            int fd = freq[d];
            if (fd == 0) continue; // 小优化
            for (int x = d; x <= U; x += d) {
                divCnt[x] += fd;
            }
        }

        // 预处理 mulCnt[x] = ∑_{k>=1} freq[k*x]
        for (int x = 1; x <= U; x++) {
            int s = 0;
            for (int j = x; j <= U; j += x) {
                s += freq[j];
            }
            mulCnt[x] = s;
        }

        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < m; i++) {
            int x = fs.nextInt();
            int ans = divCnt[x] + mulCnt[x] - freq[x]; // 去重等于x的人
            sb.append(ans).append('\n');
        }
        System.out.print(sb.toString());
    }
}
