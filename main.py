from Sim import * 
import sys
import os

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
        elif target == 'r':
            if len(args) == 2:
                sim.printroutes()
            elif len(args) == 4:
                src, dst = args[2], args[3]
                if (src, dst) in sim.routes:
                    print(sim.routes[(src, dst)].name)
                else:
                    print("no such element")
            else:
                return -1
        elif target in sim.nodes:
            sim.nodes[target].printstat()
        elif target in sim.channels:
            sim.channels[target].printstat()
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
    if len(sys.argv) != 2:
        print("usage: python main.py [conf_alias]")
        exit(-1)

    dir = "conf/" + sys.argv[1]
    if not os.path.isfile(dir + "/nodes.conf") or \
        not os.path.isfile(dir + "/channels.conf") or \
        not os.path.isfile(dir + "/routes.conf") or \
        not os.path.isfile(dir + "/senario.conf"):
        print("invalid configuration")
        exit(-1)
    
    sim = Sim(dir)
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