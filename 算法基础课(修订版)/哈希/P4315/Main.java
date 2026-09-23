import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        StringBuilder out = new StringBuilder();

        int T = sc.nextInt(); // 测试组数
        while (T-- > 0) {
            int n = sc.nextInt(); // 字符串个数

            // 读取第一个字符串并初始化最小频次数组
            String s0 = sc.next();
            int[] mn = new int[26];
            for (int i = 0; i < s0.length(); i++) {
                mn[s0.charAt(i) - 'a']++;
            }

            // 处理剩余的 n-1 个字符串
            for (int i = 1; i < n; i++) {
                String s = sc.next();
                int[] cnt = new int[26];
                for (int j = 0; j < s.length(); j++) {
                    cnt[s.charAt(j) - 'a']++;
                }
                for (int j = 0; j < 26; j++) {
                    if (cnt[j] < mn[j]) mn[j] = cnt[j]; // 取最小值
                }
            }

            // 构造结果串
            StringBuilder ans = new StringBuilder();
            for (int i = 0; i < 26; i++) {
                for (int k = 0; k < mn[i]; k++) {
                    ans.append((char) ('a' + i));
                }
            }
            if (ans.length() == 0) out.append("-1\n");
            else out.append(ans).append("\n");
        }

        System.out.print(out.toString());
    }
}
