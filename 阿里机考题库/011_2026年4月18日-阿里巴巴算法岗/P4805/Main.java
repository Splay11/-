import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.Arrays;
import java.util.StringTokenizer;

public class Main {
    static class Scanner {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st;

        String next() throws IOException {
            while (st == null || !st.hasMoreTokens()) {
                st = new StringTokenizer(br.readLine());
            }
            return st.nextToken();
        }

        int nextInt() throws IOException {
            return Integer.parseInt(next());
        }
    }

    static long solveCase(int m, int[] vals) {
        // 按优先级分值从小到大排序，再从末尾模拟轮流取最大值
        Arrays.sort(vals);

        long teamA = 0;
        long teamB = 0;
        boolean aTurn = true;

        for (int i = m - 1; i >= 0; i--) {
            if (aTurn) {
                teamA += vals[i];
            } else {
                teamB += vals[i];
            }
            aTurn = !aTurn;
        }

        return teamA - teamB;
    }

    public static void main(String[] args) throws Exception {
        Scanner sc = new Scanner();
        StringBuilder sb = new StringBuilder();

        int T = sc.nextInt();
        while (T-- > 0) {
            int m = sc.nextInt();
            int[] vals = new int[m];
            for (int i = 0; i < m; i++) {
                vals[i] = sc.nextInt();
            }
            sb.append(solveCase(m, vals)).append('\n');
        }

        System.out.print(sb.toString());
    }
}
