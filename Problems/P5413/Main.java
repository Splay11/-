import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static final int MOD = 1000000007;

    // 用单调栈求左右最近严格更大元素，距离超过 k 则该侧贡献为 0
    static int totalInterference(int[] power, int k) {
        int n = power.length;

        // ngeLeft[i]：i 左侧最近且严格更大的下标；没有则为 -1
        int[] ngeLeft = new int[n];
        int[] stack = new int[n];
        int top = 0;
        for (int i = 0; i < n; i++) {
            ngeLeft[i] = -1;
            // 栈里只保留比当前值更大的候选，栈顶就是最近的那个
            while (top > 0 && power[stack[top - 1]] <= power[i]) {
                top--;
            }
            if (top > 0) {
                ngeLeft[i] = stack[top - 1];
            }
            stack[top++] = i;
        }

        // ngeRight[i]：i 右侧最近且严格更大的下标；没有则为 -1
        int[] ngeRight = new int[n];
        top = 0;
        for (int i = 0; i < n; i++) {
            ngeRight[i] = -1;
            // 当前值能作为栈中更小元素的「右侧第一个更大」
            while (top > 0 && power[stack[top - 1]] < power[i]) {
                ngeRight[stack[--top]] = i;
            }
            stack[top++] = i;
        }

        long ans = 0;
        for (int i = 0; i < n; i++) {
            int left = ngeLeft[i];
            // 最近更大元素必须落在长度为 k 的搜索窗口内
            if (left != -1 && i - left <= k) {
                ans = (ans + (long) power[i] * (i - left)) % MOD;
            }
            int right = ngeRight[i];
            if (right != -1 && right - i <= k) {
                ans = (ans + (long) power[i] * (right - i)) % MOD;
            }
        }
        return (int) ans;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        // 第一行：全部基站强度，n 由元素个数得到
        String[] parts = br.readLine().trim().split(" ");
        int n = parts.length;
        int[] power = new int[n];
        for (int i = 0; i < n; i++) {
            power[i] = Integer.parseInt(parts[i]);
        }
        // 第二行：最多向一侧搜索的基站个数
        int k = Integer.parseInt(br.readLine().trim());
        System.out.println(totalInterference(power, k));
    }
}
