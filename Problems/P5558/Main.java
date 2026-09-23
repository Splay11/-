import java.util.Scanner;

public class Main {
    static int longestKeep(String t, int m) {
        // 前缀里浅色 a、深色 b 各有多少颗
        int[] cntA = new int[m + 1];
        int[] cntB = new int[m + 1];
        for (int i = 0; i < m; i++) {
            cntA[i + 1] = cntA[i];
            cntB[i + 1] = cntB[i];
            if (t.charAt(i) == 'a') {
                cntA[i + 1] += 1;
            } else {
                cntB[i + 1] += 1;
            }
        }
        int totalA = cntA[m];
        // bestDiff：左端点不超过当前右端点时，左段 a 个数减左段 b 个数的最大值
        int bestDiff = Integer.MIN_VALUE;
        int ans = 0;
        for (int j = 0; j <= m; j++) {
            int diff = cntA[j] - cntB[j];
            if (diff > bestDiff) {
                bestDiff = diff;
            }
            // 右端点定在 j：中段留满 b，右段留满后面的 a
            int cur = bestDiff + cntB[j] + (totalA - cntA[j]);
            if (cur > ans) {
                ans = cur;
            }
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        // 第一行墨点数，第二行条码
        int m = sc.nextInt();
        String t = sc.next();
        System.out.println(longestKeep(t, m));
        sc.close();
    }
}
