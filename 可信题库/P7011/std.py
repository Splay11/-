# -*- coding: utf-8 -*-
"""P7011 CertAuthority 标程：证书树 + 懒吊销。"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple


class CertAuthority:
    def __init__(self) -> None:
        self.parent: Dict[int, int] = {}
        self.expire: Dict[int, int] = {}
        self.revoked: Dict[int, bool] = {}

    def _exists(self, cert_id: int) -> bool:
        return cert_id in self.parent

    def _chain_clean(self, cert_id: int) -> bool:
        """路径上没有任何吊销标记。"""
        cur = cert_id
        seen = set()
        while cur != 0:
            if cur in seen or not self._exists(cur) or self.revoked[cur]:
                return False
            seen.add(cur)
            cur = self.parent[cur]
        return True

    def issue(self, certId: int, parentId: int, expireAt: int) -> bool:
        if certId <= 0 or expireAt <= 0 or certId in self.parent:
            return False
        if parentId == 0:
            self.parent[certId] = 0
            self.expire[certId] = expireAt
            self.revoked[certId] = False
            return True
        if parentId <= 0 or parentId not in self.parent:
            return False
        if not self._chain_clean(parentId):
            return False
        if expireAt > self.expire[parentId]:
            return False
        self.parent[certId] = parentId
        self.expire[certId] = expireAt
        self.revoked[certId] = False
        return True

    def revoke(self, certId: int) -> bool:
        if certId not in self.parent or self.revoked[certId]:
            return False
        self.revoked[certId] = True
        return True

    def isValid(self, certId: int, now: int) -> bool:
        cur = certId
        seen = set()
        while cur != 0:
            if cur in seen or cur not in self.parent:
                return False
            if self.revoked[cur] or now >= self.expire[cur]:
                return False
            seen.add(cur)
            cur = self.parent[cur]
        return certId in self.parent

    def ttl(self, certId: int, now: int) -> int:
        if not self.isValid(certId, now):
            return -1
        cur = certId
        mn = self.expire[cur]
        while cur != 0:
            mn = min(mn, self.expire[cur])
            cur = self.parent[cur]
        return mn - now

    def issuerOf(self, certId: int) -> int:
        if certId not in self.parent:
            return -1
        return self.parent[certId]

    def rootOf(self, certId: int) -> int:
        if certId not in self.parent:
            return -1
        cur = certId
        seen = set()
        while self.parent[cur] != 0:
            if cur in seen:
                return -1
            seen.add(cur)
            cur = self.parent[cur]
        return cur


def run_ops(ops: List[str]) -> List[str]:
    import re

    outs: List[str] = []
    obj: Optional[CertAuthority] = None
    for raw in ops:
        line = raw.strip()
        if not line:
            continue
        if line == "CertAuthority()":
            obj = CertAuthority()
            outs.append("null")
        elif line.startswith("issue("):
            m = re.fullmatch(r"issue\((-?\d+),\s*(-?\d+),\s*(-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            ok = obj.issue(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            outs.append("true" if ok else "false")
        elif line.startswith("revoke("):
            m = re.fullmatch(r"revoke\((-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append("true" if obj.revoke(int(m.group(1))) else "false")
        elif line.startswith("isValid("):
            m = re.fullmatch(r"isValid\((-?\d+),\s*(-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append("true" if obj.isValid(int(m.group(1)), int(m.group(2))) else "false")
        elif line.startswith("ttl("):
            m = re.fullmatch(r"ttl\((-?\d+),\s*(-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append(str(obj.ttl(int(m.group(1)), int(m.group(2)))))
        elif line.startswith("issuerOf("):
            m = re.fullmatch(r"issuerOf\((-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append(str(obj.issuerOf(int(m.group(1)))))
        elif line.startswith("rootOf("):
            m = re.fullmatch(r"rootOf\((-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append(str(obj.rootOf(int(m.group(1)))))
        else:
            raise SystemExit("bad op: " + line)
    return outs
