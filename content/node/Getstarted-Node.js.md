Title:  Node.js入门
Date: 2015-09-18 13:49
Tags: node.js
Slug: Getstarted-Node.js
Author: ox0spy
Summary: Node.js入门

大家都知道Node.js是基于JavaScript的，使JavaScript可以用于后台开发。

## 为啥学JavaScript

- 公司项目需要
- JavaScript程序员之多社区之活跃
- Node.js发展非常快
- 更容易成为全栈工程师 (前端、后台、客户端[React Native])

## nvm

nvm (Node Version Manager)类似Python中的`virtualenv`，是管理Node.js版本的工具，
方便在主机上安装多个Node.js版本，安装方法如下：

    :::bash
    $ curl https://raw.githubusercontent.com/creationix/nvm/v0.23.2/install.sh | bash

常用命令:

    :::bash
    $ nvm --version  # 查看nvm版本
    $ nvm -h  # 查看nvm帮助文档
    $ nvm current  # 查看当前使用的node.js版本
    $ nvm install stable
    $ nvm install <version>  # 安装指定版本的node.js
    $ nvm uninstall <version>  # 卸载指定版本的node.js
    $ nvm use <version>  # 将默认node.js版本切换到指定版本


## npm

npm (Node Package Manager)是Node.js默认的模块管理器，用来安装管理Node.js模块。
npm已经集成到Node.js中了，所以装完Node.js就不再需要单独安装npm。

常用命令如下：

    :::bash
    $ npm help  # 查看帮助
    $ npm -l  # npm命令列表
    $ npm install npm@latest -g  # 将npm更新到最新版本
    $ npm -v  # 查看npm版本
    $ npm config list -l # 查看npm配置
    $ npm info
    $ npm search
    $ npm list
    $ npm install
    $ npm update
    $ npm uninstall

更多信息请参考阮一峰的[npm模块管理器](http://javascript.ruanyifeng.com/nodejs/npm.html)


## Node.js学习

- [Node.js入门](http://www.nodebeginner.org/index-zh-cn.html)
- [从零开始Node.js系列](http://blog.fens.me/series-nodejs/)
- [Node.js包教不包会](https://github.com/alsotang/node-lessons)
- [JavaScript标准参考教程](http://javascript.ruanyifeng.com/#nodejs)有些章节专门介绍Node.js。

还在看上面文章学习的阶段 :D
