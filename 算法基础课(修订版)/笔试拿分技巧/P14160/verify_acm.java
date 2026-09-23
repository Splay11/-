import java.util.*;

class Solution {
    static final long MOD = 1_000_000_007;

    static class BIT {
        int size;
        long[] tree;

        BIT(int n) {
            size = n;
            tree = new long[n + 1];
        }

        void add(int x, long value) {
            while (x <= size) {
                tree[x] = (tree[x] + value) % MOD;
                x += x & -x;
            }
        }

        long query(int x) {
            long result = 0;
            while (x > 0) {
                result = (result + tree[x]) % MOD;
                x -= x & -x;
            }
            return result;
        }
    }

    public long solve(ArrayList<Long> a) {
        ArrayList<Long> alls = new ArrayList<>(new HashSet<>(a));
        Collections.sort(alls, Collections.reverseOrder());

        BIT bit = new BIT(alls.size());
        long result = 0;
        for (long value : a) {
            int id = Collections.binarySearch(alls, value, Collections.reverseOrder());
            if (id < 0) {
                continue;
            }
            id++;
            long sum = bit.query(id - 1);
            long res = (sum + 1) % MOD;
            result = (result + res) % MOD;
            bit.add(id, res);
        }
        return result;
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        ArrayList<Long> a = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            a.add(sc.nextLong());
        }

        Solution solution = new Solution();
        System.out.println(solution.solve(a));
        sc.close();
    }
}
