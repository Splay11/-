import java.io.*;
import java.util.*;

public class Main {

    // 统计交叉表 pulse[i] * gauge[j] >= bound 的格子数
    static long countPairs(long[] pulse, long[] gauge, long bound) {
        Arrays.sort(gauge);
        int C = gauge.length;
        long ans = 0;

        for (long p : pulse) {
            if (bound == 0) {
                ans += C;
            } else if (p == 0) {
                continue;
            } else {
                long need = (bound + p - 1) / p;
                int pos = lowerBound(gauge, need);
                ans += C - pos;
            }
        }
        return ans;
    }

    static int lowerBound(long[] arr, long target) {
        int left = 0, right = arr.length;
        while (left < right) {
            int mid = (left + right) / 2;
            if (arr[mid] >= target) right = mid;
            else left = mid + 1;
        }
        return left;
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner(System.in);
        StringBuilder sb = new StringBuilder();

        int T = fs.nextInt();
        for (int tc = 0; tc < T; tc++) {
            int R = fs.nextInt();
            int C = fs.nextInt();
            long bound = fs.nextLong();

            long[] pulse = new long[R];
            long[] gauge = new long[C];
            for (int i = 0; i < R; i++) pulse[i] = fs.nextLong();
            for (int j = 0; j < C; j++) gauge[j] = fs.nextLong();

            sb.append(countPairs(pulse, gauge, bound)).append('\n');
        }
        System.out.print(sb.toString());
    }

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

        long nextLong() throws IOException {
            int c;
            do { c = read(); } while (c <= ' ');
            long num = 0;
            while (c > ' ') {
                num = num * 10 + c - '0';
                c = read();
            }
            return num;
        }

        int nextInt() throws IOException { return (int) nextLong(); }
    }
}
