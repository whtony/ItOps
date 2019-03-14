import psutil
from com.basis.LocalTimes import LocalTimes
# from __future__ import print_function
import socket
import platform


class HostInfo(object):
    af_map = {
        socket.AF_INET: 'IPv4',
        socket.AF_INET6: 'IPv6',
        psutil.AF_LINK: 'MAC',
    }
    duplex_map = {
        psutil.NIC_DUPLEX_FULL: "full",
        psutil.NIC_DUPLEX_HALF: "half",
        psutil.NIC_DUPLEX_UNKNOWN: "?",
    }

    def __init__(self):
        print(self)

    def cpuInfo(self):
        cpucount01 = psutil.cpu_count()
        cpucount02 = psutil.cpu_count(logical=False)
        print('CPU逻辑数量：' + str(cpucount01))
        print('CPU物理数量：' + str(cpucount02))

    def bootTimes(self):
        bootimes = psutil.boot_time()
        # print('系统启动时间：' + str(bootimes))

        local = LocalTimes()
        print('系统启动时间：' + local.timestamp10_to_strtime(bootimes))
        # print('系统启动时间：' + datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"))

    def bytes2human(self, n):
        """
        >>> bytes2human(10000)
        '9.8 K'
        >>> bytes2human(100001221)
        '95.4 M'
        """
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i + 1) * 10
        for s in reversed(symbols):
            if n >= prefix[s]:
                value = float(n) / prefix[s]
                return '%.2f%s' % (value, s)
        return '%.2fB' % (n)

    def ipAddr(self):
        stats = psutil.net_if_stats()
        io_counters = psutil.net_io_counters(pernic=True)
        for nic, addrs in psutil.net_if_addrs().items():
            print("%s:" % (nic))
            if nic in stats:
                st = stats[nic]
                print("    stats          : ", end='')
                print("speed=%sMB, duplex=%s, mtu=%s, up=%s" % (
                    st.speed, self.duplex_map[st.duplex], st.mtu,
                    "yes" if st.isup else "no"))
            if nic in io_counters:
                io = io_counters[nic]
                print("    incoming       : ", end='')
                print("bytes=%s, pkts=%s, errs=%s, drops=%s" % (
                    self.bytes2human(io.bytes_recv), io.packets_recv, io.errin,
                    io.dropin))
                print("    outgoing       : ", end='')
                print(
                    "bytes=%s, pkts=%s, errs=%s, drops=%s" %
                    (self.bytes2human(
                        io.bytes_sent),
                        io.packets_sent,
                        io.errout,
                        io.dropout))
            for addr in addrs:
                print(
                    "    %-4s" %
                    self.af_map.get(
                        addr.family,
                        addr.family),
                    end="")
                print(" address   : %s" % addr.address)
                if addr.broadcast:
                    print("         broadcast : %s" % addr.broadcast)
                if addr.netmask:
                    print("         netmask   : %s" % addr.netmask)
                if addr.ptp:
                    print("      p2p       : %s" % addr.ptp)
            print("")

    def user(self):
        print(psutil.users())

    def ifcfg(self):
        print(psutil.net_if_stats())
        print(psutil.net_io_counters(pernic=True))
        print(psutil.net_if_addrs().items())

    def get_os_info(self):
        print('------------------------------')
        # print("system version---- %s" % ", ".join(sys.version.split("\n")))
        print(
            '操作系统信息：' +
            platform.system() +
            platform.version() +
            '_' +
            platform.machine())
        print('硬件信息：' + platform.processor())

    def get_cpu_linux_info(self):
        # linux cpu info
        processor_cnt = 0
        cpu_model = ""
        f_cpu_info = open("/proc/cpuinfo")
        try:
            for line in f_cpu_info:
                if (line.find("processor") == 0):
                    processor_cnt += 1
                elif (line.find("model name") == 0):
                    if (cpu_model == ""):
                        cpu_model = line.split(":")[1].strip()

            print("cpu counts: %s, cpu model: %s" % (processor_cnt, cpu_model))
        finally:
            f_cpu_info.close()

    def get_cpu_win_info(self):
        print('')


# host = HostInfo()
# host.cpuInfo()
# host.bootTimes()
# host.ipAddr()
# host.user()
# host.ifcfg()
# host.get_os_info()
# host.get_cpu_win_info()
