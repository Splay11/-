import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    static class InputReader {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st;

        String next() throws Exception {
            while (st == null || !st.hasMoreTokens()) {
                st = new StringTokenizer(br.readLine());
            }
            return st.nextToken();
        }

        int nextInt() throws Exception {
            return Integer.parseInt(next());
        }

        long nextLong() throws Exception {
            return Long.parseLong(next());
        }
    }

    static long countLeq(long[] load, long limit) {
        int length = load.length;

        // r 为右端点开区间，当前窗口为 [l, r)
        int r = 0;

        // windowSum 为当前窗口内负载之和
        long windowSum = 0;

        // curScore 为当前窗口的段累计分
        long curScore = 0;

        long cnt = 0;

        for (int l = 0; l < length; l++) {
            // 尽量右扩窗口，保证段累计分不超过 limit
            while (r < length) {
                long newSum = windowSum + load[r];
                long newScore = curScore + newSum;

                if (newScore > limit) {
                    break;
                }

                windowSum = newSum;
                curScore = newScore;
                r++;
            }

            cnt += r - l;

            if (r > l) {
                curScore -= (long) (r - l) * load[l];
                windowSum -= load[l];
            } else {
                r = l + 1;
            }
        }

        return cnt;
    }

    static long kthScore(long[] load, long rank) {
        // 上界取整段 [1, length] 的段累计分
        long running = 0;
        long high = 0;

        for (long x : load) {
            running += x;
            high += running;
        }

        long low = 0;

        // 二分最小的 ans，使 score <= ans 的区间数不少于 rank
        while (low < high) {
            long mid = low + (high - low) / 2;

            if (countLeq(load, mid) >= rank) {
                high = mid;
            } else {
                low = mid + 1;
            }
        }

        return low;
    }

    public static void main(String[] args) throws Exception {
        InputReader in = new InputReader();
        StringBuilder sb = new StringBuilder();

        int tc = in.nextInt();

        for (int caseId = 0; caseId < tc; caseId++) {
            int length = in.nextInt();
            long rank = in.nextLong();

            long[] load = new long[length];
            for (int i = 0; i < length; i++) {
                load[i] = in.nextLong();
            }

            sb.append(kthScore(load, rank)).append('\n');
        }

        System.out.print(sb.toString());
    }
}
