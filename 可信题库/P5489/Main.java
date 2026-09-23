class Solution {
    public int[] bestShotRecords(int[] scores) {
        int cnt = 1, last = 0, best = scores[0], gap = 0;
        for (int i = 1; i < scores.length; i++) {
            if (scores[i] > best) {
                if (i - last > gap) gap = i - last;
                last = i;
                best = scores[i];
                cnt++;
            }
        }
        return new int[] {cnt, gap};
    }
}
