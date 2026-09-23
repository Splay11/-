import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    // 维护未匹配左括号数量的可能区间 [lo, hi]
    static boolean solve(String s) {
        int lo = 0;
        int hi = 0;
        int n = s.length();
        for (int i = 0; i < n; i++) {
            char c = s.charAt(i);
            if (c == '(') {
                lo++;
                hi++;
            } else if (c == ')') {
                lo--;
                hi--;
            } else {
                // 星号：当右括号 / 空 / 左括号，区间向两边扩
                lo--;
                hi++;
            }
            if (hi < 0) {
                // 右括号已经多到星号也救不了
                return false;
            }
            if (lo < 0) {
                lo = 0;
            }
        }
        // 扫完后还要能把所有左括号配平
        return lo == 0;
    }

    public static void main(String[] args) throws IOException {
        // 一整行只有括号和星号
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        System.out.println(solve(s) ? "true" : "false");
    }
}
