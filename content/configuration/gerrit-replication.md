Title: Gerrit备份
Date: 2016-03-11 18:52
Tags: Gerrit,replication,MySQL
Slug: Gerrit-backup
Author: ox0spy
Summary: Gerrit备份

将Gerrit实时同步到其它系统完成Gerrit git repos备份。通常用这种方式完成Gerrit Mirror。

## 通过Gerrit replication plugin完成Gerrit同步

### 安装buck

    :::bash
    ubuntu@gerrit$ sudo apt-get install ant
    ubuntu@gerrit$ cd ~/download
    ubuntu@gerrit$ git clone https://github.com/facebook/buck.git
    ubuntu@gerrit$ cd buck
    ubuntu@gerrit$ ant  # 编译完成后 buck 可执行文件就在当前的bin目录
    ubuntu@gerrit$ echo 'export PATH=$HOME/download/buck/bin:$PATH' >> ~/.bashrc
    ubuntu@gerrit$ source ~/.bashrc

### 编译replication plugin

    :::bash
    ubuntu@gerrit$ git clone https://gerrit.googlesource.com/gerrit
    ubuntu@gerrit$ git checkout -b v2.11.4-tag v2.11.4  # 我gerrit版本是2.11.4
    ubuntu@gerrit$ git submodule update --init --recursive
    ubuntu@gerrit$ buck build plugins/replication:replication
    ubuntu@gerrit$ cp buck-out/gen/plugins/replication/replication.jar /tmp


### 安装replication plugin

    :::bash
    ubuntu@gerrit$ ssh -p 29418 localhost gerrit plugin install -n replication.jar - </tmp/replication.jar

### 配置replication

    :::bash
    ubuntu@gerrit$ cat etc/replication.config
    [remote "gerrit-backup"]
        url = ubuntu@10.x.x.x:/data/gerrit-backup/git/${name}.git
        push = +refs/heads/*:refs/heads/*
        push = +refs/tags/*:refs/tags/*
        timeout = 30
        threads = 3

### 同步一份代码到backup gerrit

    :::bash
    ubuntu@gerrit-backup $ sudo mkdir -p /data/gerrit-backup
    ubuntu@gerrit-backup $ sudo chown -R ubuntu /data
    ubuntu@gerrit-backup $ exit  # 退出gerrit-backup

    ubuntu@gerrit$ cd ~/apps/gerrit/review_site  # 登陆gerrit,并进入Gerrit目录
    ubuntu@gerrit$ tar cf - git | ssh gerrit-backup "cd /data/gerrit-backup && tar xf -"

### 开始同步

    :::bash
    ubuntu@gerrit$ ssh -p 29418 localhost gerrit plugin reload replication  # reload
    ubuntu@gerrit$ ssh -p 29418 localhost replication start --wait --all  # start replication

## Gerrit MySQL备份

通过automysqlbackup备份MySQL数据到本地文件系统.

    :::bash
    ubuntu@gerrit$ sudo apt-get install automysqlbackup
    ubuntu@gerrit$ sudo automysqlbackup  # 运行automysqlbackup测试是否可以备份，可能需要修改 /etc/default/automysqlbackup 和 /etc/mysql* 配置文件

如果需要可以将MySQL数据定期同步到Amazon S3等系统存储.


## 参考文档:

- [config-replication.txt](https://gerrit.googlesource.com/gerrit/+/v2.0.2/Documentation/config-replication.txt)
