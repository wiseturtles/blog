Title: Go学习笔记5之Beego框架
Date: 2015-07-22 16:33
Tags: go, beego
Slug: go-hello-beego
Author: crazygit
Summary: Go学习笔记5之Beego框架

### Beego框架准备

    $ go get github.com/astaxie/beego
    $ go get github.com/beego/bee

创建程序`hello-beego.go`

    :::go
    package main

    import (
            "github.com/astaxie/beego"
    )

    type MainController struct {
         beego.Controller
    }

    func (this *MainController) Get() {
        this.Ctx.WriteString("hello world")
    }

    func main() {
        beego.Router("/", &MainController{})
        beego.Run()
    }

执行`go run hello-beego.go`, 访问<http://127.0.0.1:8080>检查，　如果输出"hello world" 表示本地beego环境已经搭建成功
