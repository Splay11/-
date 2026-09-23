import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int t = sc.nextInt();  // 读取测试用例数量
        List<Long> results = new ArrayList<>();  // 使用 long 存储结果

        while (t-- > 0) {
            int n = sc.nextInt();
            int k = sc.nextInt();  // 读取每个测试用例的n和k

            int[] a = new int[n];
            for (int i = 0; i < n; ++i) {
                a[i] = sc.nextInt();  // 读取数组a
            }

            // 初始化必要的变量
            final long MIN_VALUE = -10000;  // 使用 Long.MIN_VALUE 作为最小值
            long[] dp = new long[n + 2];
            Arrays.fill(dp, MIN_VALUE);  // 初始化 dp 数组
            long[] pre = new long[n + 2];
            Arrays.fill(pre, MIN_VALUE);  // 初始化 pre 数组
            long[] udp = new long[n + 2];
            Arrays.fill(udp, MIN_VALUE);  // 初始化 udp 数组
            long[] suf = new long[n + 2];
            Arrays.fill(suf, MIN_VALUE);  // 初始化 suf 数组

            // 计算最大子段和（前缀）
            for (int i = 1; i <= n; ++i) {
                dp[i] = Math.max(a[i - 1], dp[i - 1] + a[i - 1]);
            }

            // 计算最大子段和的前缀最大值
            for (int i = 1; i <= n; ++i) {
                pre[i] = Math.max(dp[i], pre[i - 1]);
            }

            // 计算最大子段和（后缀）
            for (int i = n; i >= 1; --i) {
                udp[i] = Math.max(a[i - 1], udp[i + 1] + a[i - 1]);
            }

            // 计算最大子段和（后缀部分）
            for (int i = n; i >= 1; --i) {
                suf[i] = Math.max(suf[i + 1], udp[i]);
            }

            // 计算最终结果
            long res = MIN_VALUE;
            for (int i = 1; i <= n - k; ++i) {
                res = Math.max(res, pre[i] + suf[i + k + 1]);
            }

            results.add(res);  // 将结果保存
        }

        // 输出所有结果
        for (long result : results) {
            System.out.println(result);
        }

        sc.close();
    }
}
