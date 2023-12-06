class Channel:
    def __init__(self, name, length, capacity):
        self.name = name
        self.src = ''
        self.dst = ''
        self.length = length
        self.queue = []
        self.size = 0
        self.capacity = capacity
    
    def clear(self):
        self.queue.clear()
        self.size = 0

    def is_empty(self):
        return self.size == 0
    
    def is_full(self):
        return self.size >= self.capacity

    def refresh(self):
        self.size = len(self.queue)
        for flit in self.queue:
            flit.tick += 1
            flit.tottick += 1

    def is_available(self, index):
        if self.is_empty():
            return True
        if self.is_full():
            return False
        if len(self.queue) == 0:
            return False
        if self.queue[-1].next == -1:
            return True
        elif self.queue[-1].next == index:
            return True
        else:
            return False

    def printsummary(self):
        print(self.name + ':', end='\t')
        print(str(self.size) + '/' + str(self.capacity), end='\t')
        print("queue: [", end=' ')
        for flit in self.queue:
            print('f' + str(flit.index), end=' ')
        print("]")

    def printstat(self):
        print("source: " + self.src)
        print("destination: " + self.dst)
        print("length: " + str(self.length))
        print("capacity: " + str(self.size) + '/' + str(self.capacity))
        print("queue: [", end=' ')
        for flit in self.queue:
            print('f' + str(flit.index), end=' ')
        print("]")