from .elem.Node import Node
from .elem.Channel import Channel

def chgbase(x, k, n):
    result = ''

    while x > 0:
        x, mod = divmod(x, k)
        result += str(mod)

    result += '0' * (n - len(result))
    return result[::-1] 

def dfs(k, n, x, arr:list):
    if n == 0:
        arr.append(x)
        return
    
    for i in range(k):
        dfs(k, n-1, x+str(i), arr)

class KNC:
    def __init__(self, k, n):
        self.k = k
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
        dfs(self.k, self.n, '', nodes)
        for index in nodes:
            name = 'n'+index
            self.nodes[name] = Node(name)

    def initchannels(self):
        channels = []
        for node in self.nodes.values():
            index = node.name[1:]
            for i in range(self.n):
                channels.append(str(i)+index)
        for index in channels:
            name = 'c'+index
            self.channels[name] = Channel(name, self.chnlen, self.chncap)

    def route(self, src, dst):
        if isinstance(src, Node):
            srcidx = src.name[1:]
        else: # channel
            pos = (self.n-1) - int(src.name[1])
            _srcidx = src.name[2:]
            srcidx = _srcidx[:pos] + str((int(_srcidx[pos])-1) % self.k) + _srcidx[pos+1:]
        dstidx = dst.name[1:]
        
        if srcidx == dstidx:
            return None
        else:
            pos = 0
            while srcidx[pos] == dstidx[pos]:
                pos += 1
            return self.channels['c' + str(self.n-1-pos) + srcidx]
    
class KNC_dfree:
    def __init__(self, k, n):
        self.k = k
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
        dfs(self.k, self.n, '', nodes)
        for index in nodes:
            name = 'n'+index
            self.nodes[name] = Node(name)

    def initchannels(self):
        channels = []
        for node in self.nodes.values():
            for i in range(self.n):
                for j in range(2):
                    channels.append(str(i)+str(j)+node)
        for index in channels:
            name = 'c'+index
            self.channels[name] = Channel(name, self.chnlen, self.chncap)

    def route(self, src, dst):
        if isinstance(src, Node):
            srcidx = src.name[1:]
        else: # channel
            pos = (self.n-1) - int(src.name[1])
            _srcidx = src.name[3:]
            srcidx = _srcidx[:pos] + str((int(_srcidx[pos])-1) % self.k) + _srcidx[pos+1:]
        dstidx = dst.name[1:]
        
        if srcidx == dstidx:
            return None
        else:
            pos = 0
            while srcidx[pos] == dstidx[pos]:
                pos += 1
            if srcidx[pos] < dstidx[pos] and srcidx[pos] != 0:
                return self.channels['c' + str(self.n-1-pos) + '1' + srcidx]
            else:
                return self.channels['c' + str(self.n-1-pos) + '0' + srcidx]