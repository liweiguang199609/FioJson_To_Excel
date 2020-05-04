#!/usr/bin/python
#-*-coding:utf-8-*-
import os
from excelTable import excelTable
from fileData import fileData

def run(dirname, target_name):
    rw_types = []
    bss = []
    numjobs = []
    depths = []
    for root, dirs, files in os.walk(dirname):
        # print(root)  # os.walk()所在目录
        # print(dirs)  # os.walk()所在目录的所有目录名
        # print(files)  # os.walk()所在目录的所有非目录文件名
        for file in files:
            if not file.startswith('r_') and not file.startswith('w_') and not file.startswith('rr_') and not file.startswith('rw_'):
                continue
            # print(file)
            tmp = file.split('_')
            rw_types.insert(0, tmp[0])
            bss.insert(0, int(tmp[1]))
            numjobs.insert(0, int(tmp[2]))
            depths.insert(0, int(tmp[3]))
    rw_types = list(set(rw_types))
    rw_types.sort()
    bss = list(set(bss))
    bss.sort()
    numjobs = list(set(numjobs))
    numjobs.sort()
    depths = list(set(depths))
    depths.sort()
    print(rw_types, bss, numjobs, depths)
    para = {'numjobs': numjobs,
            'depths': depths,
            'bss': bss,
            'rw_types' : rw_types}

    a = excelTable(dirname + '/' + target_name + '.xls')
    a.setFrame(para)
    for root, dirs, files in os.walk(dirname):
        for file in files:
            if not file.startswith('r_') and not file.startswith('w_') and not file.startswith('rr_') and not file.startswith('rw_'):
                continue
            print(file)
            tmp = file.split('_')
            rw_type = tmp[0]
            bs = int(tmp[1])
            numjob = int(tmp[2])
            depth = int(tmp[3])
            data = fileData(dirname + '/' + file)
            if rw_type == 'rr' or rw_type == 'r':
                if target_name == 'iops':
                    value = data.getReadIops()
                elif target_name == 'bw':
                    value = data.getReadBw()
                elif target_name == 'mean_latency':
                    value = data.getReadClatencyMean()
                else:
                    print("输入错误")
                    exit(0)
            else:
                if target_name == 'iops':
                    value = data.getWriteIops()
                elif target_name == 'bw':
                    value = data.getWriteBw()
                elif target_name == 'mean_latency':
                    value = data.getWriteClatencyMean()
                else:
                    print("输入错误")
                    exit(0)
            a.setValue(a.getPositionFromJson({'rw_type': rw_type, 'numjob': numjob, 'depth': depth, 'bs': bs}), value)
            data.f.close()

if __name__ == '__main__':
    # run('fio-bandwidth-iops-core', 'iops') # 第一个参数是fio json文件所在目录名，第二个参数是['iops', 'bw', 'mean_latency]之一
    # run('fio-bandwidth-iops-core', 'bw')
    # run('fio-bandwidth-iops-core', 'mean_latency')

    run('4CSD-test-data', 'iops')  # 第一个参数是fio json文件所在目录名，第二个参数是['iops', 'bw', 'mean_latency]之一
    run('4CSD-test-data', 'bw')
    run('4CSD-test-data', 'mean_latency')


