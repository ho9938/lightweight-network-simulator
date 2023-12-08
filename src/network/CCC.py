from src.network.elem.Node import Node
from src.network.elem.Channel import PChannel, Policy

def out_flip(x):
    dim = int(x[0])
    pos = (len(x)-1) - dim
    flipped = '0' if x[pos] == '1' else '1'
    return x[:pos] + flipped + x[pos+1:]

def in_dec(x, n):
    deced = str((int(x[0])-1) % n)
    return deced + x[1:]

def dfs(i, n, x, arr:list):
    if i == 0:
        for j in range(n):
            arr.append(str(j)+x)
        return
    
    for j in range(2):
        dfs(i-1, n, x+str(j), arr)

class CCC:
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
        dfs(self.n, self.n, '', nodes)
        for index in nodes:
            name = 'n' + index
            self.nodes[name] = Node(name)

    def initchannels(self):
        for src in self.nodes.values():
            for i in range(2):
                srcidx = src.name[1:]
                dstidx = in_dec(srcidx, self.n) if i == 0 else out_flip(srcidx)

                name = 'c'+ srcidx[0] + str(i) + srcidx[1:]
                dst = self.nodes['n' + dstidx]
                lgth = self.chnlen
                cap = self.chncap * 3 if self.policy == Policy.DEFAULT or i == 1 else self.chncap
                dim = 1 if self.policy == Policy.DEFAULT or i == 1 else 3
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
        if srcidx[1:] == dstidx[1:]:
            pchannel = self.channels['c' + srcidx[0] + '0' + srcidx[1:]]
            line = 0 if self.policy == Policy.DEFAULT else 2
        elif flit.aux > 0:
            if int(srcidx[0]) == self.n-1:
                flit.aux = -aux
                if srcidx[-(int(srcidx[0])+1)] == dstidx[-(int(srcidx[0])+1)]:
                    pchannel = self.channels['c' + srcidx[0] + '0' + srcidx[1:]]
                    line = 0 if self.policy == Policy.DEFAULT else 1
                else:
                    pchannel = self.channels['c' + srcidx[0] + '1' + srcidx[1:]]
                    line = 0 if self.policy == Policy.DEFAULT else 0
            else:
                pchannel = self.channels['c' + srcidx[0] + '0' + srcidx[1:]]
                line = 0 if self.policy == Policy.DEFAULT else 0
        elif srcidx[-(int(srcidx[0])+1)] == dstidx[-(int(srcidx[0])+1)]:
            pchannel = self.channels['c' + srcidx[0] + '0' + srcidx[1:]]
            line = 0 if self.policy == Policy.DEFAULT else 1
        else:
            pchannel = self.channels['c' + srcidx[0] + '1' + srcidx[1:]]
            line = 0 if self.policy == Policy.DEFAULT else 0
        return pchannel.vchannels[line]