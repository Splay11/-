import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.ArrayDeque;
import java.util.Deque;

public class Main {
    // 用栈处理括号，线性扫一遍表达式
    static long solve(String s) {
        Deque<Long> stack = new ArrayDeque<>();
        long res = 0;
        long sign = 1;
        int n = s.length();
        int i = 0;
        while (i < n) {
            char c = s.charAt(i);
            if (c == ' ') {
                // 空格没有意义，直接跳过
                i++;
                continue;
            }
            if (c >= '0' && c <= '9') {
                // 把连续数字拼成一个整数
                long num = 0;
                while (i < n && s.charAt(i) >= '0' && s.charAt(i) <= '9') {
                    num = num * 10 + (s.charAt(i) - '0');
                    i++;
                }
                res += sign * num;
                continue;
            }
            if (c == '+') {
                // 加号只能当二元运算符，下一个项取正
                sign = 1;
                i++;
                continue;
            }
            if (c == '-') {
                // 减号既可二元也可一元，效果都是下一个项取负
                sign = -1;
                i++;
                continue;
            }
            if (c == '(') {
                // 进入新括号层：外层结果和括号前符号先存起来
                stack.addLast(res);
                stack.addLast(sign);
                res = 0;
                sign = 1;
                i++;
                continue;
            }
            // 右括号：用括号前符号把内层结果并回外层
            long prevSign = stack.removeLast();
            long prevRes = stack.removeLast();
            res = prevRes + prevSign * res;
            i++;
        }
        return res;
    }

    public static void main(String[] args) throws IOException {
        // 表达式含空格，必须整行读入
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        System.out.println(solve(s));
    }
}
