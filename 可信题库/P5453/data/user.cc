class ParkingLane {
public:
    ParkingLane(int capacity) { (void)capacity; }
    bool arrive(int carId) { (void)carId; return false; }
    bool admit() { return false; }
    int depart(int carId) { (void)carId; return -1; }
    bool undo() { return false; }
    int front() { return -1; }
    int waiting() { return 0; }
    int size() { return 0; }
};
