class PickupDesk:
    def __init__(self):
        self.queue = []
        self.head = 0
        self.waitingIds = set()

    def order(self, ticketId: int) -> bool:
        # 号已经在等待队列里，重复取号不改变任何状态
        if ticketId in self.waitingIds:
            return False
        self.queue.append(ticketId)
        self.waitingIds.add(ticketId)
        return True

    def serve(self) -> int:
        # 队列为空时叫号失败，返回 -1
        if self.head == len(self.queue):
            return -1
        ticketId = self.queue[self.head]
        self.head += 1
        # 叫走之后这个号不再等待，才能被重新取
        self.waitingIds.remove(ticketId)
        return ticketId

    def waiting(self) -> int:
        return len(self.waitingIds)
