import sys
import os
import random
from src.network.KNC import KNC
from src.network.CCC import CCC
from src.network.SEN import SEN
from src.network.elem.Channel import Policy

def main():
    dir = 'conf/'
    if not os.path.isdir(dir):
        os.makedirs(dir)

    files = []
    files.append(open(dir + sys.argv[1] + ".conf", 'w'))
    files.append(open(dir + sys.argv[1] + '_rr' + ".conf", 'w'))
    files.append(open(dir + sys.argv[1] + '_fcfs' + ".conf", 'w'))
    files.append(open(dir + sys.argv[1] + '_of' + ".conf", 'w'))

    for file in files:
        file.write("// [algorithm] [args..] [policy]\n")

    if len(sys.argv) == 5 and sys.argv[2].upper() == 'KNC':
        network = KNC(int(sys.argv[3]), int(sys.argv[4]), Policy.DEFAULT)
        for file in files:
            file.write("KNC" + ' ' + sys.argv[3] + ' ' + sys.argv[4] + ' ')
    elif len(sys.argv) == 4 and sys.argv[2].upper() == 'CCC':
        network = CCC(int(sys.argv[3]), Policy.DEFAULT)
        for file in files:
            file.write("CCC" + ' ' + sys.argv[3] + ' ')
    elif len(sys.argv) == 4 and sys.argv[2].upper() == 'SEN':
        network = SEN(int(sys.argv[3]), Policy.DEFAULT)
        for file in files:
            file.write("SEN" + ' ' + sys.argv[3] + ' ')
    else:
        print("invalid command.. options you can use:")
        print('python setconf.py [alias] KNC [k] [n]')
        print('python setconf.py [alias] CCC [n]')
        print('python setconf.py [alias] SEN [n]')
        file.close()
        return -1

    files[0].write("DEFAULT\n\n")
    files[1].write("RR\n\n")
    files[2].write("FCFS\n\n")
    files[3].write("OF\n\n")

    for file in files:
        file.write("// [endpoint]\n")
        file.write("5000\n\n")

    nodes = list(network.nodes.keys())
    ticks = sorted(random.choices(range(50), k=50))
    srcs = random.choices(range(len(nodes)), k=50)
    dsts = random.choices(range(len(nodes)), k=50)
    lens = random.choices(range(50), k=50)

    for file in files:
        file.write("// [tick] [source] [destination] [length]\n")
        for i in range(50):
            file.write(str(ticks[i]) + ' ' + nodes[srcs[i]] + ' ' + nodes[dsts[i]] + ' ' + str(lens[i]) + '\n')

    for file in files:
        file.close()
    
if __name__ == '__main__':
    main()