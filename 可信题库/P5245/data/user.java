class TTLCache {
    public TTLCache(int capacity) {}
    public void put(int key, int value, int expireAt) {}
    public int get(int key, int now) { return -1; }
    public int purge(int now) { return 0; }
    public int size() { return 0; }
}
