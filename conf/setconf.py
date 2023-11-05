import sys

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
    
def k_ary_n_cube(k, n):
    nodes = []
    dfs(k, n, '', nodes)

    with open("node.conf", 'w') as f:
        for node in nodes:
            f.write('n' + node + "\n\n")

    channels = []
    for node in nodes:
        for i in range(n):
            channels.append(str(i)+node)
    
    with open("channel.conf", 'w') as f:
        for channel in channels:
            f.write('c' + channel + '\n')
            f.write(str(5) + ' ' + str(5) + '\n')
            f.write('\n')
    
    with open("route.conf", "w") as f:
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
    
def main():
    while True:
        if sys.argv[1] == 'k_ary_n_cube' and len(sys.argv) == 4:
            k_ary_n_cube(int(sys.argv[2]), int(sys.argv[3]))
            break
        else:
            print("invalid command")
    
if __name__ == '__main__':
    main()