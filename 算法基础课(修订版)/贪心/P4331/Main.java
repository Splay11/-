import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int T = sc.nextInt();
        while (T-- > 0) {
            int n = sc.nextInt();
            long[] a = new long[n];
            long[] c = new long[n];
            for (int i = 0; i < n; i++) a[i] = sc.nextLong();
            for (int i = 0; i < n; i++) c[i] = sc.nextLong();

            // 点赞值 -> 杂乱度列表
            Map<Long, List<Long>> mp = new HashMap<>();
            for (int i = 0; i < n; i++) {
                mp.computeIfAbsent(a[i], k -> new ArrayList<>()).add(c[i]);
            }

            // 每组排序
            for (List<Long> lst : mp.values()) {
                Collections.sort(lst);
            }

            // 点赞值有序
            List<Long> keys = new ArrayList<>(mp.keySet());
            Collections.sort(keys);

            long ans = 0;
            while (!keys.isEmpty()) {
                while (!keys.isEmpty() && !mp.containsKey(keys.get(keys.size() - 1))) {
                    keys.remove(keys.size() - 1);
                }
                if (keys.isEmpty()) break;

                long curMax = 0;
                for (int i = keys.size() - 1; i >= 0; i--) {
                    if (i != keys.size() - 1 && keys.get(i) != keys.get(i + 1) - 1) break;
                    if (!mp.containsKey(keys.get(i))) break;
                    List<Long> lst = mp.get(keys.get(i));
                    curMax = Math.max(curMax, lst.remove(lst.size() - 1));
                    if (lst.isEmpty()) mp.remove(keys.get(i));
                }
                ans += curMax;
            }

            System.out.println(ans);
        }
    }
}
