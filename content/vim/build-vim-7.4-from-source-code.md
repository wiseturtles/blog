Title: 从源码编译安装vim 7.4
Date: 2015-03-07 00:15
Tags: vim, ubuntu
Slug: build-vim-7.4
Author: Zhang Wanming
Summary: Ubuntu 12.04上源码编译安装vim 7.4


### 准备编译环境

        $ sudo apt-get build-dep vim
        $ sudo apt-get install libncurses5-dev libgnome2-dev libgnomeui-dev \
                libgtk2.0-dev libatk1.0-dev libbonoboui2-dev \
                libcairo2-dev libx11-dev libxpm-dev libxt-dev python-dev \
                ruby-dev mercurial
        $ sudo apt-get install checkinstall


### 删除系统vim包
        $ sudo apt-get purge vim-tiny vim-common vim-runtime vim


### 下载编译

        $ hg clone https://code.google.com/p/vim/
        $ cd vim
        $ ./configure --with-features=huge \
          --enable-multibyte \
          --enable-perlinterp=dynamic \
          --enable-pythoninterp=dynamic \
          --enable-rubyinterp=dynamic \
          --enable-luainterp --with-lua-prefix=/usr \
          --with-python-config-dir=/usr/lib/python2.7/config \
          --enable-gui=auto \
          --enable-gtk2-check \
          --enable-gnome-check \
          --enable-cscope \
          --with-x \
          --prefix=/usr
        $ make VIMRUNTIMEDIR=/usr/share/vim/vim74
        $ sudo checkinstall
        $ vim --version
        $ sudo update-alternatives --install /usr/bin/editor editor /usr/bin/vim 1
        $ sudo update-alternatives --set editor /usr/bin/vim
        $ sudo update-alternatives --install /usr/bin/vi vi /usr/bin/vim 1
        $ sudo update-alternatives --set vi /usr/bin/vim

### 坑
0. Ubuntu系统包中的vim太老了
1. 浪费生命的寡妇王
2. ./configure --with-luajit 总失败，最后直接去掉

### 收获
0. checkinstall 是个好东西
