Title:  iptables配置
Date: 2015-09-23 16:40
Tags: iptables
Slug: iptables-on-debian-centos
Author: ox0spy
Summary: 在Debian、Centos上配置iptables

最近使用阿里云ECS，发现既然没有提供安全组，能让小白用户方便的配置下允许外网访问的端口。
默认所有绑定到外网ip或四个零的端口，外网都可以访问，然后，看看iptables文档，自己来配下咯。

[官方安装文档](http://sentry.readthedocs.org/en/stable/index.html#)


## 安装iptables

### Debian

安装:

    :::bash
    $ sudo apt-get install iptables

Debian系统中不需要启动iptables。

### CentOS

安装:

    :::bash
    $ sudo yum install iptables -y

启动:

    :::bash
    $ sudo service iptables start

### 配置iptables

配置指令Debian、CentOS都一样。

这两段抄的[kkyun blog](http://blog.kkyun.com/?p=50)

清除防火墙规则:

    ```
    #首先在清除前要将policy INPUT改成ACCEPT,表示接受一切请求。
    #这个一定要先做，不然清空后可能会悲剧
    $ sudo iptables -P INPUT ACCEPT

    #清空默认所有规则
    $ sudo iptables -F

    #清空自定义的所有规则
    $ sudo iptables -X

    #计数器置0
    $ sudo iptables -Z
    ```

常用配置:

    ```
    # 允许来自于lo接口的数据包
    # 如果没有此规则，你将不能通过127.0.0.1访问本地服务，例如ping 127.0.0.1
    $ sudo iptables -A INPUT -i lo -j ACCEPT

    # ssh端口22
    $ sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT

    # FTP端口21
    $ sudo iptables -A INPUT -p tcp --dport 21 -j ACCEPT

    # web服务端口80
    $ sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT

    # tomcat
    $ sudo iptables -A INPUT -p tcp --dport xxxx -j ACCEPT

    # mysql
    $ sudo iptables -A INPUT -p tcp --dport xxxx -j ACCEPT

    #允许icmp包通过,也就是允许ping
    $ sudo iptables -A INPUT -p icmp -m icmp --icmp-type 8 -j ACCEPT

    #允许所有对外请求的返回包
    #本机对外请求相当于OUTPUT,对于返回数据包必须接收啊，这相当于INPUT了
    $ sudo iptables -A INPUT -m state --state ESTABLISHED -j ACCEPT

    #如果要添加内网ip信任（接受其所有TCP请求）
    $ sudo iptables -A INPUT -p tcp -s 45.96.174.68 -j ACCEPT

    #过滤所有非以上规则的请求
    $ sudo iptables -P INPUT DROP

    #要封停一个IP，使用下面这条命令：
    $ sudo iptables -I INPUT -s ***.***.***.*** -j DROP

    #要解封一个IP，使用下面这条命令:
    $ sudo iptables -D INPUT -s ***.***.***.*** -j DROP
    ```

### 保存iptables配置

iptables配置好在当前环境生效，但，重启系统就不再可用。
所以，我们需要将iptables配置信息保存下来，并在下次系统开机时自动加载。

#### Debian

保存iptables配置到/etc/iptables:

    :::bash
    $ sudo bash -c 'iptables-save > /etc/iptables'

重启时/etc/iptables加载配置，修改/etc/network/if-pre-up.d/iptables内容如下:

    :::bash
    $ cat /etc/network/if-pre-up.d/iptables
    #!/bin/sh

    /sbin/iptables-restore < /etc/iptables

    $ sudo chmod +x /etc/network/if-pre-up.d/iptables

#### CentOS

保存iptables配置信息:

    :::bash
    $ sudo service iptables save
    iptables: Saving firewall rules to /etc/sysconfig/iptables:[  OK  ]

重启自动运行iptables:

    :::bash
    $ sudo chkconfig iptables on
