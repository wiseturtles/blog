Title: Ubuntu/Debian自动安装安全更新
Date: 2016-05-06 12:38
Tags: Ubunu, Debian
Slug: ubuntu-debian-automatic-security-updates
Author: ox0spy
Summary: Ubuntu/Debian自动安装安全更新

有台Ubuntu机器，仅仅为了科学上网，但，这年头漏洞这么多，万一哪天成肉鸡了呢。。。

本文简单记录下Ubuntu系统配置自己安装系统安全补丁。(Debian系统应该也适用)

## 安装unattended-upgrades自动更新安全补丁

    $ sudo apt-get install unattended-upgrades
    $ sudo dpkg-reconfigure unattended-upgrades  # 选Yes，自动下载安装

根据自己情况修改配置文件 - `/etc/apt/apt.conf.d/50unattended-upgrades`

可以设置邮件通知。

## 如果只想收到邮件通知，可以安装apticron

    $ apt-get install apticron

修改配置文件 - `/etc/apticron/apticron.conf`

## 订阅相关邮件列表，了解最新安全信息

- [Ubuntu Security Notices]<http://www.ubuntu.com/usn/>
- [Debian Security Information]<https://www.debian.org/security/index.en.html>

参考链接:

* <https://help.ubuntu.com/community/AutomaticSecurityUpdates>
* <https://spin.atomicobject.com/2014/08/04/debian-ubuntu-security-updates/>
