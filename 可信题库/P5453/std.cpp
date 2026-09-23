#include <vector>
#include <deque>
#include <unordered_set>
#include <string>
using namespace std;

class ParkingLane {
    int cap;
    vector<int> lane;
    deque<int> wait;
    unordered_set<int> inLane, inWait;
    vector<string> histKind;
    vector<int> histCar;
    vector<int> histWhere; // 0 lane 1 wait for arrive
public:
    ParkingLane(int capacity) : cap(capacity) {}

    bool arrive(int carId) {
        if (inLane.count(carId) || inWait.count(carId)) return false;
        if ((int)lane.size() < cap) {
            lane.push_back(carId);
            inLane.insert(carId);
            histKind.push_back("arrive");
            histCar.push_back(carId);
            histWhere.push_back(0);
        } else {
            wait.push_back(carId);
            inWait.insert(carId);
            histKind.push_back("arrive");
            histCar.push_back(carId);
            histWhere.push_back(1);
        }
        return true;
    }

    bool admit() {
        if (wait.empty() || (int)lane.size() >= cap) return false;
        int carId = wait.front();
        wait.pop_front();
        inWait.erase(carId);
        lane.push_back(carId);
        inLane.insert(carId);
        histKind.push_back("admit");
        histCar.push_back(carId);
        histWhere.push_back(-1);
        return true;
    }

    int depart(int carId) {
        if (!inLane.count(carId)) return -1;
        vector<int> temp;
        int moved = 0;
        while (!lane.empty() && lane.back() != carId) {
            temp.push_back(lane.back());
            lane.pop_back();
            moved++;
        }
        lane.pop_back();
        inLane.erase(carId);
        while (!temp.empty()) {
            lane.push_back(temp.back());
            temp.pop_back();
        }
        histKind.push_back("depart");
        histCar.push_back(carId);
        histWhere.push_back(-1);
        return moved;
    }

    bool undo() {
        if (histKind.empty()) return false;
        string kind = histKind.back();
        int carId = histCar.back();
        int where = histWhere.back();
        histKind.pop_back();
        histCar.pop_back();
        histWhere.pop_back();
        if (kind == "arrive") {
            if (where == 0) {
                if (lane.empty() || lane.back() != carId) {
                    histKind.push_back(kind); histCar.push_back(carId); histWhere.push_back(where);
                    return false;
                }
                lane.pop_back();
                inLane.erase(carId);
            } else {
                if (!inWait.count(carId)) {
                    histKind.push_back(kind); histCar.push_back(carId); histWhere.push_back(where);
                    return false;
                }
                for (deque<int>::iterator it = wait.begin(); it != wait.end(); ++it) {
                    if (*it == carId) { wait.erase(it); break; }
                }
                inWait.erase(carId);
            }
            return true;
        }
        if (kind == "admit") {
            if (lane.empty() || lane.back() != carId) {
                histKind.push_back(kind); histCar.push_back(carId); histWhere.push_back(where);
                return false;
            }
            lane.pop_back();
            inLane.erase(carId);
            wait.push_front(carId);
            inWait.insert(carId);
            return true;
        }
        if (kind == "depart") {
            if (inLane.count(carId) || inWait.count(carId) || (int)lane.size() >= cap) {
                histKind.push_back(kind); histCar.push_back(carId); histWhere.push_back(where);
                return false;
            }
            lane.push_back(carId);
            inLane.insert(carId);
            return true;
        }
        return false;
    }

    int front() { return lane.empty() ? -1 : lane.back(); }
    int waiting() { return (int)wait.size(); }
    int size() { return (int)lane.size(); }
};
