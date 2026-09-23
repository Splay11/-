import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Scanner;

public class Main {
    // 用栈做最近未匹配开启桩配对，统计内部长度能被 m 整除的舱段数
    static long countCabin(int n, int m, String t) {
        // 栈里存尚未配对的 '(' 下标（从 0 起）
        Deque<Integer> st = new ArrayDeque<Integer>();
        long ans = 0;
        for (int i = 0; i < n; i++) {
            if (t.charAt(i) == '(') {
                // 开启桩入栈，等待之后最近的闭合桩来配对
                st.push(i);
            } else {
                // 闭合桩与栈顶（左侧最近未匹配开启桩）配对
                int left = st.pop();
                // 内部长度 = 两端下标差再减 1，即中间桩标个数
                int inner = i - left - 1;
                if (inner % m == 0) {
                    ans++;
                }
            }
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int m = sc.nextInt();
        String t = sc.next();
        System.out.println(countCabin(n, m, t));
        sc.close();
    }
}
