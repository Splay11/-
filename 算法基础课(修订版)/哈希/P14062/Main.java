import java.util.*;

public class Main {
    
    public static int countPairs(int n, int[] p) {
        // 创建一个哈希表，用于记录 p_i - i 出现的次数
        Map<Integer, Integer> diffCount = new HashMap<>();
        int result = 0;

        // 遍历数组
        for (int j = 0; j < n; ++j) {
            // 计算 j - p_j
            int diff = (j + 1) - p[j];
            // 如果 -diff 已经出现过，那么就说明存在符合条件的 i
            if (diffCount.containsKey(-diff)) {
                result += diffCount.get(-diff);  // 找到符合条件的 i
            }

            // 更新 diffCount
            diffCount.put(diff, diffCount.getOrDefault(diff, 0) + 1);
        }

        return result;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        // 输入读取
        int n = scanner.nextInt();
        int[] p = new int[n];
        
        // 输入数组 p 的元素
        for (int i = 0; i < n; ++i) {
            p[i] = scanner.nextInt();
        }

        // 调用函数并输出结果
        System.out.println(countPairs(n, p));
        
        scanner.close();
    }
}
