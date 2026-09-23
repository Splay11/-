import java.io.*;
import java.util.*;

// 并查集
class DSU {
	int[] p, r;
	DSU(int n) {
		p = new int[n];
		r = new int[n];
		for (int i = 0; i < n; i++) p[i] = i;
	}
	int find(int x) {
		if (p[x] != x) p[x] = find(p[x]);
		return p[x];
	}
	boolean unite(int a, int b) {
		a = find(a); b = find(b);
		if (a == b) return false;
		if (r[a] < r[b]) { int t = a; a = b; b = t; }
		p[b] = a;
		if (r[a] == r[b]) r[a]++;
		return true;
	}
}

public class Main {
	static class FastScanner {
		BufferedInputStream in;
		byte[] buffer = new byte[1 << 16];
		int ptr = 0, len = 0;
		FastScanner(InputStream is) { in = new BufferedInputStream(is); }
		int read() throws IOException {
			if (ptr >= len) {
				len = in.read(buffer);
				ptr = 0;
				if (len <= 0) return -1;
			}
			return buffer[ptr++];
		}
		int nextInt() throws IOException {
			int c, s = 1, x = 0;
			do { c = read(); } while (c <= ' ' && c != -1);
			if (c == '-') { s = -1; c = read(); }
			for (; c > ' '; c = read()) x = x * 10 + (c - '0');
			return x * s;
		}
	}
	public static void main(String[] args) throws Exception {
		FastScanner fs = new FastScanner(System.in);
		StringBuilder sb = new StringBuilder();
		int T = fs.nextInt();
		while (T-- > 0) {
			int n = fs.nextInt();
			int m = fs.nextInt(); // m 不直接使用
			int[] a = new int[n], b = new int[n];
			for (int i = 0; i < n; i++) a[i] = fs.nextInt();
			for (int i = 0; i < n; i++) b[i] = fs.nextInt();

			// 坐标压缩：排序去重 + 二分
			int[] vals = new int[2 * n];
			for (int i = 0; i < n; i++) {
				vals[2*i] = a[i];
				vals[2*i + 1] = b[i];
			}
			Arrays.sort(vals);
			int k = 0;
			for (int i = 0; i < vals.length; i++) {
				if (i == 0 || vals[i] != vals[i - 1]) vals[k++] = vals[i];
			}
			int K = k;
			DSU dsu = new DSU(K);

			// 辅助函数：二分找到值的下标
			for (int i = 0; i < n; i++) {
				int u = Arrays.binarySearch(vals, 0, K, a[i]);
				int v = Arrays.binarySearch(vals, 0, K, b[i]);
				dsu.unite(u, v);
			}

			int C = 0;
			for (int i = 0; i < K; i++) if (dsu.find(i) == i) C++;
			sb.append(K - C).append('\n');
		}
		System.out.print(sb.toString());
	}
}
