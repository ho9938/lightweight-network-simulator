import sys
import os
import random
from src.network.KNC import KNC
from src.network.CCC import CCC
# from src.network.SEN import SEN

def main():
    dir = 'conf/'
    if not os.path.isdir(dir):
        os.makedirs(dir)

    file = open(dir + sys.argv[1] + ".conf", 'w')
    file.write("// [algorithm] [args..]\n")

    if len(sys.argv) == 5 and sys.argv[2].upper() in ['KNC', 'KNC_DF']:
        network = KNC(int(sys.argv[3]), int(sys.argv[4]))
        file.write(sys.argv[2] + ' ' + sys.argv[3] + ' ' + sys.argv[4] + "\n\n")
    elif len(sys.argv) == 4 and sys.argv[2].upper() in ['CCC', 'CCC_DF']:
        network = CCC(int(sys.argv[3]))
        file.write(sys.argv[2].upper() + ' ' + sys.argv[3] + ' ' + "\n\n")
    else:
        print("invalid command.. options you can use:")
        print('python setconf.py [alias] KNC [k] [n]')
        print('python setconf.py [alias] KNC_DF [k] [n]')
        print('python setconf.py [alias] CCC [n]')
        print('python setconf.py [alias] CCC_DF [n]')
        file.close()
        return -1

    file.write("// [endpoint]\n")
    file.write("500\n\n")

    nodes = list(network.nodes.keys())
    ticks = sorted(random.choices(range(50), k=50))
    srcs = random.choices(range(len(nodes)), k=50)
    dsts = random.choices(range(len(nodes)), k=50)
    lens = random.choices(range(50), k=50)

    file.write("// [tick] [source] [destination] [length]\n")
    for i in range(50):
        file.write(str(ticks[i]) + ' ' + nodes[srcs[i]] + ' ' + nodes[dsts[i]] + ' ' + str(lens[i]) + '\n')
    
if __name__ == '__main__':
    main()