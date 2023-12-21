policies = ['', '_rr', '_fcfs', '_of'] # len=4
nets = ['knc', 'ccc', 'sen'] # len=3
deadlocks = [[0 for _ in range(3)] for _ in range(4)]
avg_ticks = [[0 for _ in range(3)] for _ in range(4)]

for idx in range(1, 101):
    for i in range(4):
        policy = policies[i]
        for j in range(3):
            net = nets[j]
            f = open("test/data/" + net + str(idx) + policy + ".log")
            for line in f.readlines():
                tokens = line.split()
                if tokens[0] == "deadlock:":
                    deadlocks[i][j] += 1 if tokens[1] == "YES" else 0
                elif tokens[0] == "avg_ticks:":
                    avg_ticks[i][j] += float(tokens[1])
            f.close()

for i in range(4):
    for j in range(3):
        avg_ticks[i][j] /= 100

print("number of deadlocks occurred:")
print('\t' + "knc\t" + "ccc\t" + "sen\t")
for i in range(4):
    print(policies[i], end='\t')
    for j in range(3):
        print(deadlocks[i][j], end='\t')
    print()
print()

print("average ticks spent:")
print('\t' + "knc\t" + "ccc\t" + "sen\t")
for i in range(4):
    print(policies[i], end='\t')
    for j in range(3):
        print(round(avg_ticks[i][j], 2), end='\t')
    print()
print()