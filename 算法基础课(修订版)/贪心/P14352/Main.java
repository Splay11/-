import java.util.Scanner;

public class Main {

    static int[] h;

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        h = new int[n + 1];  // 1-based indexing
        for (int i = 1; i <= n; i++) {
            h[i] = sc.nextInt();
        }
        // 计算并输出最小操作代价
        System.out.println(minCost(1, n));
    }

    // 计算区间 [l, r] 的最小代价
    static int minCost(int l, int r) {
        if (l > r) {
            return 0;
        }
        if (l == r) {
            return 2; // 单个服务器默认为单列操作
        }

        int minH = Integer.MAX_VALUE;
        for (int i = l; i <= r; i++) {
            minH = Math.min(minH, h[i]);
        }

        // 行操作
        int cost1 = 1;
        int i = l;
        while (i <= r) {
            if (h[i] > minH) {
                int start = i;
                while (i <= r && h[i] > minH) {
                    i++;
                }
                cost1 += minCost(start, i - 1);
            } else {
                i++;
            }
        }
        return cost1;
    }
}
