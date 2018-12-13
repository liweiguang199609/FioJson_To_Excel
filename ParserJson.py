#!/usr/bin/python
#-*-coding:utf-8-*-
import os
from excelTable import excelTable
from fileData import fileData

def run_latency(dirname):
    target = 'latency'
    bss = []
    numjobs = []
    depths = []
    iopss = []
    for root, dirs, files in os.walk(dirname):
        # print(root)  # os.walk()所在目录
        # print(dirs)  # os.walk()所在目录的所有目录名
        # print(files)  # os.walk()所在目录的所有非目录文件名
        for file in files:
            if not file.startswith('r_') and not file.startswith('w_'):
                continue
            # print(file)
            tmp = file.split('_')
            bss.insert(0, int(tmp[1]))
            numjobs.insert(0, int(tmp[2]))
            depths.insert(0, int(tmp[3]))
            iopss.insert(0, int(tmp[4]))
    bss = list(set(bss))
    bss.sort()
    numjobs = list(set(numjobs))
    numjobs.sort()
    depths = list(set(depths))
    depths.sort()
    iopss = list(set(iopss))
    iopss.sort()
    print(bss, numjobs, depths)

    a = excelTable(dirname + '/' + target + '.xls')
    a.setFrame(numjobs, depths, bss, iopss)
    for root, dirs, files in os.walk(dirname):
        for file in files:
            rw = -1
            if file.startswith('r_'):
                rw = 0
            elif file.startswith('w_'):
                rw = 1
            else:
                continue
            print(file)
            tmp = file.split('_')
            bs = int(tmp[1])
            numjob = int(tmp[2])
            depth = int(tmp[3])
            iops = int(tmp[4])
            data = fileData(dirname + '/' + file)
            if rw == 0:
                latency_mean = data.getReadClatencyMean()
                latency_95 = data.getReadClatency95()
                latency_9999 = data.getReadClatency9999()
            else:
                latency_mean = data.getWriteClatencyMean()
                latency_95 = data.getWriteClatency95()
                latency_9999 = data.getWriteClatency9999()
            a.setValue(a.getPositionFromJson({'rw': rw, 'numjob': numjob, 'depth': depth, 'bs': bs, 'horizontal': iops, 'vertical':'mean'}), latency_mean)
            a.setValue(a.getPositionFromJson({'rw': rw, 'numjob': numjob, 'depth': depth, 'bs': bs, 'horizontal': iops, 'vertical': '95.00%'}),latency_95)
            a.setValue(a.getPositionFromJson({'rw': rw, 'numjob': numjob, 'depth': depth, 'bs': bs, 'horizontal': iops, 'vertical': '99.99%'}),latency_9999)
            data.f.close()

if __name__ == '__main__':
    run_latency('fio-latency-32')


