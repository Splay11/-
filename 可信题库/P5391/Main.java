class Solution {
    public boolean canPassBooks(int[] desks) {
        long s = 0;
        for (int i = 0; i < desks.length; i++) {
            s += desks[i];
            long k = i + 1L;
            if (s < k * (k + 1) / 2) return false;
        }
        return true;
    }
}
