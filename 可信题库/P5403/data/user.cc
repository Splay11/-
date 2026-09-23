class MicQueue {
public:
    MicQueue() {}
    bool enroll(int songId, int heat) {
        (void)songId;
        (void)heat;
        return false;
    }
    int nextPlay() { return -1; }
    bool boost(int songId, int addHeat) {
        (void)songId;
        (void)addHeat;
        return false;
    }
    bool cancel(int songId) {
        (void)songId;
        return false;
    }
    int waiting() { return 0; }
};
