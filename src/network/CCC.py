import random

def out_flip(x):
    dim = int(x[0])
    pos = (len(x)-1) - dim
    flipped = '0' if x[pos] == '1' else '1'
    return x[:pos] + flipped + x[pos+1:]

def in_dec(x, n):
    deced = str((int(x[0])-1) % n)
    return deced + x[1:]

def route(src, dst):
    if src == dst:
        return '-'
    elif src[-(int(src[0])+1)] == dst[-(int(src[0])+1)]:
        return 'c' + src[0] + '0' + src[1:]
    else:
        return 'c' + src[0] + '1' + src[1:]

def route_dfree(src, dst, phase, n):
    if src == dst:
        return '-'
    elif src[1:] == dst[1:] or phase == '20':
        return 'c2' + src[0] + '0' + src[1:]
    elif phase == '00':
        if int(src[0]) == n-1:
            if src[-(int(src[0])+1)] == dst[-(int(src[0])+1)]:
                return 'c1' + src[0] + '0' + src[1:]
            else:
                return 'c1' + src[0] + '1' + src[1:]
        else:
            return 'c0' + src[0] + '0' + src[1:]
    elif phase == '10' or phase == '11':
        if src[-(int(src[0])+1)] == dst[-(int(src[0])+1)]:
            return 'c1' + src[0] + '0' + src[1:]
        else:
            return 'c1' + src[0] + '1' + src[1:]

def dfs(i, n, x, arr:list):
    if i == 0:
        for j in range(n):
            arr.append(str(j)+x)
        return
    
    for j in range(2):
        dfs(i-1, n, x+str(j), arr)

def cube_connected_cycle(dir, n, dfree):
    nodes = []
    dfs(n, n, '', nodes)

    with open(dir + "/nodes.conf", 'w') as f:
        f.write("// [name]\n")

        for node in nodes:
            f.write('n' + node + "\n")

    channels = []
    for node in nodes:
        if dfree:
            for i in range(3):
                channels.append(str(i)+node[0]+'0'+node[1:])
            channels.append('1'+node[0]+'1'+node[1:])
        else:
            for i in range(2):
                channels.append(node[0]+str(i)+node[1:])
    
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
                if dfree:
                    f.write(route_dfree(src, dst, '00', n) + '\t')
                else:
                    f.write(route(src, dst) + '\t')
            f.write('\n')
        
        for channel in channels:
            f.write('c' + channel + '\t')
            if dfree:
                prev = channel[1] + channel[3:]
                phase = channel[0] + channel[2]
                src = in_dec(prev, n) if channel[2] == '0' else out_flip(prev)
                for dst in nodes:
                    f.write(route_dfree(src, dst, phase, n) + '\t')
            else:
                prev = channel[0] + channel[2:]
                src = in_dec(prev, n) if channel[1] == '0' else out_flip(prev)
                for dst in nodes:
                    f.write(route(src, dst) + '\t')
            f.write('\n')

    with open(dir + "/senario.conf", "w") as f:
        f.write("// [endpoint]\n")
        f.write("500\n")

        f.write('\n')

        f.write("// [tick] [source] [destination] [length]\n")

        ticks = sorted(random.choices(range(50), k=50))
        srcs = random.choices(range(len(nodes)), k=50)
        dsts = random.choices(range(len(nodes)), k=50)
        lens = random.choices(range(50), k=50)
        for i in range(50):
            f.write(str(ticks[i]) + ' n' + nodes[srcs[i]] + ' n' + nodes[dsts[i]] + ' ' + str(lens[i]) + '\n')
    