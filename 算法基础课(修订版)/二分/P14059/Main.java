import java.util.*;

public class Main {
    // check函数：判断当前值是否符合条件
    public static boolean check(int i, List<Integer> R, int cnt) {
        long su = 0;
        for (int x : R) {
            su += Math.min(i, x);
        }
        return su <= cnt;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // 读入数组R
        List<Integer> R = new ArrayList<>();
        String line = sc.nextLine();
        Scanner lineScanner = new Scanner(line);
        while (lineScanner.hasNextInt()) {
            R.add(lineScanner.nextInt());
        }

        // 读入cnt
        int cnt = sc.nextInt();

        // 二分查找的边界
        int l = 0, r = (int) 1e9;

        // 二分查找
        while (l <= r) {
            int mid = (l + r) >> 1;
            if (check(mid, R, cnt)) {
                l = mid + 1;
            } else {
                r = mid - 1;
            }
        }

        // 这种情况即题目描述的第一种情况，右端点不会动
        if (r == (int) 1e9) {
            r = -1;
        }

        // 输出结果
        System.out.println(r);
        sc.close();
    }
}
