class Node:
    def __init__(self, name:str):
        self.name = name
        self.senario = []
        self.queue = []
    
    def clear(self):
        self.senario.clear()
        self.queue.clear()

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
        print("senario remaining: ")
        for sen in self.senario:
            sen.printsummary()
