class Flit:
    def __init__(self, index, src, dst, next):
        self.index = index
        self.src = src
        self.dst = dst
        self.pos = src
        self.next = next
        self.tick = 0
        self.tottick = 0
    
    def printsummary(self):
        print('f' + str(self.index) + ':', end='\t')
        print(self.src.name + " -> " + self.dst.name + ',', end='\t')
        print("current position: " + self.pos + ',', end='\t')
        print(str(self.tick) + " ticks in current queue")

    def printstat(self):
        print("source: " + self.src.name)
        print("destination: " + self.dst.name)
        print("current position: " + str(self.pos))
        print("tick in current queue: " + str(self.tick))
        print("total tick since created: " + str(self.tottick))
    
class FlitGen:
    def __init__(self, tick, src, dst, length):
        self.tick = tick
        self.src = src
        self.dst = dst
        self.length = length
    
    def printsummary(self):
        print("[t" + str(self.tick) + ']', end='\t')
        print("source: " + self.src.name, end='\t')
        print("destination: " + self.dst.name, end='\t')
        print("packet length: " + str(self.length))

class Sim:
    def __init__(self, network, alias):
        self.maxtick = -1
        self.tick = 0
        self.network = network
        self.flits = []
        self.alias = alias
    
    def init(self):
        self.readsenario()
        self.printstat()

    def invalidconf(self, filename):
        print("invalid " + filename)
        exit(-1)

    def readsenario(self):
        with open("senarios/" + self.alias + ".sen", 'r') as f:
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
                _src, _dst = args[1], args[2]
                if _src not in self.network.nodes or _dst not in self.network.nodes:
                    self.invalidconf('senario.conf')
                src = self.network.nodes[_src]
                dst = self.network.nodes[_dst]
                src.senario.append(FlitGen(tick, src, dst, length))
        
        for node in self.network.nodes.values():
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
    
        print("senario: ")
        self.printsenario()
        print()

    def printnodes(self):
        for node in self.network.nodes.values():
            node.printsummary()
    
    def printchannels(self):
        for channel in self.network.channels.values():
            channel.printsummary()
        
    def printflits(self):
        for flit in self.flits:
            flit.printsummary()
    
    def printsenario(self):
        senarios = []
        for node in self.network.nodes.values():
            for sen in node.senario:
                senarios.append(sen)

        senarios.sort(key=lambda x: (x.tick, x.src.name))

        for sen in senarios:
            sen.printsummary()

    def proceed(self):
        self.tick += 1

        for node in self.network.nodes.values():
            while len(node.senario) > 0 and node.senario[0].tick <= self.tick:
                flitgen = node.senario[0]
                node.senario.pop(0)

                if node == flitgen.dst:
                    continue

                for _ in range(flitgen.length - 1):
                    index = len(self.flits)
                    flit = Flit(index, node, flitgen.dst, index+1)
                    self.flits.append(flit)
                    node.queue.append(flit)
                flit = Flit(len(self.flits), node, flitgen.dst, -1)
                self.flits.append(flit)
                node.queue.append(flit)

            if len(node.queue) > 0:
                flit = node.queue[0]
                target = self.network.route(node, flit.dst)
                if not target:
                    node.queue.pop(0)
                    flit.pos = "removed"
                    flit.tick = 0
                elif target.is_available(flit.index):
                    node.queue.pop(0)
                    target.queue.append(flit)
                    flit.pos = target.name
                    flit.tick = 0

        for channel in self.network.channels.values():
            if len(channel.queue) > 0:
                flit = channel.queue[0]
                if flit.tick >= channel.length:
                    target = self.network.route(channel, flit.dst)
                    if not target:
                        channel.queue.pop(0)
                        flit.pos = "removed"
                        flit.tick = 0
                    elif target.is_available(flit.index):
                        channel.queue.pop(0)
                        target.queue.append(flit)
                        flit.pos = target.name
                        flit.tick = 0

        for node in self.network.nodes.values():
            node.refresh()

        for channel in self.network.channels.values():
            channel.refresh()
    
    def clear(self):
        self.tick = 0

        for node in self.network.nodes.values():
            node.clear()
        for channel in self.network.channels.values():
            channel.clear()
        self.flits.clear()

        self.readsenario()
