class TTLCache {
public:
    TTLCache(int capacity) {}
    void put(int key, int value, int expireAt) {}
    int get(int key, int now) { return -1; }
    int purge(int now) { return 0; }
    int size() { return 0; }
};
