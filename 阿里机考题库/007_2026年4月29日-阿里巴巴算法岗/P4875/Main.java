import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Main {
    static final long MOD = 1000000007L;

    // 计算补全方案数：动态规划，维护最后一段信号字符及其长度的奇偶性
    static long countWays(String s) {
        // odd[c]：最后一段字符为 c，且长度为奇数的方案数
        // even[c]：最后一段字符为 c，且长度为偶数的方案数
        long[] odd = new long[2];
        long[] even = new long[2];

        // 初始化第一个字符
        for (int c = 0; c < 2; c++) {
            char ch = c == 0 ? 'A' : 'B';
            if (s.charAt(0) == '?' || s.charAt(0) == ch) {
                odd[c] = 1;
            }
        }

        // 从第二个字符开始动态规划
        for (int i = 1; i < s.length(); i++) {
            long[] newOdd = new long[2];
            long[] newEven = new long[2];

            for (int c = 0; c < 2; c++) {
                char ch = c == 0 ? 'A' : 'B';
                if (s.charAt(i) != '?' && s.charAt(i) != ch) {
                    continue;
                }

                // 继续放相同字符：当前段长度奇偶性翻转
                newOdd[c] = (newOdd[c] + even[c]) % MOD;
                newEven[c] = (newEven[c] + odd[c]) % MOD;

                // 放不同字符：上一段必须是奇数长度才能开启新段
                newOdd[c] = (newOdd[c] + odd[c ^ 1]) % MOD;
            }

            odd = newOdd;
            even = newEven;
        }

        // 最后一段必须是奇数长度
        return (odd[0] + odd[1]) % MOD;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();

        int T = Integer.parseInt(br.readLine().trim());

        for (int tc = 0; tc < T; tc++) {
            int n = Integer.parseInt(br.readLine().trim());
            String s = br.readLine().trim();

            sb.append(countWays(s)).append('\n');
        }

        System.out.print(sb.toString());
    }
}
