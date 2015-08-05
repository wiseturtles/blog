Title: Ubuntu install Sogou Input
Date: 2015-08-05 17:26
Tags: Ubuntu
Slug: Ubuntu-install-Sogou-Input
Author: Zhang Wanming
Summary: Ubuntu安装Sogou输入法

刚拿到一台新电脑，安装了Ubuntu 14.04，下面记录下安装Sogou输入法。

## 安装

从 http://pinyin.sogou.com/linux/?r=pinyin 下载deb安装包。（注意查看自己系统是32位，还是64位）

系统是32位 or 64位？

    :::bash
    $ uname -m

拿到Sogou Input Deb包后安装。

    :::bash
    $ sudo dpkg -i <sogoupinyin_1.2.0.0056_amd64.deb>  # <>中是您的deb包名
    $ sudo dpkg -P sogoupinyin  # 可以先卸载了，避免看到一些该包没安装完整的错误相信

安装过程中可能会看到该Deb包依赖很多其他包，请逐个安装依赖的包。

    :::bash
    $ sudo apt-get install fcitx fcitx-frontend-gtk2 fcitx-frontend-gtk3 fcitx-frontend-qt4 fcitx-module-kimpanel fcitx-libs fcitx-libs-qt  # 这是我缺少的依赖

然后，再安装下Sogou拼音输入法。

    :::bash
    $ sudo dpkg -i <sogoupinyin_1.2.0.0056_amd64.deb>  # <>中是您的deb包名


## 设置

重启电脑，登陆进入后，点击右上角 输入法设置，添加sogou输入法。

CTRL+SPACE 激活、关闭sogou输入法。
