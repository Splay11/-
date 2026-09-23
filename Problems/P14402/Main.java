import java.util.Arrays;

public class Solution {
    private static int popcount32(int x) {
        return Integer.bitCount(x);
    }

    public int[] processDataArray(int[] data, int[][] operations) {
        int[] arr = Arrays.copyOf(data, data.length);
        sortArr(arr);
        for (int[] op : operations) {
            int i = op[0], j = op[1];
            int a = arr[i];
            int b = (i == j) ? a : arr[j];
            int merged = a | b;
            if (i == j) {
                arr = removeAt(arr, i);
            } else {
                int lo = Math.min(i, j), hi = Math.max(i, j);
                arr = removeAt(arr, hi);
                arr = removeAt(arr, lo);
            }
            arr = append(arr, merged);
            sortArr(arr);
        }
        return arr;
    }

    private static void sortArr(int[] arr) {
        Integer[] boxed = new Integer[arr.length];
        for (int k = 0; k < arr.length; k++) boxed[k] = arr[k];
        Arrays.sort(boxed, (u, v) -> {
            int cu = popcount32(u), cv = popcount32(v);
            if (cu != cv) return cu - cv;
            return Integer.compare(u, v);
        });
        for (int k = 0; k < arr.length; k++) arr[k] = boxed[k];
    }

    private static int[] removeAt(int[] arr, int idx) {
        int[] res = new int[arr.length - 1];
        for (int k = 0, p = 0; k < arr.length; k++) {
            if (k != idx) res[p++] = arr[k];
        }
        return res;
    }

    private static int[] append(int[] arr, int val) {
        int[] res = Arrays.copyOf(arr, arr.length + 1);
        res[arr.length] = val;
        return res;
    }
}
