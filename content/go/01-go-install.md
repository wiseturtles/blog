Title:  Go学习笔记——(1)安装Go
Date: 2015-06-30 23:11
Tags: go, 入门
Slug: go-install
Author: crazygit
Summary: go学习笔记——(1)安装go


本文参考于:
[Installing Go - Getting Started](https://golang.org/doc/install)


### 必备技能之翻墙

这个是必须的技能，不然go的官网都没法访问, 后面也不用看了。

### 开发环境搭建

整个安装过程比较简单，下载安装包，配置环境变量即可。

以Linux为例. 

    $ wget https://storage.googleapis.com/golang/go1.4.2.linux-amd64.tar.gz
    $ tar -C /usr/local -xzf go1.4.2.linux-amd64.tar.gz

添加环境变量: 

    export GOROOT=/usr/local/go
    export PATH=$PATH:$GOROOT/bin

`GOROOT`是告诉系统Go安装在哪里，
`PATH`是指定Go相关命令的调用路径.

环境检查，按照国际惯例，当然是先来"Hello World". 创建`hello.go`: 

    :::go
    package main

    import "fmt"

    func main() {
        fmt.Printf("hello, world\n")
    }

执行

    $ go run hello.go
    hello, world

如果输出"hello,world"， 则表示环境没有什么问题. 

