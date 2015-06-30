Title:  Go学习笔记——(2)初始Go
Date: 2015-06-30 23:37
Tags: go, 入门
Slug: go-introduce
Author: crazygit
Summary: go学习笔记——(2)初识Go
status: draft


本文参考于:
[How to Write Go Code](https://golang.org/doc/instal://golang.org/doc/code.html)


## 代码组织


#### 工作空间

Go tool先天就是设计来与开源仓库协作的，不管你愿不愿意发布你的代码，构建开发环境的方式是一样的。

Go代码必须保存在一个工作空间里，　一个工作空间要有三个根目录

* src    Go源代码
* pkg    Go包对象
* bin    包含可执行命令

一个工作空间的示例:
<pre>

bin/
    hello                          # command executable
    outyet                         # command executable
pkg/
    linux_amd64/
        github.com/golang/example/
            stringutil.a           # package object
src/
    github.com/golang/example/
        .git/                      # Git repository metadata
    hello/
        hello.go               # command source
    outyet/
        main.go                # command source
        main_test.go           # test source
    stringutil/
        reverse.go             # package source
        reverse_test.go        # test source
    github.com/golang/project1/
        ......
    github.com/golang/project2/
        ......

</pre>


#### 设置GOPATH环境变量

GOPATH是Go中唯一必须需要设置的环境变量, GOPATH就是工作空间的路径

如:

    $ mkdir $HOME/go
    $ export GOPATH=$HOME/go


#### 包路径

#### 第一个Go程序

#### 第一个Go库

#### 包名

## 测试

## 第三方包
