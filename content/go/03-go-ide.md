Title: Go学习笔记——(3)打造Sublime Text 3作为Go的集成开发环境
Date: 2015-07-13 16:45
Tags: go, ide, sublime
Slug: go-ide
Author: crazygit
Summary: go学习笔记——(3)打造Sublime Text 3作为GO的集成开发环境(IDE)


### 可用于GO开发的工具

可以用于GO开发的工具和插件目前已经非常多了,如VIM, Emacs, atom等，这里[IDEs and Plugins for
Go](https://github.com/golang/go/wiki/IDEsAndTextEditorPlugins)罗列了许多可以作为GO开发
的IDE和插件，我们可以根据自己的使用习惯自行选择。本文主要阐述如何利用Sublime
Text 3 作为GO的开发环境.


### 安装Sublime text 3及插件

到Sublime 官网选择适合自己系统的版本<http://www.sublimetext.com/3>, 我选择的是
Ubuntu 64位的tarball包，解压出来可以直接用了。

依次安装插件

* Package Control
* GoSublime
* GoDef

这里我只列出了Go开发必须的插件, 其他的一些插件可以根据自身需要选择安装或者从
<http://blog.wiseturtles.com/posts/go-introduce.html>选择热门插件


### 安装插件依赖的Go Package

上面的插件需要用到一些go cmd tools, 但是这些工具因为墙的问题，没法直接下载，好
在Github上面由这些工具的镜像，因此我们可以曲线救国，从镜像下载。在下载之前，首先，还是要先设置`GOPATH`变
量, 怎么设置可以参考本系列文章第二篇<http://blog.wiseturtles.com/posts/go-introduce.html>

安装必备的cmd tools

    :::bash
    #　创建目录
    $ export GOPATH='your_go_path'
    $ mkdir -p $GOPATH/src/golang.org/x

    # 根据实际需要下载对应分支的tools
    $ git clone -b release-branch.go1.4 git@github.com:golang/tools.git $GOPATH/src/golang.org/x/tools
    $ cd $GOPATH
    # 安装工具
    $ go install golang.org/x/tools/cmd/goimports
    $ go install golang.org/x/tools/cmd/vet
    $ go install golang.org/x/tools/cmd/oracle
    $ go install golang.org/x/tools/cmd/godoc

    # 安装不需要翻墙的工具
    $ go get github.com/rogpeppe/godef

    # 最后两个是我做web开发需要安装的包，没有需要的话可以不下载
    $ go get github.com/astaxie/beego
    $ go get github.com/beego/bee

### 配置插件:

* GoSublime 配置, Preferences -> Package Settings -> GoSublime ->　Settings - User

        {
            // you may set specific environment variables here
            // e.g "env": { "PATH": "$HOME/go/bin:$PATH" }
            // in values, $PATH and ${PATH} are replaced with
            // the corresponding environment(PATH) variable, if it exists.
            //根据实际情况设置如下变量
            "env": {"GOROOT": "/usr/local/go", "GOPATH": "$HOME/golang", "PATH": "$GOPATH/bin:$GOROOT/bin:$PATH" },

            "fmt_cmd": ["goimports"],

            // enable comp-lint, this will effectively disable the live linter
            "comp_lint_enabled": true,

            // list of commands to run
            "comp_lint_commands": [
                // run `golint` on all files in the package
                // "shell":true is required in order to run the command through your shell (to expand `*.go`)
                // also see: the documentation for the `shell` setting in the default settings file ctrl+dot,ctrl+4
                {"cmd": ["golint *.go"], "shell": true},

                // run go vet on the package
                {"cmd": ["go", "vet"]},

                // run `go install` on the package. GOBIN is set,
                // so `main` packages shouldn't result in the installation of a binary
                {"cmd": ["go", "install"]}
            ],

            "on_save": [
                // run comp-lint when you save,
                // naturally, you can also bind this command `gs_comp_lint`
                // to a key binding if you want
                {"cmd": "gs_comp_lint"}
            ]
        }

* GoDef 配置, Preferences -> Package Settings -> GoDef ->　Settings - User

        {
            //根据实际情况设置如下变量
            "gopath": "/home/linliang/golang"
        }


### 使用

创建一个Go文件，默认情况下:

* 连续两次输入`Ctrl + dot(.)`, 可以查看GoSublime的功能和快捷键.
* 使用`gd`可以使用GoDef插件的跳转, 更多使用可以参考两个插件的帮助文档
