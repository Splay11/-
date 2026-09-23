import java.util.*;

class ParkingLane {
    private int cap;
    private ArrayList<Integer> lane = new ArrayList<>();
    private ArrayDeque<Integer> wait = new ArrayDeque<>();
    private HashSet<Integer> inLane = new HashSet<>();
    private HashSet<Integer> inWait = new HashSet<>();
    private ArrayList<String> histKind = new ArrayList<>();
    private ArrayList<Integer> histCar = new ArrayList<>();
    private ArrayList<Integer> histWhere = new ArrayList<>();

    public ParkingLane(int capacity) {
        this.cap = capacity;
    }

    public boolean arrive(int carId) {
        if (inLane.contains(carId) || inWait.contains(carId)) return false;
        if (lane.size() < cap) {
            lane.add(carId);
            inLane.add(carId);
            histKind.add("arrive");
            histCar.add(carId);
            histWhere.add(0);
        } else {
            wait.addLast(carId);
            inWait.add(carId);
            histKind.add("arrive");
            histCar.add(carId);
            histWhere.add(1);
        }
        return true;
    }

    public boolean admit() {
        if (wait.isEmpty() || lane.size() >= cap) return false;
        int carId = wait.pollFirst();
        inWait.remove(carId);
        lane.add(carId);
        inLane.add(carId);
        histKind.add("admit");
        histCar.add(carId);
        histWhere.add(-1);
        return true;
    }

    public int depart(int carId) {
        if (!inLane.contains(carId)) return -1;
        ArrayList<Integer> temp = new ArrayList<>();
        int moved = 0;
        while (!lane.isEmpty() && lane.get(lane.size() - 1) != carId) {
            temp.add(lane.remove(lane.size() - 1));
            moved++;
        }
        lane.remove(lane.size() - 1);
        inLane.remove(carId);
        for (int i = temp.size() - 1; i >= 0; i--) lane.add(temp.get(i));
        histKind.add("depart");
        histCar.add(carId);
        histWhere.add(-1);
        return moved;
    }

    public boolean undo() {
        if (histKind.isEmpty()) return false;
        String kind = histKind.remove(histKind.size() - 1);
        int carId = histCar.remove(histCar.size() - 1);
        int where = histWhere.remove(histWhere.size() - 1);
        if (kind.equals("arrive")) {
            if (where == 0) {
                if (lane.isEmpty() || lane.get(lane.size() - 1) != carId) {
                    histKind.add(kind); histCar.add(carId); histWhere.add(where);
                    return false;
                }
                lane.remove(lane.size() - 1);
                inLane.remove(carId);
            } else {
                if (!inWait.contains(carId)) {
                    histKind.add(kind); histCar.add(carId); histWhere.add(where);
                    return false;
                }
                wait.remove(carId);
                inWait.remove(carId);
            }
            return true;
        }
        if (kind.equals("admit")) {
            if (lane.isEmpty() || lane.get(lane.size() - 1) != carId) {
                histKind.add(kind); histCar.add(carId); histWhere.add(where);
                return false;
            }
            lane.remove(lane.size() - 1);
            inLane.remove(carId);
            wait.addFirst(carId);
            inWait.add(carId);
            return true;
        }
        if (kind.equals("depart")) {
            if (inLane.contains(carId) || inWait.contains(carId) || lane.size() >= cap) {
                histKind.add(kind); histCar.add(carId); histWhere.add(where);
                return false;
            }
            lane.add(carId);
            inLane.add(carId);
            return true;
        }
        return false;
    }

    public int front() {
        return lane.isEmpty() ? -1 : lane.get(lane.size() - 1);
    }

    public int waiting() {
        return wait.size();
    }

    public int size() {
        return lane.size();
    }
}
