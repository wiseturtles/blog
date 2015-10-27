Title: Python Pypi源
Date: 2015-10-15 21:52
Tags: python, pip, pypi
Slug: config-python-pip
Author: ox0spy
Summary: 国内Pypi源


## pip安装

    :::bash
    $ wget https://bootstrap.pypa.io/get-pip.py
    $ sudo python get-pip.py

或者，直接使用发行版的包管理安装:

    :::bash
    $ sudo apt-get install python-pip  # Debian/Ubuntu


## pip配置

官方源比较慢，上面是一些国内源。

### 国内pypi源
- https://pypi.mirrors.ustc.edu.cn/simple/
- http://mirrors.aliyun.com/pypi/simple/
- http://pypi.v2ex.com/simple
- http://pypi.douban.com/

### 修改pip默认源

    :::bash
    $ cat .pip/pip.conf
    [global]
    trusted-host = mirrors.aliyun.com
    index-url = http://mirrors.aliyun.com/pypi/simple/

如果使用阿里云主机，请用下面的地址:
index-url = http://mirrors.aliyuncs.com/pypi/simple/

不加trusted-host会报下面的警告:

> The repository located at mirrors.aliyun.com is not a trusted or secure host and is being ignored. If this repository is available via HTTPS it is recommended to use HTTPS instead, otherwise you may silence this warning and allow it anyways with '--trusted-host mirrors.aliyun.com'.
