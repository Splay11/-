# -*- coding: utf-8 -*-
from collections import deque
from typing import List


class Solution:
    def processPacketCommands(self, commands: List[str]) -> List[int]:
        buffer = deque()  # 缓冲区：按接收顺序排队
        send_q = deque()  # 发送区：按进入发送区的顺序排队
        in_buffer = set()  # 当前缓冲区中的编号，用于 O(1) 判重
        ans = []

        def flush_buffer_to_send():
            # 发送区为空时，将缓冲区全部按 FIFO 移入发送区
            while buffer:
                x = buffer.popleft()
                in_buffer.discard(x)
                send_q.append(x)

        for cmd in commands:
            parts = cmd.split()
            op = parts[0]
            if op == "RECEIVE":
                x = int(parts[1])
                # 仅检查缓冲区是否已有同编号（不检查发送区）
                if x in in_buffer:
                    ans.append(-1)
                else:
                    buffer.append(x)
                    in_buffer.add(x)
                    ans.append(x)
            elif op == "SEND":
                if send_q:
                    # 发送区非空，直接弹出最早的数据包
                    ans.append(send_q.popleft())
                elif buffer:
                    flush_buffer_to_send()
                    ans.append(send_q.popleft())
                else:
                    # 两区皆空
                    ans.append(0)
            elif op == "QUERY":
                if send_q:
                    # 只查看队首，不弹出
                    ans.append(send_q[0])
                elif buffer:
                    flush_buffer_to_send()
                    ans.append(send_q[0])
                else:
                    ans.append(0)
        return ans
