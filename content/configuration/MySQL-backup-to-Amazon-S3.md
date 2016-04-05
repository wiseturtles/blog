Title: MySQL自动备份，并同步到AmazonS3
Date: 2016-04-05 11:39
Tags: mysql, backup, S3
Slug: MySQL-backup-to-Amazon-S3
Author: ox0spy
Summary: MySQL auto backup to Amazon S3

MySQL自动备份，并将本地备份同步到Amazon S3，然后配置邮件通知。

注: 系统为Ubuntu 14.04，Debian系统也类似。

## 安装automysqlbackup

    $ sudo apt-get install automysqlbackup

## 配置automysqlbackup

### 参数介绍

配置文件路径: `/etc/default/automysqlbackup`

主要参数:
USERNAME - 数据库登陆用户名
PASSWORD - 数据库登陆密码
DBHOST - 数据库主机名或IP地址
DBNAMES - 需要备份的MySQL数据库
BACKUPDIR - 备份文件存放路径
SOCKET - MySQL服务的本地unix socket路径
MAILCONTENT - 发送邮件内容，可以为: log, files, stdout, quiet
MAXATTSIZE - 最大允许的邮件内容大小
MAILADDR - 接收通知的邮箱地址
PREBACKUP - 备份前运行的脚本
POSTBACKUP - 备份后运行的脚本

其它参数参考 `/etc/default/automysqlbackup`

修改`DBNAMES`, `BACKUPDIR`，指定需要备份的数据库名称和备份文件存放路径。


### 发送邮件通知

修改`MAILCONTENT`, `MAILADDR`指定发送什么内容到指定邮箱。

注: 先确保通过postfix在命令行可以发送邮件到你的邮箱.


### 备份到Amazon S3

安装s3cmd，使用s3cmd同步备份文件到Amazon S3。

    $ sudo pip install s3cmd

修改`POSTBACKUP`，备份完成后同步备份文件到Amazon S3。

    POSTBACKUP=/etc/automysqlbackup/mysql-backup-post
    $ cat /etc/automysqlbackup/mysql-backup-post
    #!/bin/bash

    sudo /usr/local/bin/s3cmd -c /home/user/.s3cfg -r sync local-automysqlbackup-path s3://your-backup-bucket/

注: 备份前配置s3cmd，确保它有权限操作你的S3 bucket
