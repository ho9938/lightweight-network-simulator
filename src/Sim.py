from src.network.KNC import KNC
from src.network.CCC import CCC
from src.network.SEN import SEN
from src.network.elem.Channel import Policy

class Flit:
    def __init__(self, index, src, dst, next):
        self.index = index
        self.src = src
        self.dst = dst
        self.pos = src
        self.next = next
        self.tick = 0
        self.tottick = 0
        self.aux = 1
    
    def printsummary(self):
        print('f' + str(self.index) + ':', end='\t')
        print(self.src.name + " -> " + self.dst.name + ',', end='\t')
        print("current position: " + (self.pos.name if self.pos else "removed") + ',', end='\t')
        print(str(self.tick) + " ticks in current queue")

    def printstat(self):
        print("source: " + self.src.name)
        print("destination: " + self.dst.name)
        print("current position: " + (self.pos.name if self.pos else "removed"))
        print("tick in current queue: " + str(self.tick))
        print("total tick since created: " + str(self.tottick))
    
    def markremoved(self):
        self.pos = None
        self.tick = 0
    
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
    def __init__(self, alias):
        self.maxtick = -1
        self.tick = 0
        self.network = None
        self.flits = []
        self.alias = alias
        self.readscenario()
    
    def invalidconf(self):
        print("invalid configuration")
        exit(-1)

    def readscenario(self):
        with open("conf/" + self.alias + ".conf", 'r') as f:
            index = 0
            for line in f.readlines():
                if len(line) >= 2 and line[:2] == "//":
                    continue
                args = line.split()
                if len(args) == 0 :
                    continue

                if index == 0:
                    if len(args) == 4 and args[0] == 'KNC':
                        self.network = KNC(int(args[1]), int(args[2]), Policy.getpolicy(args[3]))
                    elif len(args) == 3 and args[0] == 'CCC':
                        self.network = CCC(int(args[1]), Policy.getpolicy(args[2]))
                    elif len(args) == 3 and args[0] == 'SEN':
                        self.network = SEN(int(args[1]), Policy.getpolicy(args[2]))
                    else:
                        self.invalidconf()
                elif index == 1:
                    if len(args) != 1:
                        self.invalidconf()
                    self.maxtick = int(args[0])
                else:
                    if len(args) != 4:
                        self.invalidconf()
                    tick, length = int(args[0]), int(args[3])
                    _src, _dst = args[1], args[2]
                    if _src not in self.network.nodes or _dst not in self.network.nodes:
                        self.invalidconf()
                    src = self.network.nodes[_src]
                    dst = self.network.nodes[_dst]
                    src.scenario.append(FlitGen(tick, src, dst, length))
                    
                index += 1
        
        for node in self.network.nodes.values():
            node.scenario.sort(key=lambda x: x.tick)
                    
    def printstat(self):
        print("<Lightweigth Network Simulator>")
        print()

        print("nodes: ")
        self.printnodes()
        print()

        print("channels: ")
        self.printchannels()
        print()
    
        print("scenario: ")
        self.printscenario()
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
    
    def printscenario(self):
        scenarios = []
        for node in self.network.nodes.values():
            for sen in node.scenario:
                scenarios.append(sen)

        scenarios.sort(key=lambda x: (x.tick, x.src.name))

        for sen in scenarios:
            sen.printsummary()
        
    def printresult(self):
        deadlock = False
        tottick = 0

        for flit in self.flits:
            if flit.pos:
                deadlock = True
            tottick += flit.tottick
            
        print("deadlock: " + ("YES" if deadlock else "NO"))
        print("average ticks spent: " + str(tottick / len(self.flits)))

    def proceed(self):
        self.tick += 1

        for node in self.network.nodes.values():
            while len(node.scenario) > 0 and node.scenario[0].tick <= self.tick:
                flitgen = node.scenario[0]
                node.scenario.pop(0)

                if node == flitgen.dst:
                    continue

                for _ in range(flitgen.length - 1):
                    index = len(self.flits)
                    flit = Flit(index, node, flitgen.dst, index+1)
                    self.flits.append(flit)
                    node.queue.append(flit)
                flit = Flit(len(self.flits), node, flitgen.dst, -1)
                self.flits.append(flit)
                node.push(flit)

            if len(node.queue) > 0:
                flit = node.queue[0]
                target = self.network.route(flit)
                if not target:
                    node.pop()
                elif target.is_available(flit.index):
                    node.pop()
                    target.push(flit)

        for pchannel in self.network.channels.values():
            indices = pchannel.geturgent()
            for index in indices:
                vchannel = pchannel.vchannels[index]
                if len(vchannel.queue) <= 0:
                    continue
                flit = vchannel.queue[0]
                if flit.tick < vchannel.length:
                    continue
                target = self.network.route(flit)
                if not target:
                    continue
                if target.is_available(flit.index):
                    vchannel.pop()
                    target.push(flit)
                    pchannel.setlatest(index)
                    break

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

        self.readscenario()
