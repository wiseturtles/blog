Title: Python Gevent安装报错
Date: 2015-10-31 20:46
Tags: python, pip, gevent
Slug: gevent-install-error
Author: ox0spy
Summary: Python Gevent安装报错


Mac上pip安装gevent报错信息如下：

    libev/ev.c:1029:42: error: '_Noreturn' keyword must precede function declarator

解决：

    :::bash
    $ CFLAGS='-std=c99' pip install gevent

这里有讨论：https://github.com/NixOS/nixpkgs/issues/8569
