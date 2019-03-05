#!/bin/bash

echo "lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 493  bytes 41545 (41.5 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 493  bytes 41545 (41.5 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

foobar0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 192.168.123.1  netmask 255.255.255.0  broadcast 192.168.123.255
        ether 52:54:00:a3:b2:1c  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

wlp1s0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.172.56  netmask 255.255.255.0  broadcast 192.168.172.255
        inet6 fe80::67ae:269c:b42d:e23a  prefixlen 64  scopeid 0x20<link>
        ether de:ad:be:ef:23:23 txqueuelen 1000  (Ethernet)
        RX packets 3823  bytes 2254303 (2.2 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 2297  bytes 308681 (308.6 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0"
