import java.util.Scanner;

public class Main {
    // 判断是否能通过合成满足 mid 套红、蓝、绿三种砖块
    public static boolean check(int a, int b, int c, int x, int y, int mid) {
        int a1 = a, b1 = b, c1 = c;
        
        // 尝试从红砖合成蓝砖
        if (a1 > mid) {
            int f = (a1 - mid) / x; // 计算多余的红砖能合成多少蓝砖
            a1 -= f * x;            // 消耗这些多余的红砖
            b1 += f;                // 增加对应的蓝砖数量
        }
        
        // 尝试从蓝砖合成绿砖
        if (b1 > mid) {
            int f = (b1 - mid) / y; // 计算多余的蓝砖能合成多少绿砖
            b1 -= f * y;            // 消耗这些多余的蓝砖
            c1 += f;                // 增加对应的绿砖数量
        }
        
        return (a1 >= mid && b1 >= mid && c1 >= mid);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int T = sc.nextInt(); // 测试数据的组数
        
        while (T-- > 0) {
            // 读取每组数据
            int a = sc.nextInt(); // 红砖数量
            int b = sc.nextInt(); // 蓝砖数量
            int c = sc.nextInt(); // 绿砖数量
            int x = sc.nextInt(); // 红->蓝 合成比例
            int y = sc.nextInt(); // 蓝->绿 合成比例
            
            // 二分查找的左、右边界
            int l = 0;
            int r = 1000000000; 
            
            // 二分查找
            while (l < r) {
                int mid = (l + r + 1) / 2; // 取上中位数
                if (check(a, b, c, x, y, mid)) {
                    l = mid;     // 如果能满足 mid 套，则尝试更大的 mid
                } else {
                    r = mid - 1; // 否则缩小范围
                }
            }
            
            // 输出最终可以收集到的最大套数
            System.out.println(l);
        }
        
        sc.close();
    }
}
