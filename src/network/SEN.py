from src.network.elem.Node import Node
from src.network.elem.Channel import PChannel, Policy

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
    def __init__(self, n, policy):
        self.n = n
        self.nodes = {}
        self.channels = {}
        self.policy = policy
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
            name = 'n' + index
            self.nodes[name] = Node(name)

    def initchannels(self):
        for src in self.nodes.values():
            for i in range(2):
                srcidx = src.name[1:]
                dstidx = rol(srcidx) if i == 0 else flip(srcidx)

                name = 'c' + str(i) + srcidx
                dst = self.nodes['n' + dstidx]
                lgth = self.chnlen
                cap = self.chncap * self.n if self.policy == Policy.DEFAULT else self.chncap
                dim = 1 if self.policy == Policy.DEFAULT else self.n
                pol = self.policy
                self.channels[name] = PChannel(name, src, dst, lgth, cap, dim, pol)

    def route(self, flit):
        src, dst, aux = flit.pos, flit.dst, abs(flit.aux)
        if isinstance(src, Node):
            srcidx = src.name[1:]
        else: # channel
            srcidx = src.parent.dst.name[1:]
        dstidx = dst.name[1:]
        
        if srcidx == dstidx:
            return None
        
        # else
        if aux <= self.n and srcidx[-1] == dstidx[aux-1]:
            flit.aux = aux # rol
            pchannel = self.channels['c0' + srcidx]
            line = 0 if self.policy == Policy.DEFAULT else self.n - aux
        else:
            flit.aux = -aux # flip
            pchannel = self.channels['c1' + srcidx]
            line = 0 if self.policy == Policy.DEFAULT else self.n - aux
        return pchannel.vchannels[line]