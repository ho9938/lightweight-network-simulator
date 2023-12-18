class Node:
    def __init__(self, name:str):
        self.name = name
        self.scenario = []
        self.queue = []
    
    def clear(self):
        self.scenario.clear()
        self.queue.clear()

    def push(self, flit):
        self.queue.append(flit)
        flit.pos = self
        flit.tick = 0
        
    def pop(self):
        flit = self.queue.pop(0)
        flit.pos = None
        flit.tick = 0

    def refresh(self):
        for flit in self.queue:
            flit.tick += 1
            flit.tottick += 1
    
    def printsummary(self):
        print(self.name + ':', end='\t')
        print("queue: [", end=' ')
        for flit in self.queue:
            print('f' + str(flit.index), end=' ')
        print("]")
    
    def printstat(self):
        print("queue: [", end=' ')
        for flit in self.queue:
            print('f' + str(flit.index), end=' ')
        print("]")
        print("scenario remaining: ")
        for sen in self.scenario:
            sen.printsummary()
