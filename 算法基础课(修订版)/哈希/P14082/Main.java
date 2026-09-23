import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

        Scanner scanner = new Scanner(System.in);
        
        int n = scanner.nextInt();
        int Q = scanner.nextInt();
        
        Map<Integer, Integer> countMap = new HashMap<>();
        int num;
        
        // 统计每个数字出现的次数
        for(int i = 0; i < n; i++) {
            num = scanner.nextInt();
            countMap.put(num, countMap.getOrDefault(num, 0) + 1);
        }
        
        // 处理每个查询
        for(int i = 0; i < Q; i++) {
            num = scanner.nextInt();
            System.out.println(countMap.getOrDefault(num, 0));
        }
        
        scanner.close();
    }
}
