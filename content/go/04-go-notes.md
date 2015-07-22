Title: Go学习笔记4之知识点记录
Date: 2015-07-22 14:09
Tags: go, ide, note
Slug: go-notes
Author: crazygit
Summary: Go学习笔记4之知识点记录

### Go环境配置

* 如果你想在同一个系统中安装多个版本的Go，你可以参考第三方工具[GVM](https://github.com/moovweb/gvm)，这是目前在这
方面做得最好的工具。

* GOPATH允许多个目录, 当GOPATH有多个目录时，为了让每个目录下的bin目录都加入环境变量
可以设置`${GOPATH//://bin:}/bin`

        :::bash
        export GOROOT="/usr/local/go"
        export GOPATH="$HOME/golang:$HOME/github/golang"
        export PATH=$PATH:$GOROOT/bin:${GOPATH//://bin:}/bin

### Go 命令

详细使用可以参考
<https://github.com/astaxie/build-web-application-with-golang/blob/master/zh/01.3.md>

* go build
* go clean
* go fmt
* go install
* go test
* go tool fix
* go tool vet directory|files
* go generate
* godoc
* go version
* go env
* go list
* go run

### Go字符串

字符串是用一对双引号（""）或反引号（\`\`）括起来定义，它的类型是string
如果要声明一个多行的字符串怎么办？可以通过\`来声明

    :::go
     m := `hello
            world`


### iota枚举

Go里面有一个关键字iota，这个关键字用来声明enum的时候采用，它默认开始值是0，每调用一次加1：

    :::go
    const(
        x = iota  // x == 0
        y = iota  // y == 1
        z = iota  // z == 2
        w  // 常量声明省略值时，默认和之前一个值的字面相同。这里隐式地说w = iota，因此w == 3。其实上面y和z可同样不用"= iota"
    )

    const v = iota // 每遇到一个const关键字，iota就会重置，此时v == 0

    const (
    e, f, g = iota, iota, iota //e=0,f=0,g=0 iota在同一行值相同
    )

> 除非被显式设置为其它值或iota，每个const分组的第一个常量被默认设置为它的0值，第二及后续的常量被默认设置为它前面那个常量的值，如果前面那个常量的值是iota，则它也被设置为iota。

### 默认变量及函数名规则


* 大写字母开头的变量是可导出的，也就是其它包可以读取的，是公用变量；小写字母开头的就是不可导出的，是私有变量。
* 大写字母开头的函数也是一样，相当于class中的带public关键词的公有函数；小写字母开头的就是有private关键词的私有函数。


### 数组

声明

    :::go
    a := [3]int{1, 2, 3} // 声明了一个长度为3的int数组
    b := [10]int{1, 2, 3} // 声明了一个长度为10的int数组，其中前三个元素初始化为1、2、3，其它默认为0
    c := [...]int{4, 5, 6} // 可以省略长度而采用`...`的方式，Go会自动根据元素个数来计算长度


二维数组

    :::go
    // 声明了一个二维数组，该数组以两个数组作为元素，其中每个数组中又有4个int类型的元素
    doubleArray := [2][4]int{[4]int{1, 2, 3, 4}, [4]int{5, 6, 7, 8}}

    // 上面的声明可以简化，直接忽略内部的类型
    easyArray := [2][4]int{{1, 2, 3, 4}, {5, 6, 7, 8}}


*注意*: 数组之间的赋值是值的赋值，即当把一个数组作为参数传入函数的时候，传入的其实是该数组的副本，而不是它的指针。如果要使用指针，那么就需要用到后面介绍的slice类型了。


### Slice

注意slice和数组在声明时的区别：声明数组时，方括号内写明了数组的长度或使用...自动计算长度，而声明slice时，方括号内没有任何字符。
