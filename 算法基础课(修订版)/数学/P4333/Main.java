import java.io.*;
import java.util.*;

public class Main {
	static long C2(long c) {
		return c >= 2 ? c * (c - 1) / 2 : 0L;
	}
	static long C3(long c) {
		return c >= 3 ? c * (c - 1) * (c - 2) / 6 : 0L;
	}
	public static void main(String[] args) throws Exception {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		StringTokenizer st;
		String s = br.readLine();
		if (s == null || s.isEmpty()) return;
		int n = Integer.parseInt(s.trim());
		List<Integer> vals = new ArrayList<>(n);
		while (vals.size() < n) {
			String line = br.readLine();
			if (line == null) break;
			st = new StringTokenizer(line);
			while (st.hasMoreTokens() && vals.size() < n) {
				vals.add(Integer.parseInt(st.nextToken()));
			}
		}

		HashMap<Integer, Integer> freq = new HashMap<>(n * 2);
		for (int x : vals) freq.put(x, freq.getOrDefault(x, 0) + 1);

		long S2 = 0, S3 = 0, selfSum = 0;
		for (int cInt : freq.values()) {
			long c = cInt;
			long c2 = C2(c);
			long c3 = C3(c);
			S2 += c2;
			S3 += c3;
			selfSum += c2 * c3;
		}

		long ans = S3 * S2 - selfSum;
		System.out.println(ans);
	}
}
