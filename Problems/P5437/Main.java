import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    // 判定是否存在长度至少为 w 的窗口，使向下取整后的班均 >= x
    static boolean feasible(long[] vals, int w, long x) {
        int m = vals.length;
        long[] pre = new long[m + 1];
        for (int i = 0; i < m; i++) {
            // 前缀用 long，避免 n * 2e9 溢出
            pre[i + 1] = pre[i] + (vals[i] - x);
        }
        // mn 维护 pre[0..r-w] 的最小值
        long mn = Long.MAX_VALUE / 4;
        for (int r = w; r <= m; r++) {
            if (pre[r - w] < mn) {
                mn = pre[r - w];
            }
            if (pre[r] - mn >= 0) {
                return true;
            }
        }
        return false;
    }

    // 二分最大班均净值
    static long maxFloorAvg(long[] vals, int w) {
        long lo = vals[0];
        long hi = vals[0];
        for (int i = 1; i < vals.length; i++) {
            if (vals[i] < lo) {
                lo = vals[i];
            }
            if (vals[i] > hi) {
                hi = vals[i];
            }
        }
        long ans = lo;
        while (lo <= hi) {
            long mid = lo + (hi - lo) / 2;
            if (feasible(vals, w, mid)) {
                ans = mid;
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
        return ans;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int g = Integer.parseInt(br.readLine().trim());
        StringBuilder sb = new StringBuilder();
        for (int t = 0; t < g; t++) {
            int m = Integer.parseInt(br.readLine().trim());
            int w = Integer.parseInt(br.readLine().trim());
            // 第三行逗号分隔
            String[] parts = br.readLine().trim().split(",");
            long[] vals = new long[m];
            for (int i = 0; i < m; i++) {
                vals[i] = Long.parseLong(parts[i].trim());
            }
            if (t > 0) {
                sb.append(' ');
            }
            sb.append(maxFloorAvg(vals, w));
        }
        System.out.println(sb.toString());
    }
}
