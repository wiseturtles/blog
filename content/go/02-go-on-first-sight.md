Title:  Go学习笔记——(2)初始Go
Date: 2015-06-30 23:37
Tags: go, 入门
Slug: go-introduce
Author: crazygit
Summary: go学习笔记——(2)初识Go


本文参考于:
[How to Write Go Code](https://golang.org/doc/code.html)


## 代码组织
### 工作空间

Go tool先天就是设计来与开源仓库协作的，不管你愿不愿意发布你的代码，构建开发环境的方式是一样的。

Go代码必须保存在一个工作空间里，　一个工作空间要有三个根目录

* src    
Go源代码

* pkg    
Go库文件

* bin   
包含可执行命令

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


### 设置GOPATH环境变量

GOPATH是Go中唯一必须需要设置的环境变量, GOPATH就是工作空间的路径

如:

    $ mkdir $HOME/go
    $ export GOPATH=$HOME/go


### 包路径

无论你是否要发布你的程序, 你都应该以要发布的方式来构建你的程序,最好的包名是
github.com/user

    $ mkdir -p $GOPATH/src/github.com/user

### 第一个Go程序


下面，我将介绍如何将从头构建一个简单的go程序.
首先, 我们以`/data/github/golang`为工作空间

    $ mkdir -p /data/github/golang
    $ cd /data/github/golang
    $ export GOPATH=$(pwd)

为了创建一个简单的程序. 首先要选择包路径, 如`github.com/crazygit/hello`, 并创建对于的目录结构

    $ mkdir -p $GOPATH/src/github.com/crazygit/hello

在目录`$GOPATH/src/github.com/crazygit/hello`里创建`hello.go`

    :::go
    package main

    import "fmt"

    func main() {
            fmt.Println("Hello world")
    }

使用go工具编译并安装程序
 
    $ cd $GOPATH
    $ go install github.com/crazygit/hello

或者

    $ cd $GOPATH/github.com/crazygit/hello
    $ go install

执行了之后，可以看到`$GOPATH`中多了一个`bin`目录，里面有一个名为`hello`的可执行文件

    $ $GOPATH/bin/hello
    Hello, world.

### 第一个Go库

让我们再创建一个库，同样，先创建包路径`github.com/crazygit/stringutil`

    $ mkdir $GOPATH/src/github.com/crazygit/stringutil

在里面再创建一个名为`reverse.go`

    :::go
    package stringutil

    func Reverse(s string) string {
        r := []rune(s)
        for i, j := 0, len(r)-1; i < len(r)/2; i, j = i+1, j-1 {
            r[i], r[j] = r[j], r[i]
        }
        return string(r)
    }

编译

    $ cd $GOPATH
    $ go build github.com/crazygit/stringutil

编译过程不会有什么文件产生, 可以使用`go install`, 它会创建pkg目录
并生成`pkg/linux_amd64/github.com/crazygit/stringutil.a`文件.


修改`hello.go`,让它使用我们刚刚创建的库

    :::go
    import (
        "fmt"
        "github.com/crazygit/stringutil"
    )

    func main() {
        fmt.Println("Hello world")
        fmt.Printf(stringutil.Reverse("!oG ,olleH"))
    }

安装，当安装的的时候，它会自动根据安装依赖,所以安装`hello`时, 它会自动安装`stringutil`

    $ go install github.com/crazygit/hello

运行

    $ $GOPATH/bin/hello
    Hello, Go!


### 包名

Go代码文件的第一句话必须是

    :::go
    package name

name就是要引起的包名，所有在同一个包下的包名也一样

go里面为了方便，会使用引入包路径的最后一段作为包名，如 `crazygit/rot14`的包名就是`rot14`

可执行的命令必须引入包`package main`

## 测试

Go自带了一个使用`go test`的测试框架，为了写一个测试文件。

应该创建一个文件名`_test.go`结尾的文件，函数名为如`TestXXX`的, 并且有参数`t *testing.T`

让我们为stringutil包创建测试`$GOPATH/src/github.com/crazygit/stringutil/reverse_test.go`

    :::go
    package stringutil

    import "testing"

    func TestReverse(t *testing.T) {
        cases := []struct {
            in, want string
        }{
            {"Hello, world", "dlrow ,olleH"},
            {"Hello, 世界", "界世 ,olleH"},
            {"", ""},
        }

        for _, c := range cases {
            got := Reverse(c.in)
            if got != c.want {
                t.Errorf("Reverse(%q) == %q, want %q", c.in, got, c.want)
            }
        }
    }

执行测试

    $ go test github.com/crazygit/stringutil
    ok      github.com/crazygit/stringutil  0.002s


## 第三方包

    $ go get github.com/golang/example/hello
    $ $GOPATH/bin/hello
    Hello, Go examples!

如果当前包已经存在，`go get`会跳过下载


到此，我们对go有了个大致的印象，虽然有些地方看不懂，不过没有关系，我们后面会继续学习。
