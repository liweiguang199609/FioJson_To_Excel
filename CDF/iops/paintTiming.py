import matplotlib.pyplot as plt
import os
import re

path = "E:\python-code\FioJson_To_Excel\CDF\iops"

def getfilelist(strn):
	names = []
	for dirpath, dirnames, filenames in os.walk(path):
		for filepath in filenames:
			# image_name=os.path.join(dirpath, filepath)#获取文件的全路径
			image_name = filepath
			str1 = re.compile(strn + '''(.*?).log''')
			match_obj = re.findall(str1, image_name)
			if match_obj:
				print(image_name)
				names.append(image_name)
	return names

# titles = ['spdk-nvme-rr', 'kernel-nvme-rr', 'spdk-nvmf-rr', 'kernel-nvmf-rr', 'spdk-nvme-rw', 'kernel-nvme-rw', 'spdk-nvmf-rw', 'kernel-nvmf-rw']
# titles = ['spdk-nvme-rr', 'kernel-nvme-rr', 'spdk-nvmf-rr', 'kernel-nvmf-rr']
# titles = ['kernel-nvme-rr','kernel-nvme-rw','kernel-nvmf-rr','kernel-nvmf-rw', 'spdk-nvme-rr', 'spdk-nvme-rw']
# titles = ['kernel-nvme-rr','spdk-nvme-rr']
titles = ['kernel-nvme-rr']
result = [list() for i in range(len(titles))]

x = [list() for i in range(len(titles))]
y = [list() for i in range(len(titles))]

figure, ax = plt.subplots(figsize=(12, 10))

file_names = []
for title in titles:
	names = getfilelist(title)
	file_names.append(names)

for i in range(len(file_names)):
	for j in range(len(file_names[i])):
		with open(file_names[i][j]) as file_obj:
			for content in file_obj:
				strlist = content.split(',')
				k = int(strlist[0])
				if len(result[i]) <= k:
					result[i].append(1)
				else:
					result[i][k] = result[i][k] + 1

for i in range(len(result)):
	for j in range(1, len(result[i])):
		x[i].append(j)
		y[i].append(result[i][j])


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

plt.ylim((500, 900))
plt.xlim((10000, 15000))

#The scale setting of the coordinate axis is inward (in)
ax.tick_params(axis='both',which='both', labelsize=16, direction='in')
plt.xlabel('Timing(ms)', font2)
plt.ylabel('IOPS', font2)

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
	plt.plot(x[i], y[i], '.', color='black')

plt.legend(titles, loc='upper left', prop=font1, edgecolor='white')

plt.rcParams['agg.path.chunksize'] = 10000
#plt.show()
plt.savefig('./t.png', dpi = 600)
