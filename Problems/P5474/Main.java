import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.StringTokenizer;

public class Main {
    // 排序 + 前缀和：每次任务用二分切出小于/大于目标档的两段
    static long[] minOps(long[] values, long[] targets) {
        int m = values.length;
        long[] arr = values.clone();
        Arrays.sort(arr);
        long[] pref = new long[m + 1];
        for (int i = 0; i < m; i++) {
            pref[i + 1] = pref[i] + arr[i];
        }
        // 奇偶个数固定，用来把绝对值之和改成向下取整后的之和
        int odd = 0;
        for (int i = 0; i < m; i++) {
            if ((arr[i] & 1) == 1) {
                odd++;
            }
        }
        int even = m - odd;
        long[] ans = new long[targets.length];
        for (int qi = 0; qi < targets.length; qi++) {
            long g = targets[qi];
            int lt = lowerBound(arr, g);
            int gt = upperBound(arr, g);
            long sumLt = pref[lt];
            long sumGt = pref[m] - pref[gt];
            int cntGt = m - gt;
            long sabs = g * lt - sumLt + sumGt - g * cntGt;
            int diff = ((g & 1) == 1) ? even : odd;
            ans[qi] = (sabs - diff) / 2;
        }
        return ans;
    }

    // 第一个 >= x 的下标
    static int lowerBound(long[] arr, long x) {
        int l = 0, r = arr.length;
        while (l < r) {
            int mid = (l + r) >>> 1;
            if (arr[mid] < x) {
                l = mid + 1;
            } else {
                r = mid;
            }
        }
        return l;
    }

    // 第一个 > x 的下标
    static int upperBound(long[] arr, long x) {
        int l = 0, r = arr.length;
        while (l < r) {
            int mid = (l + r) >>> 1;
            if (arr[mid] <= x) {
                l = mid + 1;
            } else {
                r = mid;
            }
        }
        return l;
    }

    public static void main(String[] args) throws IOException {
        // 节点数和偏移可能很长，用 BufferedReader
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int m = Integer.parseInt(br.readLine().trim());
        StringTokenizer st = new StringTokenizer(br.readLine());
        long[] values = new long[m];
        for (int i = 0; i < m; i++) {
            values[i] = Long.parseLong(st.nextToken());
        }
        int k = Integer.parseInt(br.readLine().trim());
        long[] targets = new long[k];
        for (int i = 0; i < k; i++) {
            targets[i] = Long.parseLong(br.readLine().trim());
        }
        long[] ans = minOps(values, targets);
        StringBuilder sb = new StringBuilder();
        // 每项任务单独一行
        for (int i = 0; i < k; i++) {
            sb.append(ans[i]).append('\n');
        }
        System.out.print(sb.toString());
    }
}
