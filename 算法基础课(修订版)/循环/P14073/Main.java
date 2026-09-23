import java.util.ArrayList;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // 输入左边和右边天平的物品数量
        int n = sc.nextInt();
        int m = sc.nextInt();

        // 创建动态数组存储物品重量
        ArrayList<Integer> leftWeights = new ArrayList<>();
        ArrayList<Integer> rightWeights = new ArrayList<>();

        // 输入左边天平物品的重量
        for (int i = 0; i < n; i++) {
            leftWeights.add(sc.nextInt());
        }

        // 输入右边天平物品的重量
        for (int i = 0; i < m; i++) {
            rightWeights.add(sc.nextInt());
        }

        // 计算左边总重量
        int leftTotal = 0;
        for (int weight : leftWeights) {
            leftTotal += weight;
        }

        // 计算右边总重量
        int rightTotal = 0;
        for (int weight : rightWeights) {
            rightTotal += weight;
        }

        // 比较两个天平的总重量并输出结果
        if (leftTotal == rightTotal) {
            System.out.println("Equal");
        } else {
            System.out.println("Not Equal");
        }

        sc.close();
    }
}
