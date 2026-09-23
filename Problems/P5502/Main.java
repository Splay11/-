import java.util.ArrayList;
import java.util.Scanner;

public class Main {
    static ArrayList<Long> findElements(long[] a) {
        int n = a.length;
        // prefMax[i] = a[0..i] 的最大值
        long[] prefMax = new long[n];
        prefMax[0] = a[0];
        for (int i = 1; i < n; i++) {
            prefMax[i] = a[i] > prefMax[i - 1] ? a[i] : prefMax[i - 1];
        }
        // sufMin[i] = a[i..n-1] 的最小值
        long[] sufMin = new long[n];
        sufMin[n - 1] = a[n - 1];
        for (int i = n - 2; i >= 0; i--) {
            sufMin[i] = a[i] < sufMin[i + 1] ? a[i] : sufMin[i + 1];
        }
        ArrayList<Long> ans = new ArrayList<Long>();
        for (int i = 0; i < n; i++) {
            // 比左边都大、比右边都小（严格比较）
            boolean leftOk = (i == 0) || (a[i] > prefMax[i - 1]);
            boolean rightOk = (i == n - 1) || (a[i] < sufMin[i + 1]);
            if (leftOk && rightOk) {
                ans.add(a[i]);
            }
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        long[] a = new long[n];
        for (int i = 0; i < n; i++) {
            a[i] = sc.nextLong();
        }
        ArrayList<Long> ans = findElements(a);
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < ans.size(); i++) {
            if (i > 0) {
                sb.append(' ');
            }
            sb.append(ans.get(i));
        }
        System.out.println(sb.toString());
        sc.close();
    }
}
