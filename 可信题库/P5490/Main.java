class ParcelSlots {
    private int n;
    private int[] slot;
    private int cnt;

    public ParcelSlots(int n) {
        this.n = n;
        this.slot = new int[n];
        this.cnt = 0;
    }

    public boolean put(int i, int w) {
        if (i < 1 || i > n || w <= 0 || slot[i - 1] != 0) return false;
        slot[i - 1] = w;
        cnt++;
        return true;
    }

    public int take(int i) {
        if (i < 1 || i > n || slot[i - 1] == 0) return 0;
        int w = slot[i - 1];
        slot[i - 1] = 0;
        cnt--;
        return w;
    }

    public boolean moveRight(int i) {
        if (i < 1 || i >= n || slot[i - 1] == 0 || slot[i] != 0) return false;
        slot[i] = slot[i - 1];
        slot[i - 1] = 0;
        return true;
    }

    public int occupied() {
        return cnt;
    }
}
