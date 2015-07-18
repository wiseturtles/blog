Title: Mac Pro初体验
Date: 2015-07-18 14:56
Tags: Mac
Slug: mac-pro-get-started
Author: ox0spy
Summary: Mac Pro环境配置


貌似如今不玩下Mac总觉得逼格不够，最近08年买的Thinkpad R60也坏掉了，就入手一台Mac Pro。
下面记录下环境配置和最近使用感受。


## XCode

    :::bash
    $ xcode-select --install


## Homebrew

[Homebrew](http://brew.sh)是Mac中非常受欢迎的包管理工具，熟悉Linux的朋友一定知道rpm/yum, dpkg/apt等。

    :::bash
    $ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    $ brew doctor
    $ man brew                     # manpage for brew
    $ brew install <package-name>  # install package
    $ brew update
    $ brew outdated
    $ brew upgrade <package-name>
    $ brew cleanup
    $ brew list --versions


## Homebrew Cask

通过Homebrew可以方便的管理命令行程序，Homebrew Cask可以管理图形界面程序。

    :::bash
    $ brew tap caskroom/cask
    $ brew install brew-cask
    $ brew cask install google-chrome
    $ brew update && brew upgrade brew-cask && brew cleanup


## iTerm2

从苹果App Store上搜索安装iTerm2.


## Zsh

    :::bash
    $ brew install zsh zsh-completions
    $ sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
    $ chsh -s /bin/zsh

Zsh还配置了powerline，开始Zsh、vim都使用powerline，后来vim使用vim-airline。
powerline要显示一些Unicode字符，需要安装打过patch的powerline字体。

安装powerline: https://powerline.readthedocs.org/en/latest/installation/linux.html
powerline font: https://github.com/powerline/fonts

字体安装后需要在iTerm2中选用刚安装的打过powerline patch的字体。


## vim

常用vim，在mac上配置下，曾经自己的vim配置有点乱了，发现［k-vim](https://github.com/wklken/k-vim)不错，就使用它了。


    :::bash
    $ git clone https://github.com/wklken/k-vim.git ~/k-vim
    $ cd ~/k-vim && bash -x install.sh

注：
1. k-vim没有适配最新版的vbundle，导致运行安装程序报错，基本就是Bundle修改为Plugin。。。
2. YouCompleteMe安装总失败，后来手动下载安装


## Intellij IDEA

IDEA运行需要JDK，从oracle官网下载、安装Java 1.8 JDK。

从IDEA -> Project Default -> Project Structure -> SDKS中添加JDK和Intellij Platform Plugin SDK。（需要选择JDK、Intellij的目录）

安装go-lang-idea-plugin插件，可以从[官网](https://plugins.jetbrains.com/plugin/5047)下载安装；也可以通过下面方式编译安装。

    :::bash
    $ git clone https://github.com/go-lang-plugin-org/go-lang-idea-plugin.git

IDEA中打开该plugin代码，配置IDEA Platform SDK版本，Build出jar包。然后，选择jar包安装。

配置IDEA的golang开发环境浪费了很多时间，尝试了不同版本的[go-lang-idea-plugin](https://github.com/go-lang-plugin-org/go-lang-idea-plugin)，总是报错“The selected directory is not a valid home for Go SDK”。
最后运行下面命令再选择GO SDK目录终于可以了。

    :::bash
    $ echo $GOROOT
    /Users/<my-home>/Projects/golang/sdk
    $ echo $GOPATH
    /Users/<my-home>/Projects/golang/mygo
    $ cd $GOROOT
    $ git checkout -b go1.4.2 go1.4.2
    $ cd src && ./all.bash
    $ cp $GOPATH/bin/go $GOROOT/bin/
    $ cp $GOPATH/bin/gofmt $GOROOT/bin/

注：
1. GOROOT是go的源代码，下载地址：https://github.com/golang/go
2. GOPATH是go workspace，自己的代码都$GOPATH/src下


## 最后

1. mac的屏的确要比我之前用过的笔记本好很多
2. 严重怀疑网上那些把mac捧得太高的人只用过Windows，根本没用过Ubuntu之类的桌面Linux (至少目前自己还没体会到mac比Linux高效在哪里)
3. 刚开始使用难免出错，也许上面的都是错的。。
