import java.util.*;

class Solution {
    public int solve(int n, int k, ArrayList<int[]> intervals) {
        intervals.sort(Comparator.comparingInt(a -> a[0]));
        int start = 0;
        PriorityQueue<Integer> heap = new PriorityQueue<>();
        int idx = 0;
        int ans = 0;

        while (idx < n || !heap.isEmpty()) {
            while (!heap.isEmpty() && heap.peek() < start) {
                heap.poll();
            }

            while (idx < n && intervals.get(idx)[0] <= start) {
                heap.add(intervals.get(idx)[1]);
                idx++;
            }

            if (heap.isEmpty()) {
                if (idx == n) {
                    break;
                }
                start = Math.max(start, intervals.get(idx)[0]);
            }

            while (idx < n && intervals.get(idx)[0] <= start) {
                heap.add(intervals.get(idx)[1]);
                idx++;
            }

            for (int i = 0; i < k; i++) {
                if (!heap.isEmpty()) {
                    ans++;
                    heap.poll();
                }
            }

            start++;
        }

        return ans;
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int k = sc.nextInt();
        ArrayList<int[]> intervals = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            intervals.add(new int[] {sc.nextInt(), sc.nextInt()});
        }

        Solution solution = new Solution();
        System.out.println(solution.solve(n, k, intervals));
        sc.close();
    }
}
