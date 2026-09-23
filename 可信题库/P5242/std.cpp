#include <cstddef>
#include <tuple>
#include <unordered_map>
#include <utility>
#include <vector>

using namespace std;

class ParkingLot {
  int n;
  vector<vector<pair<int, int>>> spots;
  unordered_map<int, tuple<int, int, int>> car;

  bool conflict(const vector<pair<int, int> >& intervals, int start, int end) {
    for (size_t i = 0; i < intervals.size(); i++) {
      int s = intervals[i].first, e = intervals[i].second;
      if (start < e && s < end) return true;
    }
    return false;
  }

 public:
  ParkingLot(int n_) : n(n_), spots(n_) {}

  int reserve(int carId, int start, int end) {
    if (car.count(carId) || start >= end) return -1;
    for (int spot = 0; spot < n; spot++) {
      if (!conflict(spots[spot], start, end)) {
        spots[spot].push_back(make_pair(start, end));
        car[carId] = make_tuple(spot, start, end);
        return spot;
      }
    }
    return -1;
  }

  bool cancel(int carId) {
    unordered_map<int, tuple<int, int, int> >::iterator it = car.find(carId);
    if (it == car.end()) return false;
    int spot = get<0>(it->second);
    int start = get<1>(it->second);
    int end = get<2>(it->second);
    car.erase(it);
    vector<pair<int, int> >& vec = spots[spot];
    for (size_t i = 0; i < vec.size(); i++) {
      if (vec[i].first == start && vec[i].second == end) {
        vec.erase(vec.begin() + (ptrdiff_t)i);
        break;
      }
    }
    return true;
  }

  int spotOf(int carId) {
    unordered_map<int, tuple<int, int, int> >::iterator it = car.find(carId);
    if (it == car.end()) return -1;
    return get<0>(it->second);
  }

  int busyCount(int time) {
    int cnt = 0;
    for (unordered_map<int, tuple<int, int, int> >::iterator it = car.begin();
         it != car.end(); ++it) {
      int start = get<1>(it->second), end = get<2>(it->second);
      if (start <= time && time < end) cnt++;
    }
    return cnt;
  }
};
