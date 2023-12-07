from src.network.elem.Node import Node
from src.network.elem.Channel import Channel

def rol(x:str):
    return x[1:]+x[0]

def flip(x:str):
    return x[:-1]+'0' if x[-1]=='1' else x[:-1]+'1'
    
def dfs(i, x, arr:list):
    if i == 0:
        arr.append(x)
        return
    
    for j in range(2):
        dfs(i-1, x+str(j), arr)

class SEN:
    def __init__(self, n):
        self.n = n
        self.nodes = {}
        self.channels = {}
        self.chnlen = 5
        self.chncap = 5
        self.init()

    def init(self):
        self.initnodes()
        self.initchannels()
    
    def initnodes(self):
        nodes = []
        dfs(self.n, '', nodes)
        for index in nodes:
            name = 'n'+index
            self.nodes[name] = Node(name)

    def initchannels(self):
        channels = []
        for node in self.nodes.values():
            index = node.name[1:]
            for i in range(2):
                channels.append(str(i)+index)
        for index in channels:
            name = 'c'+index
            self.channels[name] = Channel(name, self.chnlen, self.chncap)

    def route(self, flit):
        src, dst, aux = flit.pos, flit.dst, abs(flit.aux)
        if isinstance(src, Node):
            srcidx = src.name[1:]
        else: # channel
            _srcidx = src.name[2:]
            srcidx = rol(_srcidx) if src.name[1] == '0' else flip(_srcidx)
        dstidx = dst.name[1:]
        
        if srcidx == dstidx or aux > self.n:
            return None
        elif srcidx[-1] == dstidx[aux-1]:
            if isinstance(src, Channel):
                flit.aux = aux # rol
            return self.channels['c0' + srcidx]
        else:
            flit.aux = -aux # flip
            return self.channels['c1' + srcidx]