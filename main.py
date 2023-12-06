import sys
import os
from src.core.Sim import Sim
from src.network.KNC import KNC, KNC_dfree
# from src.network.CCC import CCC, CCC_dfree
# from src.network.SEN import SEN, SEN_dfree

breakpoints = set()

def parse(sim, args: list):
    if len(args) == 0:
        return 1
    if args[0] == 'r':
        if len(args) == 1:
            sim.clear()
            sim.proceed()
            while sim.tick < sim.maxtick and sim.tick not in breakpoints:
                sim.proceed()
            print("simulation stopped at tick " + str(sim.tick))
        else:
            return -1
    elif args[0] == 'c':
        if len(args) == 1:
            sim.proceed()
            while sim.tick < sim.maxtick and sim.tick not in breakpoints:
                sim.proceed()
            print("simulation stopped at tick " + str(sim.tick))
        else:
            return -1
    elif args[0] == 'b':
        if len(args) == 1:
            print("current breakpoints:", end=' ')
            for b in breakpoints:
                print(str(b), end=' ')
            print()
        elif len(args) == 2:
            breakpoints.add(int(args[1]))
            print("current breakpoints:", end=' ')
            for b in breakpoints:
                print(str(b), end=' ')
            print()
        else:
            return -1
    elif args[0] == 'd':
        if len(args) == 1:
            breakpoints.clear()
            print("current breakpoints:", end=' ')
            for b in breakpoints:
                print(str(b), end=' ')
            print()
        elif len(args) == 2:
            if int(args[1]) in breakpoints:
                breakpoints.remove(int(args[1]))
            print("current breakpoints:", end=' ')
            for b in breakpoints:
                print(str(b), end=' ')
            print()
        else:
            return -1
    elif args[0] == 't':
        if len(args) == 1:
            sim.proceed()
            print("simulation stopped at tick " + str(sim.tick))
        elif len(args) == 2:
            tick = sim.tick + int(args[1])
            sim.proceed()
            while sim.tick < sim.maxtick and sim.tick not in breakpoints and sim.tick < tick:
                sim.proceed()
            print("simulation stopped at tick " + str(sim.tick))
        else:
            return -1
    elif args[0] == 'i' and len(args) >= 2:
        target = args[1]
        if target == 'n':
            sim.printnodes()
        elif target == 'c':
            sim.printchannels()
        elif target == 'f':
            sim.printflits()
        elif target == 'r' and len(args) == 4:
            _src, _dst = args[2], args[3]
            if _src in sim.network.nodes:
                src = sim.network.nodes[_src]
            elif _src in sim.network.channels:
                src = sim.network.channels[_src]
            else:
                print("no such element")
                return -1
            if _dst in sim.network.nodes:
                dst = sim.network.nodes[_dst]
            else:
                print("no such element")
                return -1
            result = sim.network.route(src, dst)
            while result:
                print(result.name)
                result = sim.network.route(result, dst)
            print("(end)")
        elif target in sim.network.nodes:
            sim.network.nodes[target].printstat()
        elif target in sim.network.channels:
            sim.network.channels[target].printstat()
        elif target[0] == 'f' and int(target[1:]) < len(sim.flits):
            sim.flits[int(target[1:])].printstat()
        else:
            print("no such element")
    elif args[0] == 'q' and len(args) == 1:
        return 0
    else:
        return -1
    
    return 1

def main():
    if len(sys.argv) == 5 and sys.argv[2] == 'knc':
        network = KNC(int(sys.argv[3]), int(sys.argv[4]))
    elif len(sys.argv) == 5 and sys.argv[2] == 'knc_dfree':
        network = KNC_dfree(int(sys.argv[3]), int(sys.argv[4]))
    elif len(sys.argv) == 4 and sys.argv[2] == 'ccc':
        network = CCC(int(sys.argv[3]))
    elif len(sys.argv) == 4 and sys.argv[2] == 'ccc_dfree':
        network = CCC_dfree(int(sys.argv[3]))
    else:
        print("usage:")
        print('python main.py [alias] knc [k] [n]')
        print('python main.py [alias] knc_dfree [k] [n]')
        print('python main.py [alias] ccc [n]')
        print('python main.py [alias] ccc_dfree [n]')
        exit(-1)

    if not os.path.isfile("senarios/" + sys.argv[1] + ".sen"):
        print("invalid senario")
        exit(-1)
    
    sim = Sim(network, sys.argv[1])
    sim.init()

    while True:
        cmd = input('(LNS) ')
        args = cmd.split()
        ret = parse(sim, args)
        if ret == 0:
            break
        elif ret == -1:
            print("invalid command")
    
if __name__ == '__main__':
    main()