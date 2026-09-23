public class Solution {
    public int[] analyzeTemperatureData(int[] temperatures, int k, int t) {
        int n = temperatures.length;
        int maxVal = temperatures[0];
        int maxIdx = 0;
        for (int i = 1; i < n; i++) {
            if (temperatures[i] > maxVal) {
                maxVal = temperatures[i];
                maxIdx = i;
            }
        }

        int count = 0;
        int bestStart = -1;
        int bestEnd = -1;
        int bestRise = -1;

        for (int i = 0; i <= n - k; i++) {
            boolean ok = true;
            for (int j = i; j < i + k - 1; j++) {
                if (temperatures[j] >= temperatures[j + 1]) {
                    ok = false;
                    break;
                }
            }
            if (!ok) continue;
            int rise = temperatures[i + k - 1] - temperatures[i];
            if (rise >= t) {
                count++;
                if (rise > bestRise
                        || (rise == bestRise && (bestStart == -1 || i < bestStart))) {
                    bestRise = rise;
                    bestStart = i;
                    bestEnd = i + k - 1;
                }
            }
        }

        return new int[] {maxVal, maxIdx, count, bestStart, bestEnd};
    }
}
