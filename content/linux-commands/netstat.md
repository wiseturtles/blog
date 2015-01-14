Title: netstat
Date: 2015-01-14 10:35
Tags: linux, command, netstat
Slug: linux-netstat
Author: crazygit
Summary: the usage of netstat


本文参考：

* <http://www.cnblogs.com/ggjucheng/archive/2012/01/08/2316661.html>
* <http://www.binarytides.com/linux-netstat-command-examples/>

## 作用

Netstat 命令用于显示各种网络相关信息，如网络连接，路由表，接口状态
(Interface Statistics)，masquerade 连接，多播成员 (Multicast Memberships) 等
等。

## 输出信息含义

执行netstat后，其输出结果为

<pre>
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address Foreign Address State
tcp 0 2 210.34.6.89:telnet 210.34.6.96:2873 ESTABLISHED
tcp 296 0 210.34.6.89:1165 210.34.6.84:netbios-ssn ESTABLISHED
tcp 0 0 localhost.localdom:9001 localhost.localdom:1162 ESTABLISHED
tcp 0 0 localhost.localdom:1162 localhost.localdom:9001 ESTABLISHED
tcp 0 80 210.34.6.89:1161 210.34.6.10:netbios-ssn CLOSE

Active UNIX domain sockets (w/o servers)
Proto RefCnt Flags Type State I-Node Path
unix 1 [ ] STREAM CONNECTED 16178 @000000dd
unix 1 [ ] STREAM CONNECTED 16176 @000000dc
unix 9 [ ] DGRAM 5292 /dev/log
unix 1 [ ] STREAM CONNECTED 16182 @000000df
</pre>

从整体上看，netstat的输出结果可以分为两个部分：

一个是Active Internet connections，称为有源TCP连接，其中"Recv-Q"和"Send-Q"指%0A的是接收队列和发送队列。这些数字一般都应该是0。如果不是则表示软件包正在队列中堆积。这种情况只能在非常少的情况见到。

另一个是Active UNIX domain sockets，称为有源Unix域套接口(和网络套接字一样，但是只能用于本机通信，性能可以提高一倍)。
Proto显示连接使用的协议,RefCnt表示连接到本套接口上的进程号,Types显示套接口的类型,State显示套接口当前的状态,Path表示连接到套接口的其它进程使用的路径名。

## 常见参数

* -a (all)显示所有监听和未监听的连接
* -t (tcp)仅显示tcp相关选项
* -u (udp)仅显示udp相关选项
* -n 拒绝显示别名，能显示数字的全部转化成数字。
* -l 仅列出有在 Listen (监听) 的服務状态
*
* -p 显示建立相关链接的程序名
* -r 显示路由信息，路由表
* -e 显示扩展信息，例如uid等
* -s 按各个协议进行统计
* -c 每隔一个固定时间，执行该netstat命令。

**提示**：LISTEN和LISTENING的状态只有用-a或者-l才能看到

## 实用命令实例

    :::bash
    # 列出所有连接（包括监听和未监听的)
    $ netstat -a

    # 列出所有tcp连接
    $ netstat -at

    # 列出所有udp连接
    $ netstat -au

    # 默认情况下，netstat命令会做一个reverse dns lookup去查找连接的ip
    # 对应的主机名，这会降低输出速度，如果不需要，可以使用-n
    # 在netstat输出中不显示主机，端口和用户名(host, port or user)
    $ netstat -an

    # 列出所有处于监听状态的
    # -l选项不要与-a同时使用，不然也会列出未监听状态的连接
    $ netstat -l

    # 列出所有监听状态的tcp连击
    $ netstat -lt

    # 列出所有监听状态的udp连击
    $ netstat -lu

    # 列出所有的unix连接
    $ netstat -lx

    # 在netstat输出中显示PID和进程名称(-p),用户名(-e)
    # -p使用需要root权限,不然无法获取PID
    $ sudo netstat -ltpe
    Proto Recv-Q Send-Q Local Address           Foreign Address         State       User       Inode       PID/Program name
    tcp        0      0 localhost:5037          *:*                     LISTEN      linliang   4530492     11684/adb
    tcp        0      0 localhost:63342         *:*                     LISTEN      linliang   10952269    6663/java
    tcp        0      0 localhost:9200          *:*                     LISTEN      linliang   10361577    12461/ssh
    tcp        0      0 *:http                  *:*                     LISTEN      root       12810       1344/nginx
    tcp        0      0 localhost:domain        *:*                     LISTEN      root       683         1481/dnsmasq

    # 上面的命令总如果使用-n,将会显示用户UID，而不是用户名

    # 列出所有的网络统计信息
    $ netstat -s
    Ip:
    14989101 total packets received
    0 forwarded
    0 incoming packets discarded
    14986294 incoming packets delivered
    11643610 requests sent out
    Icmp:
        6034 ICMP messages received
        71 input ICMP message failed.
        ICMP input histogram:
            destination unreachable: 5774
            timeout in transit: 106
            echo replies: 154
        6882 ICMP messages sent
        0 ICMP messages failed
        ICMP output histogram:
    ....

    # 显示TCP或UDP连接的统计信息
    $ netstat -st
    $ netstat -su

    # 显示kernel的路由信息(-r)
    $ netstat -rn
    Kernel IP routing table
    Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
    0.0.0.0         172.26.50.1     0.0.0.0         UG        0 0          0 eth1
    169.254.0.0     0.0.0.0         255.255.0.0     U         0 0          0 eth1
    172.26.50.0     0.0.0.0         255.255.255.0   U         0 0          0 eth1
    192.168.56.0    0.0.0.0         255.255.255.0   U         0 0          0 vboxnet0

    # 打印网络接口(-i)
    $ netstat -i
    Kernel Interface table
    Iface   MTU Met   RX-OK RX-ERR RX-DRP RX-OVR    TX-OK TX-ERR TX-DRP TX-OVR Flg
    eth1       1500 0  10650979      0      0 0      10656895      0      0      0 BMRU
    lo        65536 0   5095802      0      0 0       5095802      0      0      0 LRU
    vboxnet0   1500 0         0      0      0 0          1505      0      0      0 BMRU

    # 上面的输出比较原始，为了获取友好输出，可以加上(-e)
    # 达到与ifconfig命令类似的效果
    $ netstat -ie
    Kernel Interface table
    eth1      Link encap:Ethernet  HWaddr 44:39:c4:8d:d9:64
            inet addr:172.26.50.13  Bcast:172.26.50.255  Mask:255.255.255.0
            inet6 addr: fe80::4639:c4ff:fe8d:d964/64 Scope:Link
            UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
            RX packets:10651112 errors:0 dropped:0 overruns:0 frame:0
            TX packets:10656940 errors:0 dropped:0 overruns:0 carrier:0
            collisions:0 txqueuelen:1000
            RX bytes:6607723134 (6.6 GB)  TX bytes:10396843122 (10.3 GB)
            Interrupt:20 Memory:f7c00000-f7c20000

    lo        Link encap:Local Loopback
            inet addr:127.0.0.1  Mask:255.0.0.0
            inet6 addr: ::1/128 Scope:Host
            UP LOOPBACK RUNNING  MTU:65536  Metric:1
            RX packets:5095811 errors:0 dropped:0 overruns:0 frame:0
            TX packets:5095811 errors:0 dropped:0 overruns:0 carrier:0
            collisions:0 txqueuelen:0
            RX bytes:2717552755 (2.7 GB)  TX bytes:2717552755 (2.7 GB)

    vboxnet0  Link encap:Ethernet  HWaddr 0a:00:27:00:00:00
            inet addr:192.168.56.1  Bcast:192.168.56.255  Mask:255.255.255.0
            inet6 addr: fe80::800:27ff:fe00:0/64 Scope:Link
            UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
            RX packets:0 errors:0 dropped:0 overruns:0 frame:0
            TX packets:1505 errors:0 dropped:0 overruns:0 carrier:0
            collisions:0 txqueuelen:1000
            RX bytes:0 (0.0 B)  TX bytes:130893 (130.8 KB)
