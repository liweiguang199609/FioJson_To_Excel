#!/usr/bin/python
#-*-coding:utf-8-*-
import json
class fileData (object):
    def __init__(self,fileName):
        self.f = open(fileName,"r")
        self.data = json.loads(self.f.read())

    def getReadBw(self):
        return self.data['jobs'][0]['read']['bw']

    def getWriteBw(self):
        return self.data['jobs'][0]['write']['bw']

    def getReadClatencyMean(self):
        return self.data['jobs'][0]['read']['clat_ns']['mean']

    def getWriteClatencyMean(self):
        return self.data['jobs'][0]['write']['clat_ns']['mean']

    def getReadClatency95(self):
        return self.data['jobs'][0]['read']['clat_ns']['percentile']['95.000000']

    def getWriteClatency95(self):
        return self.data['jobs'][0]['write']['clat_ns']['percentile']['95.000000']

    def getReadClatency9999(self):
        return self.data['jobs'][0]['read']['clat_ns']['percentile']['99.990000']

    def getWriteClatency9999(self):
        return self.data['jobs'][0]['write']['clat_ns']['percentile']['99.990000']

    def getReadIops(self):
        return self.data['jobs'][0]['read']['iops']

    def getWriteIops(self):
        return self.data['jobs'][0]['write']['iops']

    def close(self):
        self.f.close()

if __name__ == '__main__':
    a=fileData("r_1024_4_32_1")
    print(a.getReadBw())
    print(a.getWriteBw())
    print(a.getReadClatencyMean())
    print(a.getWriteClatencyMean())
    print(a.getReadClatency95())
    print(a.getWriteClatency95())
    print(a.getReadClatency9999())
    print(a.getWriteClatency9999())
    print(a.getReadIops())
    print(a.getWriteIops())


