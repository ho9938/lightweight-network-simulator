from enum import Enum, auto

class Flit:
    def __init__(self, index:int, src:str, dst:str, next:int):
        self.index = index
        self.src = src
        self.dst = dst
        self.pos = src
        self.next = next
        self.tick = 0
        self.tottick = 0
    
    def printsummary(self):
        print('f' + str(self.index) + ':', end='\t')
        print(self.src + " -> " + self.dst + ',', end='\t')
        print("current position: " + self.pos + ',', end='\t')
        print(str(self.tick) + " ticks in current queue")

    def printstat(self):
        print("source: " + self.src)
        print("destination: " + self.dst)
        print("current position: " + str(self.pos))
        print("tick in current queue: " + str(self.tick))
        print("total tick since created: " + str(self.tottick))
    
class Channel:
    def __init__(self, name, length, capacity):
        self.name = name
        self.src = ''
        self.dst = ''
        self.length = length
        self.queue = []
        self.size = 0
        self.capacity = capacity

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

class Node:
    def __init__(self, name:str):
        self.name = name
        self.senario = []
        self.queue = []

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

class FlitGen:
    def __init__(self, tick:int, src:str, dst:str, length:int):
        self.tick = tick
        self.src = src
        self.dst = dst
        self.length = length
    
    def printsummary(self):
        print("[t" + str(self.tick) + ']', end='\t')
        print("source: " + self.src, end='\t')
        print("destination: " + self.dst, end='\t')
        print("packet length: " + str(self.length))

class Sim:
    def __init__(self, dir):
        self.maxtick = -1
        self.tick = 0
        self.nodes = {}
        self.channels = {}
        self.routes = {}
        self.flits = []
        self.dir = dir
    
    def init(self):
        self.readnodes()
        self.readchannels()
        self.readroutes()
        self.readsenario()
        self.printstat()

    def invalidconf(self, filename):
        print("invalid " + filename)
        exit(-1)

    def readnodes(self):
        with open(self.dir + '/nodes.conf', 'r') as f:
            for line in f.readlines():
                if len(line) >= 2 and line[:2] == "//":
                    continue
                args = line.split()
                if len(args) == 0 :
                    continue
                elif len(args) == 1:
                    node = Node(args[0])
                    self.nodes[node.name] = node
                else:
                    self.invalidconf('nodes.conf')
    
    def readchannels(self):
        with open(self.dir + '/channels.conf', 'r') as f:
            for line in f.readlines():
                if len(line) >= 2 and line[:2] == "//":
                    continue
                args = line.split()
                if len(args) == 0 :
                    continue
                elif len(args) == 3:
                    channel = Channel(args[0], int(args[1]), int(args[2]))
                    self.channels[channel.name] = channel
                else:
                    self.invalidconf('channels.conf')
    
    def readroutes(self):
        with open(self.dir + '/routes.conf', 'r') as f:
            is_top = True
            for line in f.readlines():
                if len(line) >= 2 and line[:2] == "//":
                    continue
                args = line.split()
                if len(args) == 0 :
                    continue
                if is_top:
                    nodes = args
                    if len(nodes) != len(self.nodes):
                        self.invalidconf('routes.conf')
                    for nodename in nodes:
                        if nodename not in self.nodes:
                            self.invalidconf('routes.conf')
                    is_top = False
                    continue

                if len(args) != len(nodes) + 1:
                    self.invalidconf('routes.conf')
                src = args[0]
                if (src not in self.nodes) and (src not in self.channels):
                    self.invalidconf('routes.conf')
                for dst, chn in zip(nodes, line.split()[1:]):
                    if dst not in self.nodes:
                        self.invalidconf('routes.conf')
                    if chn == '-':
                        continue
                    elif not chn in self.channels:
                        self.invalidconf('routes.conf')
                    self.routes[(src, dst)] = self.channels[chn]
    
    def readsenario(self):
        with open(self.dir + '/senario.conf', 'r') as f:
            is_top = True
            for line in f.readlines():
                if len(line) >= 2 and line[:2] == "//":
                    continue
                args = line.split()
                if len(args) == 0 :
                    continue
                if is_top:
                    if len(args) != 1:
                        self.invalidconf('senario.conf')
                    self.maxtick = int(args[0])
                    is_top = False
                    continue

                if len(args) != 4:
                    self.invalidconf('senario.conf')
                tick, length = int(args[0]), int(args[3])
                src, dst = args[1], args[2]
                if src not in self.nodes or dst not in self.nodes:
                    self.invalidconf('senario.conf')
                self.nodes[src].senario.append(FlitGen(tick, src, dst, length))
        
        for node in self.nodes.values():
            node.senario.sort(key=lambda x: x.tick)
                    
    def printstat(self):
        print("<Lightweigth Network Simulator>")
        print()

        print("nodes: ")
        self.printnodes()
        print()

        print("channels: ")
        self.printchannels()
        print()
    
        print("routes: ")
        self.printroutes()
        print()

        print("senario: ")
        self.printsenario()
        print()

    def printnodes(self):
        for node in self.nodes.values():
            node.printsummary()
    
    def printchannels(self):
        for channel in self.channels.values():
            channel.printsummary()
        
    def printroutes(self):
        print('\t', end='')
        for dst in self.nodes.values():
            print(dst.name, end='\t')
        print()
        for src in self.nodes.values():
            print(src.name, end='\t')
            for dst in self.nodes.values():
                if (src.name, dst.name) in self.routes:
                    print(self.routes[(src.name, dst.name)].name, end='\t')
                else:
                    print('-', end='\t')
            print()
        for src in self.channels.values():
            print(src.name, end='\t')
            for dst in self.nodes.values():
                if (src.name, dst.name) in self.routes:
                    print(self.routes[(src.name, dst.name)].name, end='\t')
                else:
                    print('-', end='\t')
            print()
    
    def printflits(self):
        for flit in self.flits:
            flit.printsummary()
    
    def printsenario(self):
        senarios = []
        for node in self.nodes.values():
            for sen in node.senario:
                senarios.append(sen)

        senarios.sort(key=lambda x: (x.tick, x.src))

        for sen in senarios:
            sen.printsummary()

    def proceed(self):
        self.tick += 1

        for node in self.nodes.values():
            while len(node.senario) > 0 and node.senario[0].tick <= self.tick:
                flitgen = node.senario[0]
                node.senario.pop(0)

                for _ in range(flitgen.length - 1):
                    index = len(self.flits)
                    flit = Flit(index, node.name, flitgen.dst, index+1)
                    self.flits.append(flit)
                    node.queue.append(flit)
                flit = Flit(len(self.flits), node.name, flitgen.dst, -1)
                self.flits.append(flit)
                node.queue.append(flit)

            if len(node.queue) > 0:
                flit = node.queue[0]
                if (node.name, flit.dst) not in self.routes:
                    pass
                else:
                    route = self.routes[(node.name, flit.dst)]
                    if route.is_available(flit.index):
                        node.queue.pop(0)
                        route.queue.append(flit)
                        flit.pos = route.name
                        flit.tick = 0

        for channel in self.channels.values():
            if len(channel.queue) > 0:
                flit = channel.queue[0]
                if flit.tick >= channel.length:
                    if (channel.name, flit.dst) not in self.routes:
                        channel.queue.pop(0)
                        flit.pos = "removed"
                        flit.tick = 0
                    else:
                        route = self.routes[(channel.name, flit.dst)]
                        if route.is_available(flit.index):
                            channel.queue.pop(0)
                            route.queue.append(flit)
                            flit.pos = route.name
                            flit.tick = 0

        for node in self.nodes.values():
            node.refresh()

        for channel in self.channels.values():
            channel.refresh()
    
    def clear(self):
        self.tick = 0
        self.flits.clear()
