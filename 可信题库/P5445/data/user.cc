class PickupDesk {
public:
    PickupDesk() {}
    bool order(int ticketId) {
        (void)ticketId;
        return false;
    }
    int serve() { return -1; }
    int waiting() { return 0; }
};
