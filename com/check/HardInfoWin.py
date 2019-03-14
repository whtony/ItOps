import wmi


class HardInfoWin(object):
    c = wmi.WMI()

    def __init__(self):
        self.cpu = HardInfoWin.getCPU()
        self.main = HardInfoWin.getMain_board()
        self.bios = HardInfoWin.getBIOS()
        self.disk = HardInfoWin.getDisk()
        self.memos = HardInfoWin.getPhysicalMemory()
        self.macs = HardInfoWin.getMacAddress()

    # 处理器
    @classmethod
    def getCPU(cls):
        tmpdict = {}
        tmpdict["CpuCores"] = 0
        for cpu in cls.c.Win32_Processor():
            tmpdict["cpuid"] = cpu.ProcessorId.strip()
            tmpdict["CpuType"] = cpu.Name
            tmpdict['systemName'] = cpu.SystemName
            try:
                tmpdict["CpuCores"] = cpu.NumberOfCores
            except BaseException:
                tmpdict["CpuCores"] += 1
            tmpdict["CpuClock"] = cpu.MaxClockSpeed
            tmpdict['DataWidth'] = cpu.DataWidth
        return tmpdict

    # 主板
    @classmethod
    def getMain_board(cls):
        boards = []
        # print len(c.Win32_BaseBoard()):
        for board_id in cls.c.Win32_BaseBoard():
            tmpmsg = {}
            # 主板UUID,有的主板这部分信息取到为空值，ffffff-ffffff这样的
            tmpmsg['UUID'] = board_id.qualifiers['UUID'][1:-1]
            tmpmsg['SerialNumber'] = board_id.SerialNumber  # 主板序列号
            tmpmsg['Manufacturer'] = board_id.Manufacturer  # 主板生产品牌厂家
            tmpmsg['Product'] = board_id.Product  # 主板型号
            boards.append(tmpmsg)
        return boards

    # BIOS
    @classmethod
    def getBIOS(cls):
        bioss = []
        for bios_id in cls.c.Win32_BIOS():
            tmpmsg = {}
            tmpmsg['BiosCharacteristics'] = bios_id.BiosCharacteristics  # BIOS特征码
            tmpmsg['version'] = bios_id.Version  # BIOS版本
            tmpmsg['Manufacturer'] = bios_id.Manufacturer.strip()  # BIOS固件生产厂家
            tmpmsg['ReleaseDate'] = bios_id.ReleaseDate  # BIOS释放日期
            tmpmsg['SMBIOSBIOSVersion'] = bios_id.SMBIOSBIOSVersion  # 系统管理规范版本
            bioss.append(tmpmsg)
        return bioss

    # 硬盘
    @classmethod
    def getDisk(cls):
        disks = []
        for disk in cls.c.Win32_DiskDrive():
            # print disk.__dict__
            tmpmsg = {}
            tmpmsg['SerialNumber'] = disk.SerialNumber.strip()
            tmpmsg['DeviceID'] = disk.DeviceID
            tmpmsg['Caption'] = disk.Caption
            tmpmsg['Size'] = disk.Size
            tmpmsg['UUID'] = disk.qualifiers['UUID'][1:-1]
            disks.append(tmpmsg)
        return disks

    # 内存
    @classmethod
    def getPhysicalMemory(cls):
        memorys = []
        for mem in cls.c.Win32_PhysicalMemory():
            tmpmsg = {}
            tmpmsg['UUID'] = mem.qualifiers['UUID'][1:-1]
            tmpmsg['BankLabel'] = mem.BankLabel
            tmpmsg['SerialNumber'] = mem.SerialNumber.strip()
            tmpmsg['ConfiguredClockSpeed'] = mem.ConfiguredClockSpeed
            tmpmsg['Capacity'] = mem.Capacity
            tmpmsg['ConfiguredVoltage'] = mem.ConfiguredVoltage
            memorys.append(tmpmsg)
        return memorys

    # 电池信息，只有笔记本才会有电池选项
    @classmethod
    def getBattery(cls):
        isBatterys = False
        for b in c.Win32_Battery():
            isBatterys = True
        # return isBatterys

    # 网卡mac地址：
    @classmethod
    def getMacAddress(cls):
        macs = []
        for n in cls.c.Win32_NetworkAdapter():
            mactmp = n.MACAddress
            if mactmp and len(mactmp.strip()) > 5:
                tmpmsg = {}
                tmpmsg['MACAddress'] = n.MACAddress
                tmpmsg['Name'] = n.Name
                tmpmsg['DeviceID'] = n.DeviceID
                tmpmsg['AdapterType'] = n.AdapterType
                tmpmsg['Speed'] = n.Speed
                macs.append(tmpmsg)
        # print(macs)
        return macs

    def normcheck(self):
        print('==>开始服务器硬件信息巡检==>')
        # print(self.cpu)
        print('__________CPU__________')
        print('CpuCores:' + str(self.cpu['CpuCores']))
        print('CpuType:' + str(self.cpu['CpuType']))
        print('systemName:' + str(self.cpu['systemName']))
        # print(self.main)
        print('__________Main_board__________')
        print('Manufacturer:' + self.main[0]['Manufacturer'])
        print('SerialNumber:' + self.main[0]['SerialNumber'])
        print('Product:' + self.main[0]['Product'])
        # print(self.bios)
        print('__________BIOS__________')
        print('version:' + self.bios[0]['version'])
        print('Manufacturer:' + self.bios[0]['Manufacturer'])
        print('ReleaseDate:' + self.bios[0]['ReleaseDate'])
        print('SMBIOSBIOSVersion:' + self.bios[0]['SMBIOSBIOSVersion'])
        print('__________Disks__________')
        # print(self.disk)
        disktag = 0
        for d in self.disk:
                disktag = disktag + 1
                print('_______________Disk' + str(disktag) + '_____')
                print('Caption:' + d['Caption'])
                size = round(int(d['Size']) / 1024 / 1024 / 1024, 2)
                print('Size:' + str(size) + 'G')
                print('SerialNumber:' + d['SerialNumber'])
                print('DeviceID:' + d['DeviceID'])
                print('UUID:' + d['UUID'])
        print('__________Memos__________')
        # print(self.memos)
        memotag = 0
        for m in self.memos:
            # print(m)
            memotag = memotag + 1
            print('_______________Memo' + str(memotag) + '_____')
            print('BankLabel:' + m['BankLabel'])
            print('SerialNumber:' + m['SerialNumber'])
            print('ConfiguredClockSpeed:' + str(m['ConfiguredClockSpeed']))
            size = round(int(m['Capacity']) / 1024 / 1024 / 1024, 0)
            print('Capacity:' + str(size) + 'G')
            print('UUID:' + m['UUID'])
        print('__________MacAddress__________')
        # print(self.macs)
        mactag = 0
        for mac in self.macs:
            mactag = mactag + 1
            print('_______________MacAddress' + str(mactag) + '_____')
            print('DeviceID:' + mac['DeviceID'])
            print('AdapterType:' + mac['AdapterType'])
            print('Name:' + mac['Name'])
            # print(type(m['Speed']).__name__)
            if type(mac['Speed']).__name__ == 'str':
                speed = round(int(mac['Speed']) / 1024 / 1024, 2)
                print('Speed:' + str(speed) + 'M')
            else:
                print('Speed:None')
            print('MACAddress:' + mac['MACAddress'])
        print('<==结束服务器硬件信息巡检<==')
        # sysinfo.print(printBattery())


# info = HardInfoWin()
# info.normcheck()
