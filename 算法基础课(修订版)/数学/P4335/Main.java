import java.util.*;

/**
 * ACM 风格主类 Main
 */
public class Main {

    // 功能函数：返回 [k_min, k_max]；若无解返回 null
    static int[] solveCase(int n, int l, int r) {
        // 向上取整 l/n = (l + n - 1) / n；向下取整 r/n = r / n
        int kMin = (l + n - 1) / n;
        int kMax = r / n;
        if (kMin > kMax) return null;
        return new int[]{kMin, kMax};
    }

    public static void main(String[] args) {
        // 题目数据量很小，使用 Scanner 即可
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int T = sc.nextInt();
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < T; i++) {
            int n = sc.nextInt();
            int l = sc.nextInt();
            int r = sc.nextInt();
            int[] res = solveCase(n, l, r);
            if (res == null) {
                sb.append("-1");
            } else {
                sb.append(res[0]).append(" ").append(res[1]);
            }
            if (i + 1 < T) sb.append('\n');
        }
        System.out.print(sb.toString());
        sc.close();
    }
}
