import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Scanner;

public class Main {
    static final long INF = 4_000_000_000_000_000_000L;

    // 空队列用一行单独的 0 表示
    static boolean isEmpty(int[] arr) {
        return arr.length == 0 || (arr.length == 1 && arr[0] == 0);
    }

    // 连续放掉不超过 lim，刚好接 t 项的最小耗时
    static long minCost(int[] arr, int t, int lim) {
        int n = arr.length;
        if (n == 0) {
            return 0;
        }
        if (t == 0) {
            return n <= lim ? 0 : -1;
        }
        if (t > n) {
            return -1;
        }
        if (n - t > (long) (t + 1) * lim) {
            return -1;
        }

        long[] dp = new long[n];
        for (int i = 0; i < n; i++) {
            dp[i] = (i <= lim) ? arr[i] : INF;
        }

        // 第 2..t 次接单：上一层下标落在 [i-lim-1, i-1] 内取最小
        for (int k = 2; k <= t; k++) {
            long[] ndp = new long[n];
            for (int i = 0; i < n; i++) {
                ndp[i] = INF;
            }
            Deque<Integer> dq = new ArrayDeque<>();
            for (int i = 0; i < n; i++) {
                int prev = i - 1;
                if (prev >= 0 && dp[prev] < INF) {
                    while (!dq.isEmpty() && dp[dq.peekLast()] >= dp[prev]) {
                        dq.pollLast();
                    }
                    dq.addLast(prev);
                }
                int lo = i - lim - 1;
                while (!dq.isEmpty() && dq.peekFirst() < lo) {
                    dq.pollFirst();
                }
                if (!dq.isEmpty()) {
                    ndp[i] = dp[dq.peekFirst()] + arr[i];
                }
            }
            dp = ndp;
        }

        long ans = INF;
        for (int i = 0; i < n; i++) {
            if (n - 1 - i <= lim && dp[i] < ans) {
                ans = dp[i];
            }
        }
        return ans >= INF ? -1 : ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String first = sc.nextLine().trim();
        if (first.isEmpty()) {
            System.out.println(0);
            sc.close();
            return;
        }
        String[] parts = first.split("\\s+");
        int[] arr = new int[parts.length];
        for (int i = 0; i < parts.length; i++) {
            arr[i] = Integer.parseInt(parts[i]);
        }
        if (isEmpty(arr)) {
            System.out.println(0);
            sc.close();
            return;
        }
        int t = Integer.parseInt(sc.nextLine().trim());
        int lim = Integer.parseInt(sc.nextLine().trim());
        sc.close();
        System.out.println(minCost(arr, t, lim));
    }
}
