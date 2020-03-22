import os
import time
from RoundProgress import *

class CheckFrames(object):

    def Singlepath(self, path):
        self.filepath = path  # 坏帧路径
        Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        name = {}
        totalsize = 0
        total = 0
        Text2 = "\n非exr文件：\n"
        for filename in os.listdir(self.filepath):
            if filename.split('.')[-1] == 'exr':
                exrfile = self.filepath + '/' + filename  # exr文件路径
                for ch in exrfile:
                    if '\u4e00' <= ch <= '\u9fff':
                        error = "文件路径中有中文名称，请检查重新上传"
                        return error, "", {"工号": "", "检测人": "", "检测时间": Time, "检测路径": exrfile, "检测失败": "文件路径中有中文名称，请检查重新上传！"}, "", "", "", ""
                name[filename.split('.')[0]] = name.get(filename.split('.')[0], [])
                name[filename.split('.')[0]].append(int(filename.split('.')[-2]))  # 将坏帧名和序列放入字典，名字映射多个序列
                numlength = len(filename.split('.')[-2])  # 获取序列长度
                totalsize += os.path.getsize(exrfile)  # exr文件大小求和
                total += 1  # exr文件数
            else:
                Text2 += ('    ' + filename + '\n')

        lostframe = []
        lostframenum = 0
        lost = ''
        for n, num in name.items():
            a = set(range(num[0], num[-1] + 1))
            missing = sorted(list(a.difference(num)))  # 得到缺失序列
            if missing:
                for p in missing:
                    lostframenum += 1
                    lost += ("<p style = 'margin: 5px'>" + str(lostframenum) + '.' + n + '.' + str(p).zfill(numlength) + '.exr')  # 输出缺失帧
                    lostframe.append(n + '.' + str(p).zfill(numlength) + '.exr')
        if lostframenum != 0:
            Lost = lost
        else:
            Lost = "<p style = 'margin: 5px'>    暂未发现异常帧\n"
            lostframe.append("暂未发现异常帧")
        progress = 0
        badframe = []
        badframenum = 0
        bad = ''
        for filename in os.listdir(self.filepath):
            badfile = self.filepath + '/' + filename  # exr文件路径
            if filename.split('.')[-1] == 'exr':
                if os.path.getsize(badfile) < (totalsize / (total * 1000)):  # 小于平均大小的100倍输出坏帧
                    badframenum += 1
                    bad += ("<p style = 'margin: 5px'>" + str(badframenum) + '.' + filename)
                    badframe.append(filename)
                progress += 1
                persent = 100 * progress // total
                MyThread.p = persent  # 当前进度传入进度条
        if badframenum != 0:
            Bad = bad
        else:
            Bad = "<p style = 'margin: 5px'>    暂未发现异常帧\n"
            badframe.append("暂未发现异常帧")
        data = {"工号": "", "检测人": "", "检测时间": Time, "检测路径": self.filepath, "缺帧": lostframe, "坏帧": badframe}
        totalText = "检测的" + str(total) + "帧中，发现了" + str(lostframenum + badframenum) + "帧异常"
        return Lost, Bad, data, totalText, str(lostframenum), str(badframenum), str(total)

    def Multipath(self, path):
        self.filepath = path  # 坏帧路径
        Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        totalsize = 0
        total = 0
        lostframe = []
        lostframenum = 0
        lost = ''
        Text2 = "\n非exr文件：\n"
        for each in os.listdir(self.filepath):
            name = {}
            each_filepath = self.filepath + '/' + each  # 分类路径
            for filename in os.listdir(each_filepath):
                if filename.split('.')[-1] == 'exr':
                    exrfile = each_filepath + '/' + filename  # exr文件路径
                    for ch in exrfile:
                        if '\u4e00' <= ch <= '\u9fff':
                            error = "文件路径中有中文名称，请检查重新上传"
                            return error, "", {"工号": "", "检测人": "", "检测时间": Time, "检测路径": exrfile, "检测失败": "文件路径中有中文名称，请检查重新上传！"}, "", "", "", ""
                    name[filename.split('.')[0]] = name.get(filename.split('.')[0], [])
                    name[filename.split('.')[0]].append(int(filename.split('.')[-2]))  # 将坏帧名和序列放入字典，名字映射多个序列
                    numlength = len(filename.split('.')[-2])  # 获取序列长度
                    totalsize += os.path.getsize(exrfile)  # exr文件大小求和
                    total += 1  # exr文件数
                else:
                    Text2 += ('    ' + each_filepath + '/' + filename + '\n')
            for n, num in name.items():
                a = set(range(num[0], num[-1] + 1))
                missing = sorted(list(a.difference(num)))  # 得到缺失序列
                if missing:
                    for p in missing:
                        lostframenum += 1
                        lost += ("<p style = 'margin: 5px'>" + str(lostframenum) + '.' + each_filepath + '/' + n + '.' + str(p).zfill(numlength) + '.exr')  # 输出缺失帧
                        lostframe.append(each_filepath + '/' + n + '.' + str(p).zfill(numlength) + '.exr')
        if lostframenum != 0:
            Lost = lost
        else:
            Lost = "<p style = 'margin: 5px'>    暂未发现异常帧\n"
            lostframe.append("暂未发现异常帧")

        progress = 0
        badframe = []
        badframenum = 0
        bad = ''
        for each in os.listdir(self.filepath):
            each_filepath = self.filepath + '/' + each  # 分类路径
            for filename in os.listdir(each_filepath):
                badfile = each_filepath + '/' + filename  # exr文件路径
                if filename.split('.')[-1] == 'exr':
                    if os.path.getsize(badfile) < (totalsize / (total * 1000)):  # 小于平均大小的100倍输出坏帧
                        badframenum += 1
                        bad += ("<p style = 'margin: 5px'>" + str(badframenum) + '.' + badfile)
                        badframe.append(badfile)
                    progress += 1
                    persent = 100 * progress // total
                    MyThread.p = persent  # 当前进度传入进度条
        if badframenum != 0:
            Bad = bad
        else:
            Bad = "<p style = 'margin: 5px'>    暂未发现异常帧\n"
            badframe.append("暂未发现异常帧")
        data = {"工号": "", "检测人": "", "检测时间": Time, "检测路径": self.filepath, "缺帧": lostframe, "坏帧": badframe}
        totalText = "检测的" + str(total) + "帧中，发现了" + str(lostframenum + badframenum) + "帧异常"
        return Lost.replace('/', '\\'), Bad.replace('/', '\\'), data, totalText, str(lostframenum), str(badframenum), str(total)