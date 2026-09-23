#include <map>
#include <unordered_map>
#include <vector>
using namespace std;

class ShardLeaseManager {
    int shard_count;
    int max_hold;
    // shard -> (client, expire)
    unordered_map<int, pair<int, int>> lease;
    // client -> shard -> expire
    unordered_map<int, unordered_map<int, int>> by_client;

    bool valid_shard(int shard_id) const {
        return shard_id >= 0 && shard_id < shard_count;
    }

    void expire_shard(int shard_id, int now) {
        auto it = lease.find(shard_id);
        if (it == lease.end()) return;
        if (now >= it->second.second) {
            int cid = it->second.first;
            lease.erase(it);
            auto cit = by_client.find(cid);
            if (cit != by_client.end()) {
                cit->second.erase(shard_id);
                if (cit->second.empty()) by_client.erase(cit);
            }
        }
    }

    void expire_client(int client_id, int now) {
        auto cit = by_client.find(client_id);
        if (cit == by_client.end()) return;
        vector<int> dead;
        for (auto& kv : cit->second) {
            if (now >= kv.second) dead.push_back(kv.first);
        }
        for (int sid : dead) expire_shard(sid, now);
    }

    int active_count(int client_id, int now) {
        expire_client(client_id, now);
        auto cit = by_client.find(client_id);
        return cit == by_client.end() ? 0 : (int)cit->second.size();
    }

public:
    ShardLeaseManager(int shardCount, int maxHold) : shard_count(shardCount), max_hold(maxHold) {}

    bool acquire(int clientId, int shardId, int now, int ttl) {
        if (clientId <= 0 || ttl <= 0 || !valid_shard(shardId)) return false;
        expire_shard(shardId, now);
        expire_client(clientId, now);
        if (lease.count(shardId)) return false;
        if (active_count(clientId, now) >= max_hold) return false;
        int exp = now + ttl;
        lease[shardId] = {clientId, exp};
        by_client[clientId][shardId] = exp;
        return true;
    }

    bool renew(int clientId, int shardId, int now, int ttl) {
        if (clientId <= 0 || ttl <= 0 || !valid_shard(shardId)) return false;
        expire_shard(shardId, now);
        auto it = lease.find(shardId);
        if (it == lease.end() || it->second.first != clientId) return false;
        int exp = now + ttl;
        lease[shardId] = {clientId, exp};
        by_client[clientId][shardId] = exp;
        return true;
    }

    bool release(int clientId, int shardId, int now) {
        if (clientId <= 0 || !valid_shard(shardId)) return false;
        expire_shard(shardId, now);
        auto it = lease.find(shardId);
        if (it == lease.end() || it->second.first != clientId) return false;
        lease.erase(it);
        auto cit = by_client.find(clientId);
        if (cit != by_client.end()) {
            cit->second.erase(shardId);
            if (cit->second.empty()) by_client.erase(cit);
        }
        return true;
    }

    int owner(int shardId, int now) {
        if (!valid_shard(shardId)) return -1;
        expire_shard(shardId, now);
        auto it = lease.find(shardId);
        return it == lease.end() ? -1 : it->second.first;
    }

    int heldCount(int clientId, int now) {
        if (clientId <= 0) return -1;
        return active_count(clientId, now);
    }
};
