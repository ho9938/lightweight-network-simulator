import sys
import os
from src.algorithm.k_ary_n_cube import *
from src.algorithm.cube_connected_cycle import *

def main():
    dir = 'conf/' + sys.argv[1]
    if not os.path.isdir(dir):
        os.makedirs(dir)

    if len(sys.argv) == 5 and sys.argv[2] == 'k_ary_n_cube':
            k_ary_n_cube(dir, int(sys.argv[3]), int(sys.argv[4]), False)
    elif len(sys.argv) == 5 and sys.argv[2] == 'k_ary_n_cube_dfree':
            k_ary_n_cube(dir, int(sys.argv[3]), int(sys.argv[4]), True)
    elif len(sys.argv) == 4 and sys.argv[2] == 'cube_connected_cycle':
            cube_connected_cycle(dir, int(sys.argv[3]), False)
    elif len(sys.argv) == 4 and sys.argv[2] == 'cube_connected_cycle_dfree':
            cube_connected_cycle(dir, int(sys.argv[3]), True)
    else:
        print("invalid command.. options you can use:")
        print('python setconf.py [alias] k_ary_n_cube [k] [n]')
        print('python setconf.py [alias] k_ary_n_cube_dfree [k] [n]')
        print('python setconf.py [alias] cube_connected_cycle [n]')
        print('python setconf.py [alias] cube_connected_cycle_dfree [n]')
    
if __name__ == '__main__':
    main()