class Solution {
    public int maxSplitProduct(String seq) {
        int n = seq.length();
        int ans = 0;
        for (int k = 1; k < n; k++) {
            int prod = Integer.parseInt(seq.substring(0, k)) * Integer.parseInt(seq.substring(k));
            if (prod > ans) ans = prod;
        }
        return ans;
    }
}
