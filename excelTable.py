#!/usr/bin/python
# -*-coding:utf-8-*-
import xlwt
import xlrd
import os
from fileData import fileData

class excelTable(object):
    def __init__(self, excelFileName):
        if os.path.exists(excelFileName):
            os.remove(excelFileName)
        self.excelFileName = excelFileName
        self.workbook = xlwt.Workbook(encoding='utf8')
        self.worksheet = self.workbook.add_sheet(u'sheet1')
        self.style = xlwt.XFStyle()  # 创建一个样式对象，初始化样式
        al = xlwt.Alignment()
        al.horz = 0x02  # 设置水平居中
        al.vert = 0x01  # 设置垂直居中
        self.style.alignment = al
        self.workbook.save(excelFileName)
        self.numjobs = 0
        self.depths = 0
        self.bss = 0
        self.iops = 0
        self.rw_types = 0

    def setFrame(self, para):
        for key in para:
            exec("self." + key + " = " + str(para[key]))
        numjob_length = len(self.numjobs)
        depth_length = len(self.depths)
        bs_length = len(self.bss)

        for rw_index in range(len(self.rw_types)):
            rw_position = {'x': rw_index * numjob_length * ( 2 + bs_length ) + 1, 'y': 0} # x towords down ; y towords the right
            self.worksheet.write_merge(rw_position['x'], rw_position['x'] + numjob_length * ( 2 + bs_length ) - 1, rw_position['y'],rw_position['y'], self.rw_types[rw_index], self.style)
            for numjob_index in range(len(self.numjobs)):
                numjobs_position = {'x': rw_position['x'] + numjob_index * ( 2 + bs_length ), 'y': rw_position['y'] + 1}
                depths_position = {'x': numjobs_position['x'], 'y': numjobs_position['y'] + 4}
                bss_position = {'x': numjobs_position['x'] + 2, 'y': numjobs_position['y'] + 2}
                self.worksheet.write_merge(numjobs_position['x'],numjobs_position['x'] + bs_length + 1,numjobs_position['y'],numjobs_position['y'],"numjobs=" + str(self.numjobs[numjob_index]), self.style)
                self.worksheet.write_merge(depths_position['x'],depths_position['x'],depths_position['y'],depths_position['y'] + depth_length - 1,"depths", self.style)
                self.worksheet.write_merge(bss_position['x'],bss_position['x'] + bs_length - 1,bss_position['y'],bss_position['y'],"bs", self.style)

                for i in range(len(self.depths)):
                    self.worksheet.write(depths_position['x'] + 1, depths_position['y'] + i, self.depths[i], self.style)
                for i in range(len(self.bss)):
                    self.worksheet.write(bss_position['x'] + i, bss_position['y'] + 1, self.bss[i], self.style)
        self.workbook.save(self.excelFileName)

    def getPositionFromJson(self, json):
        rw_type = json['rw_type'] # 取出rw_types类型
        numjob = json['numjob']
        depth = json['depth']
        bs = json['bs']
        if numjob not in self.numjobs:
            return -1
        if depth not in self.depths:
            return -1
        if bs not in self.bss:
            return -1
        rw_type_index = -1
        numjob_index = -1
        depth_index = -1
        bs_index = -1
        for rw_type_index in range(len(self.rw_types)):
            if self.rw_types[rw_type_index] == rw_type:
                break
        for numjob_index in range(len(self.numjobs)):
            if self.numjobs[numjob_index] == numjob:
                break
        numjob_length = len(self.numjobs)
        depth_length = len(self.depths)
        bs_length = len(self.bss)
        rw_types_position = {'x': rw_type_index * numjob_length * (2 + bs_length) + 1, 'y': 0}
        numjob_position = {'x': rw_types_position['x'] + numjob_index * (2 + bs_length), 'y': rw_types_position['y'] + 1}
        depth_position = {'x': numjob_position['x'], 'y': numjob_position['y'] + 4}
        bs_position = {'x': numjob_position['x'] + 2, 'y': numjob_position['y'] + 2}

        ExcelFile = xlrd.open_workbook(self.excelFileName)
        table = ExcelFile.sheets()[0]
        for i in range(len(self.depths)):
            if table.cell(depth_position['x'] + 1,depth_position['y'] + i).value == depth:
                depth_index = i
                break
        for i in range(len(self.depths)):
            if table.cell(bs_position['x'] + i,bs_position['y'] + 1).value == bs:
                bs_index = i
                break
        x = depth_position['x'] + 2 + bs_index
        y = depth_position['y'] + depth_index
        position = {}
        position['x'] = x
        position['y'] = y
        return position

    def setValue(self, position, data):
        self.worksheet.write(position['x'], position['y'], data, self.style)
        self.workbook.save(self.excelFileName)

    def close(self):
        return 0

    def testsetPositionAndValue(self):
        numjobs = (1, 2, 4)
        depths = (1, 32, 64)
        bss = (4, 1024, 2048)
        a.setFrame(numjobs, depths, bss)
        a.setValue(a.getPositionFromJson({'rw_types':'rr', 'numjob': 4, 'depth': 32, 'bs': 4}), 'lwg')

# excel table operation test
if __name__ == '__main__':
    data = fileData('rw_8_2_1_1')
    bw = data.getWriteBw()
    a = excelTable("2.xls")
    para = {'numjobs':(1, 2, 4, 8),
            'depths':(1, 32, 64),
            'bss':(4, 8, 1024, 2048),
            'rw_types':('r', 'rr', 'rw', 'w')}   # rw_tpyes排序后是这个顺序
    a.setFrame(para)
    a.setValue(a.getPositionFromJson({'rw_type': 'rw', 'numjob': 2, 'depth': 1, 'bs': 8}), bw)
