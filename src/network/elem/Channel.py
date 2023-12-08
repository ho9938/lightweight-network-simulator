from enum import Enum, auto

class Policy(Enum):
    DEFAULT = auto() # no virtual channel
    RR = auto() # round-robin
    FCFS = auto() # first come first served
    OF = auto() # oldest first

    def getpolicy(str):
        if str == 'RR':
            return Policy.RR
        elif str == 'FCFS':
            return Policy.FCFS
        elif str == 'OF':
            return Policy.OF
        else:
            return Policy.DEFAULT
    
class VChannel:
    def __init__(self, name, line, length, capacity, parent):
        self.name = name
        self.line = line
        self.queue = []
        self.next = -1
        self.length = length
        self.capacity = capacity
        self.parent = parent
    
    def clear(self):
        self.queue.clear()

    def is_empty(self):
        return len(self.queue) == 0
    
    def is_full(self):
        return len(self.queue) >= self.capacity
    
    def push(self, flit):
        self.queue.append(flit)
        flit.pos = self
        flit.tick = 0
        flit.aux = flit.aux+1 if flit.aux > 0 else flit.aux
        self.next = flit.next
        
    def pop(self):
        flit = self.queue.pop(0)
        flit.pos = None
        flit.tick = 0

    def refresh(self):
        for flit in self.queue:
            flit.tick += 1
            flit.tottick += 1
        while len(self.queue) > 0:
            flit = self.queue[0]
            if flit.tick >= self.length and flit.dst == self.parent.dst:
                self.queue.pop(0)
            else:
                return
                

    def is_available(self, index):
        if self.is_empty():
            return True
        if self.is_full():
            return False
        if len(self.queue) == 0:
            return False
        if self.next == -1:
            return True
        elif self.next == index:
            return True
        else:
            return False

class PChannel:
    def __init__(self, name, src, dst, lgth, cap, dim, pol):
        self.name = name
        self.src = src
        self.dst = dst
        self.vchannels = [VChannel(name, i, lgth, cap, self) for i in range(dim)]
        self.dimension = dim
        self.policy = pol
        self.latest = dim - 1
    
    def geturgent(self):
        index = 0
        if self.policy == Policy.RR:
            index = (self.latest+1) % self.dimension
        elif self.policy == Policy.FCFS:
            maxtick = -1
            for i in range(self.dimension):
                vchannel = self.vchannels[i]
                if len(vchannel.queue) == 0:
                    continue
                if maxtick < vchannel.queue[0].tick:
                    maxtick = vchannel.queue[0].tick
                    index = i
        elif self.policy == Policy.OF:
            maxttick = -1
            for i in range(self.dimension):
                vchannel = self.vchannels[i]
                if len(vchannel.queue) == 0:
                    continue
                if maxttick < vchannel.queue[0].tottick:
                    maxttick = vchannel.queue[0].tottick
                    index = i
        self.latest = index
        return self.vchannels[index]
    
    def clear(self):
        for vchannel in self.vchannels:
            vchannel.clear()

    def refresh(self):
        for vchannel in self.vchannels:
            vchannel.refresh()

    def printsummary(self):
        print(self.name + ':', end='\t')
        for i in range(self.dimension):
            vchannel = self.vchannels[i]
            print(str(i) + ' (' + str(len(vchannel.queue)) + '/' + str(vchannel.capacity) + ') [', end=' ')
            for flit in vchannel.queue:
                print('f' + str(flit.index), end=' ')
            print("]", end='\t')
        print()

    def printstat(self):
        print("source: " + self.src.name)
        print("destination: " + self.dst.name)
        for i in range(self.dimension):
            vchannel = self.vchannels[i]
            print("length: " + str(vchannel.length), end='\t')
            print("capacity: " + str(len(vchannel.queue)) + '/' + str(vchannel.capacity), end='\t')
            print("queue: [", end=' ')
            for flit in vchannel.queue:
                print('f' + str(flit.index), end=' ')
            print("]")