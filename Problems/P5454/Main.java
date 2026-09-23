import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class Main {
    // 枚举每个探测原点，按平方距离分桶，同一桶内 c 个点贡献 c*(c-1) 组有序对
    static long countEquidistant(int[][] loc) {
        int m = loc.length;
        long ans = 0;
        // 复用同一张表，避免每轮 new HashMap 把内存顶满
        Map<Long, Integer> buckets = new HashMap<>();
        // 每个点都当一次探测原点
        for (int p = 0; p < m; p++) {
            buckets.clear();
            int ux = loc[p][0];
            int uy = loc[p][1];
            for (int q = 0; q < m; q++) {
                if (p == q) {
                    continue;
                }
                // 先转成 long 再乘，否则 dx*dx 在 int 里会溢出
                long dx = (long) loc[q][0] - ux;
                long dy = (long) loc[q][1] - uy;
                long d2 = dx * dx + dy * dy;
                buckets.put(d2, buckets.getOrDefault(d2, 0) + 1);
            }
            // 同一距离有 c 个点：有序对 (q, r) 共 c*(c-1) 种
            for (int c : buckets.values()) {
                ans += (long) c * (c - 1);
            }
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int m = sc.nextInt();
        int[][] loc = new int[m][2];
        // 读入 m 座雷达站的坐标
        for (int i = 0; i < m; i++) {
            loc[i][0] = sc.nextInt();
            loc[i][1] = sc.nextInt();
        }
        sc.close();
        System.out.println(countEquidistant(loc));
    }
}
