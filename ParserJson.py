#!/usr/bin/python
#-*-coding:utf-8-*-
import os
from excelTable import excelTable
from fileData import fileData

def run_bw(dirname):
    target = 'bw'
    bss = []
    numjobs = []
    depths = []
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
    bss = list(set(bss))
    bss.sort()
    numjobs = list(set(numjobs))
    numjobs.sort()
    depths = list(set(depths))
    depths.sort()
    print(bss, numjobs, depths)

    a = excelTable(dirname + '/' + target + '.xls')
    a.setFrame(numjobs, depths, bss)
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
            data = fileData(dirname + '/' + file)
            if rw == 0:
                bw = data.getReadBw()
            else:
                bw = data.getWriteBw()
            a.setValue(a.getPositionFromJson({'rw': rw, 'numjob': numjob, 'depth': depth, 'bs': bs}), bw)
            data.f.close()

def run_iops(dirname):
    target = 'iops'
    bss = []
    numjobs = []
    depths = []
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
    bss = list(set(bss))
    bss.sort()
    numjobs = list(set(numjobs))
    numjobs.sort()
    depths = list(set(depths))
    depths.sort()
    print(bss, numjobs, depths)

    a = excelTable(dirname + '/' + target + '.xls')
    a.setFrame(numjobs, depths, bss)
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
            data = fileData(dirname + '/' + file)
            if rw == 0:
                iops = data.getReadIops()
            else:
                iops = data.getWriteIops()
            a.setValue(a.getPositionFromJson({'rw': rw, 'numjob': numjob, 'depth': depth, 'bs': bs}), iops)
            data.f.close()

if __name__ == '__main__':
    run_bw('fio-bandwidth-iops-core')
    run_iops('fio-bandwidth-iops-core')


