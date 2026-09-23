import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.Locale;

public class Main {
    // 扫描空格与字母段，累加单词长度并计数
    static String solve(String s) {
        long total = 0;
        int cnt = 0;
        int n = s.length();
        int i = 0;
        while (i < n) {
            // 跳过一个或多个空格
            while (i < n && s.charAt(i) == ' ') {
                i++;
            }
            if (i >= n) {
                break;
            }
            int j = i;
            // 连续字母构成一个单词
            while (j < n && s.charAt(j) != ' ') {
                j++;
            }
            total += (j - i);
            cnt++;
            i = j;
        }
        // 用美式小数点，避免本地化成逗号
        return String.format(Locale.US, "%.2f", (double) total / cnt);
    }

    public static void main(String[] args) throws IOException {
        // 句子含空格，整行读入
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        System.out.println(solve(s));
    }
}
