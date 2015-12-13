Title: Mac Python ValueError: unknown locale: UTF-8
Date: 2015-12-13 08:39
Tags: Python, Shell, Mac
Slug: mac-python-ValueError-unknown-locale-utf-8
Author: ox0spy
Summary: Mac Python报错: ValueError: unknown locale: UTF-8

Mac brew更新软件报locale utf-8 unknown。


## 问题描述

`brew update && brew upgrade`，更新 mpv 时报错: `ValueError: unknown locale: UTF-8`

#### 确定当前locale

    :::bash
    $ locale
    LANG=
    LC_COLLATE="C"
    LC_CTYPE="UTF-8"
    LC_MESSAGES="C"
    LC_MONETARY="C"
    LC_NUMERIC="C"
    LC_TIME="C"
    LC_ALL=

#### Python获取当前locale

    :::bash
	$ python -c 'import locale; print(locale.getdefaultlocale());'
    Traceback (most recent call last):
    File "<string>", line 1, in <module>
    File "/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7/lib/python2.7/locale.py", line 543, in getdefaultlocale return _parse_localename(localename)
    File "/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7/lib/python2.7/locale.py", line 475, in _parse_localename raise ValueError, 'unknown locale: %s' % localename
    ValueError: unknown locale: UTF-8

#### 解决

设置locale为en_US.UTF-8，我使用的zsh，所以在`~/.zshrc`中添加locale设置：

    :::bash
    export LANG=en_US.UTF-8
    export LC_CTYPE=en_US.UTF-8


再通过Python获取当前locale：

    :::bash
    $ python -c 'import locale; print(locale.getdefaultlocale());'
    ('en_US', 'UTF-8')


`brew upgrade`也正常工作了。
