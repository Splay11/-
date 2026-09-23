import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int res = 0;
        
        // 使用哈希表存储频率
        Map<Integer, Integer> countLeft = new HashMap<>();
        Map<Integer, Integer> countRight = new HashMap<>();
        
        // 读取数组
        int[] a = new int[n];
        for (int i = 0; i < n; i++) {
            a[i] = scanner.nextInt();
        }
        
        // 初始化 countRight
        for (int i = 0; i < n; i++) {
            countRight.put(a[i], countRight.getOrDefault(a[i], 0) + 1);
        }
        
        // 遍历每个元素，计算符合条件的三元组数量
        for (int i = 0; i < n; i++) {
            int t = a[i] + 1;  // 计算 t = a[j] + 1
            res += countLeft.getOrDefault(t, 0) * countRight.getOrDefault(t, 0);
            
            // 更新 countLeft 和 countRight
            countLeft.put(a[i], countLeft.getOrDefault(a[i], 0) + 1);
            countRight.put(a[i], countRight.get(a[i]) - 1);
        }
        
        // 输出结果
        System.out.println(res);
        
        scanner.close();
    }
}
