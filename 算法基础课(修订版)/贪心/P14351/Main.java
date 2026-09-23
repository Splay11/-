import java.util.*;

public class Main {

    public static long getMaxAestheticValue(int n, int m, int[] a, int[] b, int[] c) {
        List<List<Integer>> idx = new ArrayList<>();
        for (int i = 0; i <= m; i++) {
            idx.add(new ArrayList<>());
        }
        for (int i = 0; i < n; i++) {
            idx.get(a[i]).add(i);
        }

        long totalValue = 0; // 使用 long 以防止溢出

        for (List<Integer> lst : idx) {
            if (lst.isEmpty()) continue;

            // 按 (b[i] - c[i]) 降序排序
            lst.sort((x, y) -> Integer.compare((b[y] - c[y]), (b[x] - c[x])));

            // 处理第一个物品，选择 b[i] 或 c[i] 中较大值
            totalValue += Math.max(b[lst.get(0)], c[lst.get(0)]);

            // 处理剩余物品，全部选择不贴标签的美观值 c[i]
            for (int i = 1; i < lst.size(); i++) {
                totalValue += c[lst.get(i)];
            }
        }

        return totalValue;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int m = scanner.nextInt();
        int[] a = new int[n];
        int[] b = new int[n];
        int[] c = new int[n];

        for (int i = 0; i < n; i++) {
            a[i] = scanner.nextInt();
        }
        for (int i = 0; i < n; i++) {
            b[i] = scanner.nextInt();
        }
        for (int i = 0; i < n; i++) {
            c[i] = scanner.nextInt();
        }

        long result = getMaxAestheticValue(n, m, a, b, c);
        System.out.println(result);
        scanner.close();
    }
}
