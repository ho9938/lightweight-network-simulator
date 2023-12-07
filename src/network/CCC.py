from src.network.elem.Node import Node
from src.network.elem.Channel import Channel

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
        dfs(self.n, self.n, '', nodes)
        for index in nodes:
            name = 'n'+index
            self.nodes[name] = Node(name)

    def initchannels(self):
        channels = []
        for node in self.nodes.values():
            index = node.name[1:]
            for i in range(2):
                channels.append(index[0]+str(i)+index[1:])
        for index in channels:
            name = 'c'+index
            self.channels[name] = Channel(name, self.chnlen, self.chncap)

    def route(self, flit):
        src, dst, aux = flit.pos, flit.dst, abs(flit.aux)
        if isinstance(src, Node):
            srcidx = src.name[1:]
        else: # channel
            _srcidx = src.name[1] + src.name[3:]
            srcidx = in_dec(_srcidx, self.n) if src.name[2] == '0' else out_flip(_srcidx)
        dstidx = dst.name[1:]
        
        if srcidx == dstidx:
            return None
        elif srcidx[1:] == dstidx[1:]:
            return self.channels['c' + srcidx[0] + '0' + srcidx[1:]]
        elif flit.aux > 0:
            if int(srcidx[0]) == self.n-1:
                flit.aux = -aux
                if srcidx[-(int(srcidx[0])+1)] == dstidx[-(int(srcidx[0])+1)]:
                    return self.channels['c' + srcidx[0] + '0' + srcidx[1:]]
                else:
                    return self.channels['c' + srcidx[0] + '1' + srcidx[1:]]
            else:
                return self.channels['c' + srcidx[0] + '0' + srcidx[1:]]
        elif srcidx[-(int(srcidx[0])+1)] == dstidx[-(int(srcidx[0])+1)]:
            return self.channels['c' + srcidx[0] + '0' + srcidx[1:]]
        else:
            return self.channels['c' + srcidx[0] + '1' + srcidx[1:]]

class CCC_DF:
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
        dfs(self.n, self.n, '', nodes)
        for index in nodes:
            name = 'n'+index
            self.nodes[name] = Node(name)

    def initchannels(self):
        channels = []
        for node in self.nodes.values():
            index = node.name[1:]
            for i in range(3):
                channels.append(str(i)+index[0]+'0'+index[1:])
            channels.append('1'+index[0]+'1'+index[1:])
        for index in channels:
            name = 'c'+index
            self.channels[name] = Channel(name, self.chnlen, self.chncap)

    def route(self, flit):
        src, dst, aux = flit.pos, flit.dst, abs(flit.aux)
        if isinstance(src, Node):
            srcidx = src.name[1:]
        else: # channel
            _srcidx = src.name[2] + src.name[4:]
            srcidx = in_dec(_srcidx, self.n) if src.name[3] == '0' else out_flip(_srcidx)
        dstidx = dst.name[1:]
        
        if srcidx == dstidx:
            return None
        elif srcidx[1:] == dstidx[1:]:
            return self.channels['c2' + srcidx[0] + '0' + srcidx[1:]]
        elif flit.aux > 0:
            if int(srcidx[0]) == self.n-1:
                flit.aux = -aux
                if srcidx[-(int(srcidx[0])+1)] == dstidx[-(int(srcidx[0])+1)]:
                    return self.channels['c1' + srcidx[0] + '0' + srcidx[1:]]
                else:
                    return self.channels['c1' + srcidx[0] + '1' + srcidx[1:]]
            else:
                return self.channels['c0' + srcidx[0] + '0' + srcidx[1:]]
        elif srcidx[-(int(srcidx[0])+1)] == dstidx[-(int(srcidx[0])+1)]:
            return self.channels['c1' + srcidx[0] + '0' + srcidx[1:]]
        else:
            return self.channels['c1' + srcidx[0] + '1' + srcidx[1:]]