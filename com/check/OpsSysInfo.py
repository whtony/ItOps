import platform
import psutil


class OpsSysInfo(object):
    def __init__(self):
        pass

    def summary(self):
        print('操作系统类型：' + self.getOsInfo())
        print('系统已运行时间:' + str(self.getBootTime()))

    @classmethod
    def getOsInfo(cls):
        return platform.system()

    @classmethod
    def getBootTime(cls):
        return psutil.boot_time()

# info = OpsSysInfo()
# info.summary()