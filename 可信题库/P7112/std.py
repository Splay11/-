# -*- coding: utf-8 -*-
"""P7112 分片租约管理器标程。"""
from __future__ import annotations

from typing import Dict, Optional, Tuple


class ShardLeaseManager:
    def __init__(self, shardCount: int, maxHold: int) -> None:
        self.shard_count = shardCount
        self.max_hold = maxHold
        # shardId -> (clientId, expireAt)
        self.lease: Dict[int, Tuple[int, int]] = {}
        # clientId -> {shardId: expireAt}
        self.by_client: Dict[int, Dict[int, int]] = {}

    def _valid_shard(self, shard_id: int) -> bool:
        return 0 <= shard_id < self.shard_count

    def _expire_shard(self, shard_id: int, now: int) -> None:
        if shard_id not in self.lease:
            return
        cid, exp = self.lease[shard_id]
        if now >= exp:
            del self.lease[shard_id]
            mp = self.by_client.get(cid)
            if mp is not None and shard_id in mp:
                del mp[shard_id]
                if not mp:
                    del self.by_client[cid]

    def _expire_client(self, client_id: int, now: int) -> None:
        mp = self.by_client.get(client_id)
        if not mp:
            return
        dead = [sid for sid, exp in mp.items() if now >= exp]
        for sid in dead:
            self._expire_shard(sid, now)

    def _active_count(self, client_id: int, now: int) -> int:
        self._expire_client(client_id, now)
        mp = self.by_client.get(client_id)
        return 0 if not mp else len(mp)

    def acquire(self, clientId: int, shardId: int, now: int, ttl: int) -> bool:
        if clientId <= 0 or ttl <= 0 or not self._valid_shard(shardId):
            return False
        self._expire_shard(shardId, now)
        self._expire_client(clientId, now)
        if shardId in self.lease:
            return False
        if self._active_count(clientId, now) >= self.max_hold:
            return False
        exp = now + ttl
        self.lease[shardId] = (clientId, exp)
        self.by_client.setdefault(clientId, {})[shardId] = exp
        return True

    def renew(self, clientId: int, shardId: int, now: int, ttl: int) -> bool:
        if clientId <= 0 or ttl <= 0 or not self._valid_shard(shardId):
            return False
        self._expire_shard(shardId, now)
        if shardId not in self.lease:
            return False
        cid, _ = self.lease[shardId]
        if cid != clientId:
            return False
        exp = now + ttl
        self.lease[shardId] = (clientId, exp)
        self.by_client.setdefault(clientId, {})[shardId] = exp
        return True

    def release(self, clientId: int, shardId: int, now: int) -> bool:
        if clientId <= 0 or not self._valid_shard(shardId):
            return False
        self._expire_shard(shardId, now)
        if shardId not in self.lease:
            return False
        cid, _ = self.lease[shardId]
        if cid != clientId:
            return False
        del self.lease[shardId]
        mp = self.by_client.get(clientId)
        if mp is not None and shardId in mp:
            del mp[shardId]
            if not mp:
                del self.by_client[clientId]
        return True

    def owner(self, shardId: int, now: int) -> int:
        if not self._valid_shard(shardId):
            return -1
        self._expire_shard(shardId, now)
        if shardId not in self.lease:
            return -1
        return self.lease[shardId][0]

    def heldCount(self, clientId: int, now: int) -> int:
        if clientId <= 0:
            return -1
        return self._active_count(clientId, now)
