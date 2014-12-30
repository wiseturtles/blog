Title: WIFI Hotspot Setup On Ubuntu 12.04
Date: 2014-12-30
Category: Ubuntu
Tags: Ubuntu
Slug: wifi-hotspot-setup-on-ubuntu
Authors: Zhang Wanming
Summary: Ubuntu笔记本上配置hotspot

为了Ubuntu笔记本方便对Android手机上的Apps做抓包。

参考：http://thenewbieblog.wordpress.com/2012/05/01/wifi-hotspot-setup-on-ubuntu/

查看Ubuntu系统配置
===================

查看无线网卡硬件信息
---------------------

    :::bash

    $ sudo lspci | grep -i network
    03:00.0 Network controller: Intel Corporation Wireless 7260 (rev 6b)


查看无线网卡驱动信息
---------------------

    :::bash

    $ lsmod

查看无线网卡设备名称
---------------------

    :::bash

    $ iwconfig
    wlan0     IEEE 802.11bgn  Mode:Master  Tx-Power=16 dBm   
              Retry  long limit:7   RTS thr:off   Fragment thr:off
              Power Management:on


安装需要的软件
---------------

    :::bash

    $ sudo apt-get install dhcp3-server hostapd

修改/etc/hostapd/hostapd.conf
------------------------------

    :::bash

    $ cat /etc/hostapd/hostapd.conf
    interface=wlan0
    driver=nl80211
    ssid=your_hotspot_name
    channel=1
    hw_mode=g
    auth_algs=1
    wpa=3
    wpa_passphrase=your-password
    wpa_key_mgmt=WPA-PSK
    wpa_pairwise=TKIP CCMP
    rsn_pairwise=CCMP


修改/etc/default/isc-dhcp-server
---------------------------------

    :::bash

    $ grep INTERFACES /etc/default/isc-dhcp-server
    INTERFACES="wlan0"


修改/etc/dhcp/dhcpd.conf
-------------------------

    :::bash

    配置文件: /etc/dhcp/dhcpd.conf
    Make sure the follow lines are Commented out ( put a hash “#”  sign at the beginning of the line ) the following lines:
    # option definitions common to all supported networks…
    #option domain-name “example.org”;
    #option domain-name-servers ns1.example.org, ns2.example.org;
    #default-lease-time 600;
    #max-lease-time 7200;

    Add the following lines to the file (copy and paste)
    subnet 10.10.0.0 netmask 255.255.255.0 {
            range 10.10.0.2 10.10.0.16;
            option domain-name-servers 8.8.4.4, 208.67.222.222;
            option routers 10.10.0.1;
    }

    (Note: the only other line in this whole config file that is uncommented is :

    ddns-update-style none;)


修改/etc/default/hostapd
-------------------------

    :::bash

    $ grep -E 'RUN_DAEMON|DAEMON_CONF|DAEMON_OPTS' /etc/default/hostapd | grep -Ev '^#'
    RUN_DAEMON="yes"
    DAEMON_CONF="/etc/hostapd/hostapd.conf"
    DAEMON_OPTS="-dd"


修改/etc/network/interfaces
----------------------------

    :::bash

    $ cat /etc/network/interfaces
    auto lo
    iface lo inet loopback
    auto wlan0
    iface wlan0 inet static
        address 10.10.0.1
        netmask 255.255.255.0


修改/etc/sysctl.conf
---------------------

    :::bash
    $ grep net.ipv4.ip_forward /etc/sysctl.conf 
    net.ipv4.ip_forward=1


修改/etc/rc.local
-------------------

    :::bash
    编辑 /etc/rc.local, 在 "exit 0" 前添加下一行
    iptables -t nat -A POSTROUTING -s 10.10.0.0/16 -o ppp0 -j MASQUERADE


重启电脑
---------

重启电脑，手机测试是否可以连接.
