import java.util.*;

public class Main {
    
    static int jobNum;
    static int[] times = new int[30];
    static Map<Integer, Set<Integer>> mutex = new HashMap<>();
    static int ans = 1;
    static int cost = Integer.MAX_VALUE;

    // 检查任务是否与已选择任务组冲突
    public static boolean check(int i, Set<Integer> usd) {
        for (int u : usd) {
            if (mutex.getOrDefault(u, new HashSet<>()).contains(i) || mutex.getOrDefault(i, new HashSet<>()).contains(u)) {
                return false;
            }
        }
        return true;
    }

    // DFS递归处理
    public static void dfs(int i, Set<Integer> usd, int time) {
        if (i >= jobNum) {
            if (ans <= usd.size()) {
                if (ans < usd.size()) {
                    ans = usd.size();
                    cost = time;
                } else if (ans == usd.size()) {
                    if (time < cost) {
                        cost = time;
                    }
                }
            }
            return;
        }
        if (usd.size() + jobNum - i + 1 < ans) return ;
        dfs(i + 1, usd, time);
        if (check(i, usd)) {
            usd.add(i);
            dfs(i + 1, usd, time + times[i]);
            usd.remove(i);
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        jobNum = sc.nextInt();
        for (int i = 0; i < jobNum; i++) {
            times[i] = sc.nextInt();
        }

        int mutexNum = sc.nextInt();
        for (int i =

 0; i < mutexNum; i++) {
            int a = sc.nextInt() - 1;
            int b = sc.nextInt() - 1;
            mutex.computeIfAbsent(a, k -> new HashSet<>()).add(b);
            mutex.computeIfAbsent(b, k -> new HashSet<>()).add(a);
        }

        Set<Integer> usd = new HashSet<>();
        dfs(0, usd, 0);

        System.out.println(cost);

        sc.close();
    }
}
