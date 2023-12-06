import sys
import os
import random
from src.network.KNC import KNC
# from src.network.CCC import CCC
# from src.network.SEN import SEN

def main():
    dir = 'senarios/'
    if not os.path.isdir(dir):
        os.makedirs(dir)

    if len(sys.argv) == 5 and sys.argv[2] == 'knc':
        network = KNC(int(sys.argv[3]), int(sys.argv[4]))
    elif len(sys.argv) == 4 and sys.argv[2] == 'ccc':
        network = CCC(int(sys.argv[3]))
    else:
        print("invalid command.. options you can use:")
        print('python sengen.py [alias] knc [k] [n]')
        print('python sengen.py [alias] ccc [n]')
        return -1

    nodes = list(network.nodes.keys())
    with open(dir + sys.argv[1] + ".sen", 'w') as f:
        f.write("// [endpoint]\n")
        f.write("500\n")

        f.write('\n')

        f.write("// [tick] [source] [destination] [length]\n")
        ticks = sorted(random.choices(range(50), k=50))
        srcs = random.choices(range(len(nodes)), k=50)
        dsts = random.choices(range(len(nodes)), k=50)
        lens = random.choices(range(50), k=50)
        for i in range(50):
            f.write(str(ticks[i]) + ' ' + nodes[srcs[i]] + ' ' + nodes[dsts[i]] + ' ' + str(lens[i]) + '\n')
    
if __name__ == '__main__':
    main()