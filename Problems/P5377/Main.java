import java.util.Arrays;
import java.util.Scanner;

public class Main {
    // 每人价值都是 1，按驻场总耗材从小到大批准
    static int maxAccept(int n, long b, int[] v) {
        long[] costs = new long[n];
        for (int i = 0; i < n; i++) {
            // 下标从 0 计：从当天到第 n 天共 (n-i) 天
            costs[i] = (long) v[i] * (n - i);
        }
        Arrays.sort(costs);
        long used = 0;
        int ans = 0;
        for (int i = 0; i < n; i++) {
            if (used + costs[i] <= b) {
                used += costs[i];
                ans++;
            } else {
                break;
            }
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        long b = sc.nextLong();
        int[] v = new int[n];
        for (int i = 0; i < n; i++) {
            v[i] = sc.nextInt();
        }
        System.out.println(maxAccept(n, b, v));
        sc.close();
    }
}
