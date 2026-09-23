import java.io.*;
import java.util.*;

public class Main {

    static class FastScanner {
        private final InputStream in = System.in;
        private final byte[] buffer = new byte[1 << 16];
        private int ptr = 0, len = 0;

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
                val = val * 10 + c - '0';
                c = read();
            }
            return val * sign;
        }
    }

    // 在化简后的品类序列上求最长奇回文半径
    static int oddPalindromeRadius(int[] labels, int n) {
        int[] radius = new int[n];
        int left = 0, right = -1;
        int best = 0;

        for (int i = 0; i < n; i++) {
            int k;
            if (i > right) {
                k = 1;
            } else {
                k = Math.min(radius[left + right - i], right - i + 1);
            }

            while (i - k >= 0 && i + k < n && labels[i - k] == labels[i + k]) {
                k++;
            }

            radius[i] = k;
            best = Math.max(best, k);

            if (i + k - 1 > right) {
                left = i - k + 1;
                right = i + k - 1;
            }
        }

        return best;
    }

    static int maxClearances(int n, int[] categories) throws IOException {
        int[] stack = new int[n];
        int top = 0;

        // 模拟不补货箱时的全部配对清除
        for (int i = 0; i < n; i++) {
            if (top > 0 && stack[top - 1] == categories[i]) {
                top--;
            } else {
                stack[top++] = categories[i];
            }
        }

        int reducedLen = top;
        int base = (n - reducedLen) / 2;

        // 已全部清完，补入单个货箱无法产生新清除
        if (reducedLen == 0) {
            return base;
        }

        int[] reduced = Arrays.copyOf(stack, reducedLen);
        int extra = oddPalindromeRadius(reduced, reducedLen);

        return base + extra;
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner();
        StringBuilder sb = new StringBuilder();

        int T = fs.nextInt();

        for (int tc = 0; tc < T; tc++) {
            int n = fs.nextInt();
            int[] categories = new int[n];

            for (int i = 0; i < n; i++) {
                categories[i] = fs.nextInt();
            }

            sb.append(maxClearances(n, categories)).append('\n');
        }

        System.out.print(sb.toString());
    }
}
