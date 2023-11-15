import sys
import os

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
    
def k_ary_n_cube(dir, k, n):
    nodes = []
    dfs(k, n, '', nodes)

    with open(dir + "/nodes.conf", 'w') as f:
        f.write("// [name]\n")

        for node in nodes:
            f.write('n' + node + "\n")

    channels = []
    for node in nodes:
        for i in range(n):
            channels.append(str(i)+node)
    
    with open(dir + "/channels.conf", 'w') as f:
        f.write("// [name] [length] [capacity]\n")

        for channel in channels:
            f.write('c' + channel + ' ')
            f.write(str(5) + ' ' + str(5) + '\n')
    
    with open(dir + "/routes.conf", "w") as f:
        f.write("//                    [destination]   ...\n")
        f.write("// [current position] [next position] ...\n")
        f.write("// ...                ...             ...\n")

        for node in nodes:
            f.write('\t' + 'n' + node)
        f.write('\n')

        for src in nodes:
            f.write('n' + src + '\t')
            for dst in nodes:
                if src == dst:
                    f.write('-' + '\t')
                else:
                    pos = 0
                    while src[pos] == dst[pos]:
                        pos += 1
                    f.write('c' + str(n-1-pos) + src + '\t')
            f.write('\n')
        
        for channel in channels:
            f.write('c' + channel + '\t')
            for dst in nodes:
                pos = (n-1) - int(channel[0])
                _src = channel[1:]
                src = _src[:pos] + str((int(_src[pos])-1) % k) + _src[pos+1:]
                if src == dst:
                    f.write('-' + '\t')
                else:
                    pos = 0
                    while src[pos] == dst[pos]:
                        pos += 1
                    f.write('c' + str(n-1-pos) + src + '\t')
            f.write('\n')

    with open(dir + "/senario.conf", "w") as f:
        f.write("// [endpoint]\n")
        f.write("50\n")

        f.write('\n')

        f.write("// [tick] [source] [destination] [length]\n")
    
def main():
    dir = 'conf/' + sys.argv[1]
    if not os.path.isdir(dir):
        os.makedirs(dir)

    if len(sys.argv) == 5 and sys.argv[2] == 'k_ary_n_cube':
            k_ary_n_cube(dir, int(sys.argv[3]), int(sys.argv[4]))
    else:
        print("invalid command.. options you can use:")
        print('python setconf.py [alias] k_ary_n_cube [k] [n]')
    
if __name__ == '__main__':
    main()