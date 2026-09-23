public class ParkingLane {
    public ParkingLane(int capacity) {}
    public boolean arrive(int carId) { return false; }
    public boolean admit() { return false; }
    public int depart(int carId) { return -1; }
    public boolean undo() { return false; }
    public int front() { return -1; }
    public int waiting() { return 0; }
    public int size() { return 0; }
}
