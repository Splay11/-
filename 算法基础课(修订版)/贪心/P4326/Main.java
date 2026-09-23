import java.io.*;
import java.util.*;

public class Main {
	static class FS {
		private final InputStream in = System.in;
		private final byte[] buf = new byte[1 << 16];
		private int p = 0, l = 0;
		private int read() throws IOException {
			if (p >= l) { l = in.read(buf); p = 0; if (l <= 0) return -1; }
			return buf[p++];
		}
		long nextLong() throws IOException {
			int c; do { c = read(); } while (c <= 32);
			long s = 1;
			if (c == '-') { s = -1; c = read(); }
			long x = 0;
			while (c > 32) { x = x * 10 + (c - '0'); c = read(); }
			return x * s;
		}
		int nextInt() throws IOException { return (int) nextLong(); }
	}

	public static void main(String[] args) throws Exception {
		FS fs = new FS();
		int T = fs.nextInt();
		StringBuilder sb = new StringBuilder();
		while (T-- > 0) {
			int n = fs.nextInt();
			long[] a = new long[n];
			for (int i = 0; i < n; i++) a[i] = fs.nextLong();
			Arrays.sort(a); // 升序，倒序遍历
			boolean[] used = new boolean[n + 1];
			boolean ok = true;
			for (int i = n - 1; i >= 0; i--) {
				long x = a[i];
				while (x > n || (x > 0 && used[(int) x])) x >>= 1; // x//=2
				if (x == 0) { ok = false; break; }
				used[(int) x] = true;
			}
			sb.append(ok ? "YES" : "NO").append('\n');
		}
		System.out.print(sb.toString());
	}
}
