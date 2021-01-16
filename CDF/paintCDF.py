import matplotlib.pyplot as plt

# titles = ['spdk-nvme-rr', 'kernel-nvme-rr', 'spdk-nvmf-rr', 'kernel-nvmf-rr', 'spdk-nvme-rw', 'kernel-nvme-rw', 'spdk-nvmf-rw', 'kernel-nvmf-rw']
titles = ['spdk-nvme-rr', 'kernel-nvme-rr', 'spdk-nvmf-rr', 'kernel-nvmf-rr']
# titles = ['kernel-nvme-rr','kernel-nvme-rw','kernel-nvmf-rr','kernel-nvmf-rw', 'spdk-nvme-rr', 'spdk-nvme-rw']
# titles = ['kernel-nvme-rr','spdk-nvme-rr']
# titles = ['kernel-nvme-rw']
marker_num = 10
result = [list() for i in range(len(titles))]

x = [list() for i in range(len(titles))]
y = [list() for i in range(len(titles))]

figure, ax = plt.subplots(figsize=(12, 6))

file_names = []
for title in titles:
	file_names.append(title + ".log")


for i in range(len(file_names)):
	with open(file_names[i]) as file_obj:
		for content in file_obj:
			strlist = content.split(',')
			v = float(strlist[1])
			result[i].append(v/1000)

for i in range(len(result)):
	result[i].sort()

percent_90 = 0
percent_99 = 0
for i in range(len(result)):
	percent_90 = 0
	percent_99 = 0
	total_num = len(result[i])
	old = result[i][0]
	sum = 1
	for j in range(1, len(result[i])):
		new = result[i][j]
		if (new == old):
			sum += 1
			continue
		else:
			for k in range(sum):
				x[i].append(old)
				y[i].append(j*1.0/total_num) # CDF图=>小于当前值的数量占total数量的比例
			if percent_90 == 0 and j*1.0/total_num >= 0.9:
				print('%s 90 percent %f' % (titles[i], new))
				percent_90 = 1
			if percent_99 == 0 and j*1.0/total_num >= 0.99:
				print('%s 99 percent %f' % (titles[i], new))
				percent_99 = 1
			old = new
			sum = 1
	for k in range(sum): # 上面else的两个append在最后执行，CDF为1的点
		x[i].append(old)
		y[i].append(1.0)


font1 = {'family' : 'Times New Roman',
'weight' : 'normal',
'size' : 16
}
font2 = {'family' : 'Times New Roman',
'weight' : 'normal',
'size' : 22
}
labels = ax.get_xticklabels() + ax.get_yticklabels()
# print labelsax
[label.set_fontname('Times New Roman') for label in labels]

plt.ylim((0, 1.1))
plt.xlim((25, 115))

#The scale setting of the coordinate axis is inward (in)
ax.tick_params(axis='both',which='both', labelsize=16, direction='in')
plt.xlabel('Latency(us)', font2)
plt.ylabel('CDF', font2)

# 这里默认最多8种线条的属性，线条颜色，标记类型，标记颜色
line_attributes = [
	{'color' : '#515151', 'marker' : 'o', 'markerfacecolor': '#515151'},
	{'color' : '#F14040', 'marker' : 'o', 'markerfacecolor': 'white'},
	{'color' : '#1A6FDF', 'marker' : '^', 'markerfacecolor': '#1A6FDF'},
	{'color' : '#37AD6B', 'marker' : '^', 'markerfacecolor': 'white'},
	{'color' : '#B177DE', 'marker' : 's', 'markerfacecolor': '#B177DE'},
	{'color' : '#CC9900', 'marker' : 's', 'markerfacecolor': 'white'},
	{'color' : '#00CBCC', 'marker' : 'H', 'markerfacecolor': '#00CBCC'},
	{'color' : '#7D4E4E', 'marker' : 'H', 'markerfacecolor': 'white'}]

if len(x) > 8:
	print("实例超过8个")
	exit(-1)
for i in range(len(x)):
	plt.plot(x[i], y[i], '-', linewidth='3', color=line_attributes[i]["color"], marker=line_attributes[i]["marker"],\
			 				markerfacecolor=line_attributes[i]["markerfacecolor"], markersize=10, \
			 				markevery=list(range(int(len(x[i])/marker_num), len(x[i]), int(len(x[i])/marker_num)))) # markevery默认打marker_num个点

plt.legend(titles, loc='upper left', prop=font1, edgecolor='white')

#plt.show()
plt.savefig('./t.png', dpi = 600)
