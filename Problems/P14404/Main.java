public class Solution {
    public int[] predictGeneration(int[][] sub_arrays, int station_capacity) {
        int n = sub_arrays.length;
        if (n == 0) return new int[0];

        int[] base = new int[n];
        int[] mins = new int[n];
        int[] maxs = new int[n];
        for (int i = 0; i < n; i++) {
            maxs[i] = sub_arrays[i][0];
            mins[i] = sub_arrays[i][1];
            base[i] = sub_arrays[i][2];
        }

        long total = 0, minTotal = 0;
        for (int i = 0; i < n; i++) {
            total += base[i];
            minTotal += mins[i];
        }

        double[] values = new double[n];
        for (int i = 0; i < n; i++) values[i] = base[i];

        if (total > station_capacity) {
            long need = total - station_capacity;
            long spaceSum = 0;
            for (int i = 0; i < n; i++) spaceSum += base[i] - mins[i];
            if (spaceSum == 0) return new int[n];
            for (int i = 0; i < n; i++) {
                double space = base[i] - mins[i];
                values[i] = base[i] - need * space / (double) spaceSum;
            }
        } else if (total < minTotal) {
            long need = minTotal - total;
            long spaceSum = 0;
            for (int i = 0; i < n; i++) spaceSum += maxs[i] - base[i];
            if (spaceSum == 0) return new int[n];
            for (int i = 0; i < n; i++) {
                double space = maxs[i] - base[i];
                values[i] = base[i] + need * space / (double) spaceSum;
            }
        }

        int[] ans = new int[n];
        for (int i = 0; i < n; i++) {
            ans[i] = (int) Math.ceil(values[i] - 1e-12);
        }
        return ans;
    }
}
