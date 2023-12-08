from src.network.elem.Node import Node
from src.network.elem.Channel import PChannel, Policy

def dec(x, i, k, n):
    pos = (n-1) - i
    deced = (int(x[pos])-1) % k
    return x[:pos] + str(deced) + x[pos+1:]

def dfs(k, n, x, arr:list):
    if n == 0:
        arr.append(x)
        return
    
    for i in range(k):
        dfs(k, n-1, x+str(i), arr)

class KNC:
    def __init__(self, k, n, policy):
        self.k = k
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
        dfs(self.k, self.n, '', nodes)
        for index in nodes:
            name = 'n' + index
            self.nodes[name] = Node(name)

    def initchannels(self):
        for src in self.nodes.values():
            for i in range(self.n):
                srcidx = src.name[1:]
                dstidx = dec(srcidx, i, self.k, self.n)

                name = 'c' + str(i) + srcidx
                dst = self.nodes['n' + dstidx]
                lgth = self.chnlen
                cap = self.chncap*2 if self.policy == Policy.DEFAULT else self.chncap
                dim = 1 if self.policy == Policy.DEFAULT else 2
                pol = self.policy
                self.channels[name] = PChannel(name, src, dst, lgth, cap, dim, pol)

    def route(self, flit):
        src, dst = flit.pos, flit.dst
        if isinstance(src, Node):
            srcidx = src.name[1:]
        else: # channel
            srcidx = src.parent.dst.name[1:]
        dstidx = dst.name[1:]
        
        if srcidx == dstidx:
            return None
        
        # else
        pos = 0
        while srcidx[pos] == dstidx[pos]:
            pos += 1
        if srcidx[pos] < dstidx[pos] and srcidx[pos] != 0:
            pchannel = self.channels['c' + str(self.n-1-pos) + srcidx]
            line = 0 if self.policy == Policy.DEFAULT else 1
        else:
            pchannel = self.channels['c' + str(self.n-1-pos) + srcidx]
            line = 0 if self.policy == Policy.DEFAULT else 0
        return pchannel.vchannels[line]