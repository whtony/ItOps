import psutil


stats = psutil.net_if_stats()
io_counters = psutil.net_io_counters(pernic=True)
for nic, addrs in psutil.net_if_addrs().items():
    print("%s:" % (nic))
    if nic in stats:
        st = stats[nic]
        print("    stats          : ", end='')
        # print("speed=%sMB, duplex=%s, mtu=%s, up=%s" % (
        #     st.speed, duplex_map[st.duplex], st.mtu,
        #     "yes" if st.isup else "no"))
    if nic in io_counters:
        io = io_counters[nic]
        print("    incoming       : ", end='')
        # print("bytes=%s, pkts=%s, errs=%s, drops=%s" % (
        #     bytes2human(io.bytes_recv), io.packets_recv, io.errin,
        #     io.dropin))
        print("    outgoing       : ", end='')
        # print("bytes=%s, pkts=%s, errs=%s, drops=%s" % (
        #     bytes2human(io.bytes_sent), io.packets_sent, io.errout,
        #     io.dropout))
    for addr in addrs:
        # print(
        #     "    %-4s" %
        #     af_map.get(
        #         addr.family,
        #         addr.family),
        #     end="")
        print(" address   : %s" % addr.address)
        if addr.broadcast:
            print("         broadcast : %s" % addr.broadcast)
        if addr.netmask:
            print("         netmask   : %s" % addr.netmask)
        if addr.ptp:
            print("      p2p       : %s" % addr.ptp)
    print("")
