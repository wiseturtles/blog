Title: Linux远程文件拷贝
Date: 2015-11-11 10:12
Tags: Linux, ssh, sync, python, tar
Slug: copy-remote-host-file
Author: ox0spy
Summary: Linux远程文件拷贝


我们经常会碰到从一个主机上拷贝文件到其他主机，本文汇总下常用方法。

## ssh

提到远程文件拷贝，大家肯定首先想到的是ssh。(啥? 你想到的是ftp?? 搭建个ftp好麻烦...)

避免输入用户密码，可以先运行:

    :::bash
    $ ssh-copy-id <user@remote-host>  # 输入密码，它会将你的key(~/.ssh/id_rsa.pub)添加到remote-host:~user/.ssh/authorized_keys


通过scp做文件拷贝:

    :::bash
    $ scp [-r] [-P port] <your-local-file> []<user>@]<remote-host>:<remote-file-path>

如果网络比较慢可以先压缩再拷贝:

    :::bash
    $ ssh user@remote-host "tar zcf - /file/path/to/copy" | tar zxf - -C /file/path/to/receive  # 从remote-host拷贝文件回来
    $ tar zcf - /file/path/to/copy | ssh user@remote-host "tar zxf - -C /file/path/to/receive"  # 将本地文件拷贝到remote-host


## HTTP

也可以通过HTTP协议拷贝，如果本地正好有nginx/apache，ln -s 创建个软链接到外部可以访问的路径，从其它机器可以通过wget下载。
但，不是所有机器都装了nginx/apache，可以通过Python自带模块快速启动一个HTTP Simple Server。

    :::bash
    $ python -mSimpleHTTPServer  # 默认监听8000端口，你当然可以自己指定端口
    $ python -mSimpleHTTPServer 8888  # 指定监听端口为8888
    $ wget listen-ip:port/<file/path> # 从其它主机拷贝文件

既然已经有了HTTP Server，你当然可以通过浏览器访问了。

HTTP完全可以支持断点续传，wget -c 就可以。


## rsync

大家可能都体会过scp传输过程中，网络、主机异常导致必须重新传，小文件、网络快还好，不然真的想打人。
你一定想如果可以断点续传就好了，rsync可以完成你的心愿。

    :::bash
    $ rsync -P --rsh=ssh --progress <your-local-file> user@remote-host:<receive-file-path>
    $ rsync -P -v -e ssh <local-file> user@remote-host:receive-file-path  # 本地同步文件到remote-host
    $ rsync -P -v -e ssh user@remote-host:receive-file-path <local-file-path>  # remote-host文件同步到本地


rsync功能强大，以后再补充。

## zsync

先安装后看文档吧，基于HTTP的rsync，使用有一定限制，必须服务端有 .zsync 才行。优点是速度非常快。
