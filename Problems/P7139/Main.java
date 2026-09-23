import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    // 从 [left,right] 向两边扩张，统计以这里为中心的回文个数
    static int expand(String s, int left, int right) {
        int n = s.length();
        int cnt = 0;
        while (left >= 0 && right < n && s.charAt(left) == s.charAt(right)) {
            cnt++;
            left--;
            right++;
        }
        return cnt;
    }

    // 枚举每个中心：奇数中心是一个字符，偶数中心在两个字符之间
    static int solve(String s) {
        int n = s.length();
        int ans = 0;
        for (int i = 0; i < n; i++) {
            // 以 s[i] 为中心的奇数回文
            ans += expand(s, i, i);
            // 以 s[i] 和 s[i+1] 缝为中心的偶数回文
            ans += expand(s, i, i + 1);
        }
        return ans;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        // 一整行就是字符串 s
        String s = br.readLine();
        System.out.println(solve(s));
    }
}
