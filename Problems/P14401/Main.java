public class Solution {
    public int[] findMaintenanceWindow(int n, int w, int[] scores) {
        if (n < w) return new int[] {-1, 0};

        long windowSum = 0;
        int zeroCount = 0;
        for (int i = 0; i < w; i++) {
            windowSum += scores[i];
            if (scores[i] == 0) zeroCount++;
        }

        int bestStart = -1;
        long minSum = Long.MAX_VALUE;
        if (zeroCount == 0) {
            minSum = windowSum;
            bestStart = 0;
        }

        for (int start = 1; start <= n - w; start++) {
            int outVal = scores[start - 1];
            int inVal = scores[start + w - 1];
            windowSum += inVal - outVal;
            if (outVal == 0) zeroCount--;
            if (inVal == 0) zeroCount++;
            if (zeroCount == 0 && windowSum < minSum) {
                minSum = windowSum;
                bestStart = start;
            }
        }

        if (bestStart == -1) return new int[] {-1, 0};
        return new int[] {bestStart, (int) minSum};
    }
}
