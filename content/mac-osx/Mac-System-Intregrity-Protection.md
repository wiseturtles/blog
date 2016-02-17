Title: Mac System Intregrity Protection - Operation not permitted
Date: 2016-02-16 14:36
Tags: Mac, SIP
Slug: Mac-System-Intregrity-Protection
Author: ox0spy
Summary: Mac删除系统文件报错

貌似刚拿到电脑是自己手动编译安装了vim 7.3，后来都是brew install vim最新版本。

今天vim出了点问题，发现系统上还有个vim 7.3，准备删除时就报`Operation not permitted`


## 问题描述

```
$ sudo rm -rf /usr/share/vim/
rm: /usr/share/vim: Operation not permitted
```

习惯Linux我就觉得有没有搞错，我是root呀，什么文件不能删除呢。。。

Google下才知道Apple为了防止恶意软件破坏系统开启了[System Intregrity Protection](https://support.apple.com/en-us/HT204899)。

## 解决

查看文件flag:

```
$ ls -lO /usr/share/vim
-rwxr-xr-x  8 root  wheel  restricted - Aug  2 22:36 /usr/share/vim
```

参考: <http://stackoverflow.com/questions/30768087/restricted-folder-files-in-os-x-el-capitan>

- reboot
- as soon as you hear the "Mac sound" on the grey screen, press Cmd+R to enter Recovery mode
- Open Utilities->Terminal
- Run the command csrutil disable
- Reboot, you'll land in the normal OS with SIP disabled
- do all the changes you'd like to do
- Reboot again
- as soon as you hear the "Mac sound" on the grey screen, press Cmd+R to enter Recovery mode
- Enable SIP with csrutil enable
- Reboot again
- done

流程如下:

重启 -> Command+R，进入恢复模式 -> 在终端通过`csrutil disable`禁掉SIP -> 重启 -> 删除文件 -> 再通过Command+R，进入恢复模式 -> 通过 `csrutil enable` 启用SIP -> 再次重启

查看SIP状态:

```
$ csrutil status
System Integrity Protection status: enabled.
```
