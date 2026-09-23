import java.io.*;
import java.util.*;

public class Main {

    // 计算最早空闲时刻：排序维护窗口后，找第一个不被任何窗口覆盖的非负整数
    static long findEarliestFree(long[][] windows) {
        // 按窗口起点从小到大排序
        Arrays.sort(windows, new Comparator<long[]>() {
            public int compare(long[] a, long[] b) {
                if (a[0] == b[0]) {
                    return Long.compare(a[1], b[1]);
                }
                return Long.compare(a[0], b[0]);
            }
        });

        // ans 表示当前最早可能空闲的时刻
        long ans = 0;

        for (long[] w : windows) {
            long s = w[0];   // 窗口起点
            long e = w[1];   // 窗口终点

            // 若当前窗口起点大于 ans，说明 ans 未被占用，即为答案
            if (s > ans) {
                break;
            }

            // 若 ans 落在当前窗口内，则把 ans 推进到窗口终点之后
            if (e >= ans) {
                ans = e + 1;
            }
        }

        return ans;
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner(System.in);
        PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(System.out)));

        int n = fs.nextInt();
        long[][] windows = new long[n][2];

        // 读取 n 个维护窗口
        for (int i = 0; i < n; i++) {
            windows[i][0] = fs.nextLong();
            windows[i][1] = fs.nextLong();
        }

        out.println(findEarliestFree(windows));
        out.flush();
    }

    // 快读类
    static class FastScanner {
        private final InputStream in;
        private final byte[] buffer = new byte[1 << 16];
        private int ptr = 0;
        private int len = 0;

        FastScanner(InputStream in) {
            this.in = in;
        }

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

        long nextLong() throws IOException {
            int c;
            do {
                c = read();
            } while (c <= ' ' && c != -1);

            long sign = 1;
            if (c == '-') {
                sign = -1;
                c = read();
            }

            long num = 0;
            while (c > ' ') {
                num = num * 10 + c - '0';
                c = read();
            }

            return num * sign;
        }

        int nextInt() throws IOException {
            return (int) nextLong();
        }
    }
}
