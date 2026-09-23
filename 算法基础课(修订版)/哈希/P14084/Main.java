import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        int n = scanner.nextInt();
        Map<Integer, Integer> counts = new HashMap<>();  // 哈希表，记录每个数字的出现次数
        StringBuilder sb = new StringBuilder();          // 用于高效地构建输出字符串
        
        for (int i = 1; i <= n; ++i) {
            int num = scanner.nextInt();
            counts.put(num, counts.getOrDefault(num, 0) + 1);  // 更新数字 num 的出现次数
            
            // 直接获取数字 i 在前缀 [a1, a2, ..., ai] 中的出现次数
            if (i > 1)
                sb.append(' ');
            sb.append(counts.getOrDefault(i, 0));
        }
        
        System.out.println(sb.toString());  // 一次性输出所有结果
        scanner.close();
    }
}
