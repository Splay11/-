import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    // [l, r) 是否全是数字且非空
    static boolean isDigits(String s, int l, int r) {
        if (l >= r) {
            return false;
        }
        for (int i = l; i < r; i++) {
            char c = s.charAt(i);
            if (c < '0' || c > '9') {
                return false;
            }
        }
        return true;
    }

    // 整数：可选正负号，后面至少一位数字
    static boolean isInteger(String s) {
        if (s.isEmpty()) {
            return false;
        }
        int i = 0;
        if (s.charAt(0) == '+' || s.charAt(0) == '-') {
            i = 1;
        }
        return isDigits(s, i, s.length());
    }

    // 小数：可选正负号，后面是 digits. / digits.digits / .digits
    static boolean isDecimal(String s) {
        if (s.isEmpty()) {
            return false;
        }
        int i = 0;
        if (s.charAt(0) == '+' || s.charAt(0) == '-') {
            i = 1;
        }
        int dot = -1;
        for (int j = i; j < s.length(); j++) {
            if (s.charAt(j) == '.') {
                if (dot != -1) {
                    return false;
                }
                dot = j;
            }
        }
        if (dot == -1) {
            return false;
        }
        boolean left = isDigits(s, i, dot);
        boolean right = isDigits(s, dot + 1, s.length());
        // 小数点两侧不能都没有数字
        return left || right;
    }

    // 有效数字 =（整数或小数）后面可以跟一个指数 e/E + 整数
    static boolean valid(String s) {
        int epos = -1;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == 'e' || c == 'E') {
                if (epos != -1) {
                    return false;
                }
                epos = i;
            }
        }
        if (epos == -1) {
            return isInteger(s) || isDecimal(s);
        }
        String left = s.substring(0, epos);
        String right = s.substring(epos + 1);
        if (left.isEmpty() || right.isEmpty()) {
            return false;
        }
        return (isInteger(left) || isDecimal(left)) && isInteger(right);
    }

    static String solve(String s) {
        return valid(s) ? "true" : "false";
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        System.out.println(solve(s));
    }
}
