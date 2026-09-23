import java.util.*;

public class Main {
    static final long MOD = 1000000007;
    
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

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        long[] a = new long[n];
        ArrayList<Long> alls = new ArrayList<>();

        for (int i = 0; i < n; i++) {
            a[i] = scanner.nextLong();
            alls.add(a[i]);
        }

        // 离散化：排序并去重
        alls = new ArrayList<>(new HashSet<>(alls));
        Collections.sort(alls, Collections.reverseOrder());

        // 树状数组的大小为离散化后的唯一元素个数
        int size = alls.size();
        BIT bit = new BIT(size);

        long result = 0;
        for (int i = 0; i < n; i++) {
            // 查找a[i]在离散化数组中的排名
            // 如果 binarySearch 没找到元素，返回的是 -(插入点 + 1)，所以我们需要 + 1 来获取排名
            int id = Collections.binarySearch(alls, a[i], Collections.reverseOrder());
            
            if (id < 0) {
                continue; // 若没有找到，id 会变成 -(插入点 + 1)，我们需要调整它
            }
            id++; // 将索引调整为从 1 开始

            long sum = bit.query(id - 1);
            long res = (sum + 1) % MOD;

            result = (result + res) % MOD;

            bit.add(id, res);
        }

        System.out.println(result);
    }
}
