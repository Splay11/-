import java.util.*;

public class Main {
    static class UnionFind {
        int[] fa;

        public UnionFind(int n) {
            fa = new int[n + 1]; // 初始化父节点数组
            for (int i = 0; i <= n; i++) {
                fa[i] = i;
            }
        }

        public int find(int x) {
            if (fa[x] != x) {
                fa[x] = find(fa[x]); // 路径压缩
            }
            return fa[x];
        }

        public void union(int x, int y) {
            int fax = find(x);
            int fay = find(y);
            if (fax != fay) {
                fa[fax] = fay; // 合并集合
            }
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = Integer.parseInt(scanner.nextLine()); // 读取图片数量
        int[][] a = new int[n][n]; // 相似度矩阵
        for (int i = 0; i < n; i++) {
            String[] line = scanner.nextLine().split(" ");
            for (int j = 0; j < n; j++) {
                a[i][j] = Integer.parseInt(line[j]);
            }
        }
        
        UnionFind uf = new UnionFind(n);
        int[] ans = new int[n + 1]; // 每个相似类的相似度之和

        // 读取相似度矩阵并构建并查集
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= n; j++) {
                if (a[i - 1][j - 1] != 0) { // 注意索引从 0 开始
                    uf.union(i, j);
                }
            }
        }

        // 计算每个相似类的相似度之和
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= n; j++) {
                if (a[i - 1][j - 1] != 0 && uf.find(i) == uf.find(j)) {
                    ans[uf.find(i)] += a[i - 1][j - 1];
                    a[i - 1][j - 1] = 0; // 避免重复计算
                    a[j - 1][i - 1] = 0;
                }
            }
        }
        for(int i = 1; i <= n; i++){
            if(uf.find(i) != i)ans[i] = -1;
        }
        // 排序并输出
        List<Integer> sortedList = new ArrayList<>();
        for (int i = 1; i <= n; i++) {
            if(ans[i] == -1)continue;
            sortedList.add(ans[i]);
        }
        sortedList.sort(Collections.reverseOrder()); // 按降序排序

        for (int score : sortedList) {
            System.out.print(score + " ");
        }
        scanner.close();
    }
}
