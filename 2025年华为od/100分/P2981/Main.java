public class Solution {
    public long maxSolarPanelArea(int[] heights) {
        int left = 0, right = heights.length - 1;
        long best = 0;
        while (left < right) {
            long h = Math.min(heights[left], heights[right]);
            long area = h * (right - left);
            if (area > best) best = area;
            if (heights[left] <= heights[right]) {
                left++;
            } else {
                right--;
            }
        }
        return best;
    }
}
