import java.util.HashMap;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        int n = scanner.nextInt();
        int Q = scanner.nextInt(); // 读取 n 和 Q 的值

        // 使用 HashMap 存储每个数字及其出现的位置
        Map<Integer, List<Integer>> positions = new HashMap<>();
        for(int i = 0; i < n; i++) {
            int num = scanner.nextInt();
            positions.computeIfAbsent(num, k -> new ArrayList<>()).add(i + 1); // 位置从1开始
        }

        // 处理每个查询
        for(int i = 0; i < Q; i++) {
            int x = scanner.nextInt();
            int k = scanner.nextInt();
            
            if(positions.containsKey(x) && positions.get(x).size() >= k) {
                System.out.println(positions.get(x).get(k - 1));
            } else {
                System.out.println(-1);
            }
        }

        scanner.close();
    }
}
