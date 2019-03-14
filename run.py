import re
from com.check.OpsSysInfo import *
# from com.check.HardInfoWin import *


class run(object):

    def __init__(self):
        self.sysinfo = OpsSysInfo()
        # self.hardinfowin = HardInfoWin()

    def selectl1(self):
        count = 1
        while count == 1:
            print('系统概要:\n' + self.sysinfo.summary())
            print('____________________')
            print('服务器系统巡检类型：')
            print('——1、服务器硬件信息巡检')
            print('——2、操作系统信息巡检')
            print('——3、中间件系统巡检')
            print('——4、数据库系统巡检')
            print('——5、信息系统巡检')
            sel01 = input('请选择巡检类型(数字键1-5，0退出)：')

            while not re.findall('^[0-5]+$', sel01):
                # 限定只能输入数字
                sel01 = input("选择错误！请选择数字键0-5")
                print('选择6项：' + sel01)
            if str(sel01) == '1':
                if cls.sysinfo.getOsInfo() == 'Windows':
                    cls.sysinfowin.normcheck()
            if str(sel01) == '0':
                break


# wi = run()
# wi.selectl1()
info = OpsSysInfo()
info.summary()

