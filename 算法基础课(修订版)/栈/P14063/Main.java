import java.util.*;
import java.io.*;

public class Main {
    // 计算整数n的十六进制表示中各位数字的和
    private static int computeWeight(int n) {
        if (n == 0) return 0;
        int s = 0;
        while (n > 0) {
            int digit = n & 0xF;  // 获取最低四位
            s += digit;
            n >>= 4;  // 右移四位，处理下一个十六进制数字
        }
        return s;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        
        // 读取数组大小
        int N = Integer.parseInt(br.readLine());
        
        // 读取数组
        int[] arr = new int[N];
        String[] inputs = br.readLine().split(" ");
        for (int i = 0; i < N; i++) {
            arr[i] = Integer.parseInt(inputs[i]);
        }
        
        // 计算权重
        int[] weights = new int[N];
        for (int i = 0; i < N; i++) {
            weights[i] = computeWeight(arr[i]);
        }
        
        // 初始化答案数组
        int[] answer = new int[N];
        Arrays.fill(answer, -1);
        
        // 使用栈进行处理
        Deque<Integer> stack = new ArrayDeque<>();
        
        // 从右到左遍历
        for (int i = N - 1; i >= 0; i--) {
            while (!stack.isEmpty() && weights[stack.peek()] <= weights[i]) {
                stack.pop();
            }
            if (!stack.isEmpty()) {
                answer[i] = stack.peek();
            }
            stack.push(i);
        }
        
        // 输出结果
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < N; i++) {
            sb.append(answer[i]);
            if (i < N - 1) {
                sb.append(" ");
            }
        }
        System.out.println(sb);
    }
}
