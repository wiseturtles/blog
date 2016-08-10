Title: SaltStack介绍
Date: 2016-08-10 20:40
Tags: CentOS, SaltStack
Slug: get-started-saltstack
Author: ox0spy
Summary: SaltStack介绍

本文只介绍了SaltStack在CentOS上的安装，其它其它有类似的包管理工具可以安装.


## CentOS上安装salt-master和salt-minion

### 安装salt-master

在centos上安装salt-master:

    $ sudo rpm --import https://repo.saltstack.com/yum/redhat/7/x86_64/latest/SALTSTACK-GPG-KEY.pub
    $ sudo bash -c 'cat - > /etc/yum.repos.d/saltstack.repo <<"EOF"
[saltstack-repo]
name=SaltStack repo for RHEL/CentOS $releasever
baseurl=https://repo.saltstack.com/yum/redhat/$releasever/$basearch/latest
enabled=1
gpgcheck=1
gpgkey=https://repo.saltstack.com/yum/redhat/$releasever/$basearch/latest/SALTSTACK-GPG-KEY.pub
EOF'
    $ sudo yum clean expire-cache
    $ sudo yum install -y salt-master
    $ sudo systemctl enable salt-master.service
    $ sudo systemctl restart salt-master.service

### 安装salt-minion

在centos上安装salt-minion:

    $ sudo rpm --import https://repo.saltstack.com/yum/redhat/7/x86_64/latest/SALTSTACK-GPG-KEY.pub
    $ sudo bash -c 'cat - > /etc/yum.repos.d/saltstack.repo <<"EOF"
[saltstack-repo]
name=SaltStack repo for RHEL/CentOS $releasever
baseurl=https://repo.saltstack.com/yum/redhat/$releasever/$basearch/latest
enabled=1
gpgcheck=1
gpgkey=https://repo.saltstack.com/yum/redhat/$releasever/$basearch/latest/SALTSTACK-GPG-KEY.pub
EOF'
    $ sudo yum clean expire-cache
    $ sudo yum install -y salt-minion
    $ sudo bash -c "echo 'master: $SALT_MASTER' >> /etc/salt/minion" # $SALT_MASTER 替换为salt master主机的IP
    $ sudo systemctl enable salt-minion.service
    $ sudo systemctl restart salt-minion.service

注: 如果salt-master使用默认配置，请确保salt-master的4505, 4506端口可以被salt-minion访问.

### 简单测试

salt-minion设置过master IP并重启salt-minion后，应该在salt-master上可以通过下面命令看到minion:

    [root@master ~]$ salt-key -L  # 列出所有minion
    [root@master ~]$ salt-key -A  # 接受所有minion，也可以通过 -a 接受指定minion

接受minion后，就可以在salt-master上发布命令到minion了。

    [root@master ~]$ salt '*' test.ping  # 简单测试master <-> minion是否连通

## 选择主机

经常会看到 `salt '*' test.ping` 这里的 `'*'` 意思是作用于所有主机。

下面介绍 salt 支持的匹配方式。

### globbing

    [root@master ~]$ salt 'ubuntu*' disk.usage

### grains system

    [root@master ~]$ salt -G 'os:CentOS' cmd.run 'id'

### regular expression

    [root@master ~]$ salt -E 'centos[0-9]' test.ping

### 明确指定一个列表

    [root@master ~]$ salt -L 'centos1,centos2' test.ping

### multiple target types can be combined in one command

    [root@master ~]$ salt -C 'G@os:CentOS and centos* or S@192.168.50.*' test.ping

注: 参考 - <https://docs.saltstack.com/en/getstarted/fundamentals/targeting.html>

## 执行命令

### 执行单个命令，比如：在minion上执行`id`命令并输出:

    [root@master ~]$ salt '*' cmd.run 'id'

### 执行脚本：

首先要开启`/etc/salt/master`的如下设置:

    file_roots:
      base:
        - /srv/salt

如果salt-master没有`/srv/salt/scripts`目录请自己创建，然后写个简单脚本:

    [root@master ~]$ cat /srv/salt/scripts/get_ip.sh
    #!/bin/bash

    ifconfig | grep 'inet ' | grep -Ev '127.0.0.1' | awk '{print $2}'

    [root@master ~]$ salt '*' cmd.script 'salt://scripts/get_ip.sh'

## Tips

### 以指定用户运行salt-master，避免每次输入salt指令都需要加 sudo；比如以centos用户运行salt-master

    [centos@master ~]$ sudo chown -R centos /etc/salt /var/log/salt /var/cache/salt /var/run/salt
    [centos@master ~]$ sudo mkdir -p /srv/salt
    [centos@master ~]$ sudo chown -R centos /srv/salt
    在 /etc/salt/master 中设置 user: centos

注: 理论上salt-minion也可以通过这种方式运行以指定用户运行，但我测试会报错 "Minion did not return. [No response]"

### 删除不存在的salt minion

    [root@master ~]$ salt-run manage.down removekeys=True
