class ParkingLane {
    constructor(capacity) {}
    arrive(carId) { return false; }
    admit() { return false; }
    depart(carId) { return -1; }
    undo() { return false; }
    front() { return -1; }
    waiting() { return 0; }
    size() { return 0; }
}
