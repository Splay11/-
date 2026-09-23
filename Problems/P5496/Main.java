import java.util.Scanner;

public class Main {
    static int distinctCount(String s) {
        boolean[] seen = new boolean[26];
        int tot = 0;
        for (int i = 0; i < s.length(); i++) {
            int idx = s.charAt(i) - 'a';
            if (!seen[idx]) {
                seen[idx] = true;
                tot++;
            }
        }
        return tot;
    }

    static boolean canSplit(String s, int m, int limit) {
        // 每段不同字母不超过 limit 时，最少要拆成几段；能拆得更碎就不会更差
        int n = s.length();
        int pieces = 0;
        int i = 0;
        while (i < n) {
            pieces++;
            if (pieces > m) {
                return false;
            }
            int[] cnt = new int[26];
            int kinds = 0;
            int j = i;
            // 从 i 尽量往右延伸，直到再加一个字母会超过上限
            while (j < n) {
                int idx = s.charAt(j) - 'a';
                if (cnt[idx] == 0) {
                    if (kinds == limit) {
                        break;
                    }
                    kinds++;
                }
                cnt[idx]++;
                j++;
            }
            if (j == i) {
                return false;
            }
            i = j;
        }
        return true;
    }

    static int minInterference(String s, int m) {
        // 干扰度越大越容易拆进 m 段，二分最小可行上限
        int left = 1;
        int right = distinctCount(s);
        while (left < right) {
            int mid = (left + right) / 2;
            if (canSplit(s, m, mid)) {
                right = mid;
            } else {
                left = mid + 1;
            }
        }
        return left;
    }

    public static void main(String[] args) {
        // 只有一行字符串，Scanner 足够
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int m = sc.nextInt();
        String s = sc.next();
        if (s.length() > n) {
            s = s.substring(0, n);
        }
        System.out.println(minInterference(s, m));
        sc.close();
    }
}
