import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.Comparator;
import java.util.StringTokenizer;

public class Main {
    static class Fenwick {
        int n;
        int[] c;

        Fenwick(int n) {
            this.n = n;
            c = new int[n + 1];
        }

        void add(int i, int v) {
            // 在工位 i 上加上 v
            while (i <= n) {
                c[i] += v;
                i += i & -i;
            }
        }

        int pre(int i) {
            int s = 0;
            while (i > 0) {
                s += c[i];
                i -= i & -i;
            }
            return s;
        }

        int rng(int left, int right) {
            // 统计上游窗口 [left, right]
            if (left > right) {
                return 0;
            }
            return pre(right) - pre(left - 1);
        }
    }

    static class Station {
        long w;
        int pos;
    }

    static class Query {
        long thresh;
        int left;
        int right;
        int qid;
    }

    static int[] solve(int n, int d, long k, long[] w, int[] qs) {
        Station[] stations = new Station[n];
        for (int i = 1; i <= n; i++) {
            stations[i - 1] = new Station();
            stations[i - 1].w = w[i];
            stations[i - 1].pos = i;
        }
        Query[] queries = new Query[qs.length];
        for (int i = 0; i < qs.length; i++) {
            int x = qs[i];
            int left = x - d;
            if (left < 1) {
                left = 1;
            }
            queries[i] = new Query();
            queries[i].thresh = w[x] - k;
            queries[i].left = left;
            queries[i].right = x - 1;
            queries[i].qid = i;
        }
        // 工位、询问都按重量/阈值从小到大，才能用双指针离线插入
        Arrays.sort(stations, new Comparator<Station>() {
            public int compare(Station a, Station b) {
                if (a.w < b.w) {
                    return -1;
                }
                if (a.w > b.w) {
                    return 1;
                }
                return 0;
            }
        });
        Arrays.sort(queries, new Comparator<Query>() {
            public int compare(Query a, Query b) {
                if (a.thresh < b.thresh) {
                    return -1;
                }
                if (a.thresh > b.thresh) {
                    return 1;
                }
                return 0;
            }
        });
        Fenwick bit = new Fenwick(n);
        int[] ans = new int[qs.length];
        int p = 0;
        for (int i = 0; i < queries.length; i++) {
            while (p < n && stations[p].w <= queries[i].thresh) {
                bit.add(stations[p].pos, 1);
                p++;
            }
            ans[queries[i].qid] = bit.rng(queries[i].left, queries[i].right);
        }
        return ans;
    }

    public static void main(String[] args) throws IOException {
        // n、m 到 1e5，用 BufferedReader 读入
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int m = Integer.parseInt(st.nextToken());
        int d = Integer.parseInt(st.nextToken());
        long k = Long.parseLong(st.nextToken());
        st = new StringTokenizer(br.readLine());
        long[] w = new long[n + 1];
        for (int i = 1; i <= n; i++) {
            w[i] = Long.parseLong(st.nextToken());
        }
        int[] qs = new int[m];
        for (int i = 0; i < m; i++) {
            qs[i] = Integer.parseInt(br.readLine().trim());
        }
        int[] out = solve(n, d, k, w, qs);
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < out.length; i++) {
            sb.append(out[i]).append('\n');
        }
        System.out.print(sb.toString());
    }
}
