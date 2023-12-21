from matplotlib import pyplot as plt

x_axis = {}
x_axis['knc'] = [9, 27, 64, 81, 256]
x_axis['ccc'] = [8, 24, 64, 160, 384]
x_axis['sen'] = [8, 32, 64, 128, 256]

y_axis = {}
y_axis['knc_rr'] = [0, 0, 0, 0, 0]
y_axis['knc_fcfs'] = [0, 0, 0, 0, 0]
y_axis['knc_of'] = [0, 0, 0, 0, 0]
y_axis['ccc_rr'] = [0, 0, 0, 0, 0]
y_axis['ccc_fcfs'] = [0, 0, 0, 0, 0]
y_axis['ccc_of'] = [0, 0, 0, 0, 0]
y_axis['sen_rr'] = [0, 0, 0, 0, 0]
y_axis['sen_fcfs'] = [0, 0, 0, 0, 0]
y_axis['sen_of'] = [0, 0, 0, 0, 0]

for net in ['knc', 'ccc', 'sen']:
    for i in range(5):
        scale = x_axis[net][i]
        for idx in range(1, 101):
            for policy in ['rr', 'fcfs', 'of']:
                f = open("test/data/" + net + '_' + str(scale) + '_' + str(idx) + '_' + policy + ".log", 'r')
                avgticks = float(f.readlines()[1].split()[1])
                y_axis[net + '_' + policy][i] += avgticks
                f.close()

for legend, sums in y_axis.items():
    print(legend, end='\t')
    for i in range(5):
        sums[i] = round(sums[i]/100, 2) # average
        print(sums[i], end='\t')
    print()

plt.title('average ticks spent (RR)')
for net in ['knc', 'ccc', 'sen']:
    for policy in ['rr']:
        label = net + '_' + policy
        plt.plot(x_axis[net], y_axis[label], label=label)
plt.xlim(0, 260)
plt.legend()
plt.show()

plt.title('average ticks spent (SEN)')
for net in ['sen']:
    for policy in ['rr', 'fcfs', 'of']:
        label = net + '_' + policy
        plt.plot(x_axis[net], y_axis[label], label=label)
plt.xlim(0, 260)
plt.legend()
plt.show()