import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        // 读取数组长度
        int n = scanner.nextInt();
        int[] arr = new int[n];
        
        // 读取数组元素
        for (int i = 0; i < n; ++i) {
            arr[i] = scanner.nextInt();
        }
        
        // 读取查询次数
        int q = scanner.nextInt();
        while (q-- > 0) {
            int l = scanner.nextInt();
            int r = scanner.nextInt();
            l--; // 转换为0开始的索引
            r--;
            
            int maxValue = arr[l];
            List<Integer> maxIndices = new ArrayList<>();
            maxIndices.add(l + 1); // 记录第一个元素的下标（转为1开始）
            
            // 找到最大值和下标
            for (int i = l + 1; i <= r; ++i) {
                if (arr[i] > maxValue) {
                    maxValue = arr[i];
                    maxIndices.clear(); // 清空之前的下标
                    maxIndices.add(i + 1); // 记录当前最大值下标（转为1开始）
                } else if (arr[i] == maxValue) {
                    maxIndices.add(i + 1); // 记录当前最大值下标
                }
            }
            
            // 输出结果
            System.out.println(maxValue);
            for (int i = 0; i < maxIndices.size(); ++i) {
                System.out.print(maxIndices.get(i));
                if (i != maxIndices.size() - 1) {
                    System.out.print(" ");
                }
            }
            System.out.println();
        }
        
        scanner.close();
    }
}
