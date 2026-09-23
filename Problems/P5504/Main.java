import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Scanner;

public class Main {
    // 单调双端队列求一维窗口最大值
    static long[] slidingMax1d(long[] arr, int k) {
        int n = arr.length;
        long[] res = new long[n - k + 1];
        Deque<Integer> dq = new ArrayDeque<Integer>();
        for (int i = 0; i < n; i++) {
            while (!dq.isEmpty() && arr[dq.peekLast()] <= arr[i]) {
                dq.pollLast();
            }
            dq.addLast(i);
            if (dq.peekFirst() <= i - k) {
                dq.pollFirst();
            }
            if (i >= k - 1) {
                res[i - k + 1] = arr[dq.peekFirst()];
            }
        }
        return res;
    }

    static long[][] windowMax(long[][] mat, int k) {
        int n = mat.length;
        int m = mat[0].length;
        // 先对每一行做长度为 k 的滑动窗口最大值
        long[][] rowMax = new long[n][];
        for (int i = 0; i < n; i++) {
            rowMax[i] = slidingMax1d(mat[i], k);
        }
        int cols = m - k + 1;
        int rows = n - k + 1;
        long[][] ans = new long[rows][cols];
        for (int j = 0; j < cols; j++) {
            long[] col = new long[n];
            for (int i = 0; i < n; i++) {
                col[i] = rowMax[i][j];
            }
            long[] colRes = slidingMax1d(col, k);
            for (int i = 0; i < rows; i++) {
                ans[i][j] = colRes[i];
            }
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int m = sc.nextInt();
        int k = sc.nextInt();
        long[][] mat = new long[n][m];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                mat[i][j] = sc.nextLong();
            }
        }
        long[][] ans = windowMax(mat, k);
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < ans.length; i++) {
            for (int j = 0; j < ans[i].length; j++) {
                if (j > 0) {
                    sb.append(' ');
                }
                sb.append(ans[i][j]);
            }
            sb.append('\n');
        }
        System.out.print(sb.toString());
        sc.close();
    }
}
