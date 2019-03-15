import platform
import psutil
from com.basis.LocalTimes import *


class OpsSysInfo(object):
    def __init__(self):
        self.localtimes = LocalTimes()

    def summary(self):
        print('操作系统类型：' + self.getOsInfo())
        print(int(self.getBootTime()))
        print('系统已运行时间:' + self.localtimes.timestamp10_to_strtime(self.getBootTime()))

    @classmethod
    def getOsInfo(cls):
        return platform.system()

    @classmethod
    def getBootTime(cls):
        return psutil.boot_time()

# info = OpsSysInfo()
# info.summary()