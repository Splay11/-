# -*- coding: utf-8 -*-
from typing import List, Optional, Tuple


class Solution:
    def filterValidAClassIPs(self, ips: List[str]) -> List[str]:
        valid = []
        # 逐个校验：合法 IP 连同排序键一起暂存
        for ip in ips:
            key = self._parse_valid(ip)
            if key is not None:
                valid.append((key, ip))
        # 按 (第二段, 第三段, 第四段) 数值三元组升序，不能用字符串排序
        valid.sort(key=lambda x: x[0])
        return [ip for _, ip in valid]

    def _parse_valid(self, ip: str) -> Optional[Tuple[int, int, int]]:
        """解析并校验单个 IP；合法则返回后三段数值，否则返回 None。"""
        parts = ip.split(".")
        # 必须是四段式 xxx.xxx.xxx.xxx
        if len(parts) != 4:
            return None
        nums = []
        for p in parts:
            # 空分段非法，如 "10..1.1"
            if not p:
                return None
            # 前导零规则：仅允许单独的 "0"，"01"、"00" 等均非法
            if len(p) > 1 and p[0] == "0":
                return None
            # 分段必须全为数字字符
            if not p.isdigit():
                return None
            v = int(p)
            # 每段取值范围 0~255
            if v < 0 or v > 255:
                return None
            nums.append(v)
        # A 类内网：第一段固定为 10
        if nums[0] != 10:
            return None
        # 返回后三段作为排序键
        return nums[1], nums[2], nums[3]
