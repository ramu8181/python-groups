cisco@inserthostnamehere:/var/tmp$ more scapy7.py 
from scapy.all import *

class IGMP3(Packet):
    name = "IGMP3"
    fields_desc = [
        ByteField("type", 0x11),
        ByteField("mrtime", 20),
        XShortField("chksum", None),
        IPField("gaddr", "226.94.1.1"),
        IntField("others", 0x0)
    ]

    def post_build(self, p, pay):
        p += pay
        if self.chksum is None:
            ck = checksum(p)
            p = p[:2] + struct.pack('!H', ck) + p[4:]
        return p

bind_layers(IP, IGMP3, frag=0, proto=2)

p = IP(dst="192.168.25.9") / IGMP3()

for i in range ( 1, 1000):
    send(p, iface="ens2")
