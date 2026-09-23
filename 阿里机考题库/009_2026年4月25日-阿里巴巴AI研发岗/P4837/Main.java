import java.io.BufferedInputStream;
import java.io.IOException;

public class Main {
    static final int MAX_MASK = 1023;
    static final int SIZE = 1024;

    static int countDistinctMasks(int[] feat) {
        // g[mask]：所有包含 mask 的超集特征值的按位与结果
        int[] g = new int[SIZE];

        // exist[mask]：是否存在原初值恰好为 mask
        boolean[] exist = new boolean[SIZE];

        for (int i = 0; i < SIZE; i++) {
            g[i] = MAX_MASK;
        }

        for (int x : feat) {
            g[x] = x;
            exist[x] = true;
        }

        // 超集 DP：合并更大掩码的按位与信息
        for (int bit = 0; bit < 10; bit++) {
            for (int mask = 0; mask < SIZE; mask++) {
                if ((mask & (1 << bit)) == 0) {
                    int superMask = mask | (1 << bit);
                    if (exist[superMask]) {
                        g[mask] &= g[superMask];
                        exist[mask] = true;
                    }
                }
            }
        }

        int ans = 0;
        for (int mask = 0; mask < SIZE; mask++) {
            // 可达当且仅当存在超集且其按位与恰好为 mask
            if (exist[mask] && g[mask] == mask) {
                ans++;
            }
        }

        return ans;
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner();

        int tc = fs.nextInt();
        StringBuilder sb = new StringBuilder();

        for (int caseId = 0; caseId < tc; caseId++) {
            int m = fs.nextInt();
            int[] feat = new int[m];

            for (int i = 0; i < m; i++) {
                feat[i] = fs.nextInt();
            }

            sb.append(countDistinctMasks(feat)).append('\n');
        }

        System.out.print(sb.toString());
    }
}

class FastScanner {
    private final BufferedInputStream in = new BufferedInputStream(System.in);
    private final byte[] buffer = new byte[1 << 16];
    private int ptr = 0;
    private int len = 0;

    private int read() throws IOException {
        if (ptr >= len) {
            len = in.read(buffer);
            ptr = 0;
            if (len <= 0) {
                return -1;
            }
        }
        return buffer[ptr++];
    }

    int nextInt() throws IOException {
        int c;
        do {
            c = read();
        } while (c <= ' ');

        int sign = 1;
        if (c == '-') {
            sign = -1;
            c = read();
        }

        int val = 0;
        while (c > ' ') {
            val = val * 10 + (c - '0');
            c = read();
        }

        return val * sign;
    }
}
