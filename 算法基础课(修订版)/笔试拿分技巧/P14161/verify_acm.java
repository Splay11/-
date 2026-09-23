import java.util.*;

class Solution {
    int jobNum;
    int[] times = new int[30];
    Map<Integer, Set<Integer>> mutex = new HashMap<>();
    int ans = 1;
    int cost = Integer.MAX_VALUE;

    boolean check(int i, Set<Integer> usd) {
        for (int u : usd) {
            if (mutex.getOrDefault(u, Collections.emptySet()).contains(i)
                    || mutex.getOrDefault(i, Collections.emptySet()).contains(u)) {
                return false;
            }
        }
        return true;
    }

    void dfs(int i, Set<Integer> usd, int time) {
        if (i >= jobNum) {
            if (ans <= usd.size()) {
                if (ans < usd.size()) {
                    ans = usd.size();
                    cost = time;
                } else if (time < cost) {
                    cost = time;
                }
            }
            return;
        }
        if (usd.size() + jobNum - i + 1 < ans) {
            return;
        }
        dfs(i + 1, usd, time);
        if (check(i, usd)) {
            usd.add(i);
            dfs(i + 1, usd, time + times[i]);
            usd.remove(i);
        }
    }

    public int solve(ArrayList<Integer> inputTimes, ArrayList<int[]> mutexPairs) {
        jobNum = inputTimes.size();
        for (int i = 0; i < jobNum; i++) {
            times[i] = inputTimes.get(i);
        }
        mutex.clear();
        for (int[] pair : mutexPairs) {
            int a = pair[0] - 1;
            int b = pair[1] - 1;
            mutex.computeIfAbsent(a, k -> new HashSet<>()).add(b);
            mutex.computeIfAbsent(b, k -> new HashSet<>()).add(a);
        }
        ans = 1;
        cost = Integer.MAX_VALUE;
        dfs(0, new HashSet<>(), 0);
        return cost;
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int jobNum = sc.nextInt();
        ArrayList<Integer> times = new ArrayList<>();
        for (int i = 0; i < jobNum; i++) {
            times.add(sc.nextInt());
        }

        int mutexNum = sc.nextInt();
        ArrayList<int[]> mutexPairs = new ArrayList<>();
        for (int i = 0; i < mutexNum; i++) {
            mutexPairs.add(new int[] {sc.nextInt(), sc.nextInt()});
        }

        Solution solution = new Solution();
        System.out.println(solution.solve(times, mutexPairs));
        sc.close();
    }
}
