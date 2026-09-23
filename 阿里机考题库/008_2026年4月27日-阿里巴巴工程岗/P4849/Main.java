import java.util.*;

public class Main {
    static final long MOD = 1000000007L;

    static long segmentContribution(long len) {
        // 长度为 len 的合规差分段贡献 len*(len-1)*(len+1)/6
        return len * (len - 1) * (len + 1) / 6;
    }

    static long countTurnPoints(int m, long[] readings) {
        if (m < 3) {
            return 0;
        }

        long total = 0;
        long runLen = 1; // 当前合规差分段长度

        for (int i = 1; i < m - 1; i++) {
            long deltaLeft = readings[i] - readings[i - 1];
            long deltaRight = readings[i + 1] - readings[i];
            // 相邻差分异号或含零，说明该内部测点是拐点
            if (deltaLeft * deltaRight <= 0) {
                runLen++;
            } else {
                total = (total + segmentContribution(runLen)) % MOD;
                runLen = 1;
            }
        }

        total = (total + segmentContribution(runLen)) % MOD;
        return total;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int T = sc.nextInt();
        StringBuilder sb = new StringBuilder();

        while (T-- > 0) {
            int m = sc.nextInt();
            long[] readings = new long[m];

            for (int i = 0; i < m; i++) {
                readings[i] = sc.nextLong();
            }

            sb.append(countTurnPoints(m, readings)).append('\n');
        }

        System.out.print(sb.toString());
        sc.close();
    }
}
