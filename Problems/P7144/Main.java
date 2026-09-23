import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    // 只有 a e i o u，y 不算
    static boolean isVowel(char c) {
        return c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u';
    }

    // 扫一遍连续元音段，更长才更新，平局保留先出现的
    static String solve(String s) {
        String best = "";
        int n = s.length();
        int i = 0;
        while (i < n) {
            if (!isVowel(s.charAt(i))) {
                i++;
                continue;
            }
            int j = i;
            while (j < n && isVowel(s.charAt(j))) {
                j++;
            }
            // 严格更长才换，避免平局取到后面那段
            if (j - i > best.length()) {
                best = s.substring(i, j);
            }
            i = j;
        }
        if (best.isEmpty()) {
            return "-1";
        }
        return best;
    }

    public static void main(String[] args) throws IOException {
        // 一整行小写字母
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        System.out.println(solve(s));
    }
}
