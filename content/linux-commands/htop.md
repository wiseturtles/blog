Title: htop
Date: 2015-01-09 14:04
Tags: linux, command, htop
Slug: linux-htop
Author: crazygit
Summary: the usage of htop



本文转摘自 [Linux运维笔记](https://blog.linuxeye.com/350.html).  并做适当修改　

## 简介

Htop是一款运行于Linux系统监控与进程管理软件，用于取代Unix下传统的top。与top只提供最消耗资源的进程列表不同，htop提供所有进程的列表，并且使用彩色标识出处理器、swap和内存状态。

用户一般可以在top无法提供详尽系统信息的情况下选择安装并使用htop。比如，在查找应用程序的内存泄漏问题时。与top相比，htop提供更方便、光标控制的界面来杀死进程。

htop用C语言编写，采用了ncurses库。htop的名称源于其作者的名字。


1. htop安装

        $ sudo apt-get install htop

2. htop用法

    ![htop screenshot](http://pic.yupoo.com/crazygit_v/ElYP0hQ6/medium.jpg)

    上面左上角显示CPU、内存、Swap使用情况，右边显示任务、负载、开机时间，下面就是进程实时状况。

3. 常用快捷键

    下面是 F1~F10 的功能和对应的字母快捷键。
    <table class="table table-striped table-bordered table-hover table-condensed">
    <tbody>
    <tr>
    <td>
        Shortcut Key
    </td>
    <td>
        Function Key
    </td>
    <td>
        Description
    </td>
    <td>
        中文说明
    </td>
    </tr>
    <tr>
    <td>
        h, ?
    </td>
    <td>
        F1
    </td>
    <td>
        Invoke htop Help
    </td>
    <td>
        查看htop使用说明
    </td>
    </tr>
    <tr>
    <td>
        S
    </td>
    <td>
        F2
    </td>
    <td>
        Htop Setup Menu
    </td>
    <td>
        htop 设定
    </td>
    </tr>
    <tr>
    <td>
        /
    </td>
    <td>
        F3
    </td>
    <td>
        Search for a Process
    </td>
    <td>
        搜索进程
    </td>
    </tr>
    <tr>
    <td>
        \
    </td>
    <td>
        F4
    </td>
    <td>
        Incremental process filtering
    </td>
    <td>
        增量进程过滤器
    </td>
    </tr>
    <tr>
    <td>
        t
    </td>
    <td>
        F5
    </td>
    <td>
        Tree View
    </td>
    <td>
        显示树形结构
    </td>
    </tr>
    <tr>
    <td>
        ,
    </td>
    <td>
        F6
    </td>
    <td>
        Sort by a column
    </td>
    <td>
        选择排序方式
    </td>
    </tr>
    <tr>
    <td>
        [
    </td>
    <td>
        F7
    </td>
    <td>
        Nice – (change priority)
    </td>
    <td>
        可减少nice值，这样就可以提高对应进程的优先级
    </td>
    </tr>
    <tr>
    <td>
        ]
    </td>
    <td>
        F8
    </td>
    <td>
        Nice + (change priority)
    </td>
    <td>
        可增加nice值，这样就可以降低对应进程的优先级
    </td>
    </tr>
    <tr>
    <td>
        k
    </td>
    <td>
        F9
    </td>
    <td>
        Kill a Process
    </td>
    <td>
        可对进程传递信号
    </td>
    </tr>
    <tr>
    <td>
        q
    </td>
    <td>
        F10
    </td>
    <td>
        Quit htop
    </td>
    <td>
        结束htop
    </td>
    </tr>
    </tbody>
    </table>


4. 命令行选项（COMMAND-LINE OPTIONS）

    <table class="table table-striped table-bordered table-hover table-condensed">
    <tbody>
    <tr>
    <td>
        -C –no-color
    </td>
    <td>
        使用一个单色的配色方案
    </td>
    </tr>
    <tr>
    <td>
        -d –delay=DELAY
    </td>
    <td>
        设置延迟更新时间，单位秒
    </td>
    </tr>
    <tr>
    <td>
        -h –help
    </td>
    <td>
        显示htop 命令帮助信息
    </td>
    </tr>
    <tr>
    <td>
        -u –user=USERNAME
    </td>
    <td>
        只显示一个给定的用户的过程
    </td>
    </tr>
    <tr>
    <td>
        -p –pid=PID,PID…
    </td>
    <td>
        只显示给定的PIDs
    </td>
    </tr>
    <tr>
    <td>
        -s –sort-key COLUMN
    </td>
    <td>
        依此列来排序
    </td>
    </tr>
    <tr>
    <td>
        -v –version
    </td>
    <td>
        显示版本信息
    </td>
    </tr>
    </tbody>
    </table>


5. 交互式命令（INTERACTIVE COMMANDS）

    <table class="table table-striped table-bordered table-hover table-condensed">
    <tbody>
    <tr>
    <td>
        上下键或PgUP, PgDn
    </td>
    <td>
        选定想要的进程，左右键或Home, End 移动字段，当然也可以直接用鼠标选定进程
    </td>
    </tr>
    <tr>
    <td>
        Space
    </td>
    <td>
        标记/取消标记一个进程。命令可以作用于多个进程，例如 “kill”，将应用于所有已标记的进程
    </td>
    </tr>
    <tr>
    <td>
        U
    </td>
    <td>
        取消标记所有进程
    </td>
    </tr>
    <tr>
    <td>
        s
    </td>
    <td>
        选择某一进程，按s:用strace追踪进程的系统调用
    </td>
    </tr>
    <tr>
    <td>
        l
    </td>
    <td>
        显示进程打开的文件: 如果安装了lsof，按此键可以显示进程所打开的文件
    </td>
    </tr>
    <tr>
    <td>
        I
    </td>
    <td>
        倒转排序顺序，如果排序是正序的，则反转成倒序的，反之亦然
    </td>
    </tr>
    <tr>
    <td>
        +, -
    </td>
    <td>
        在树形模式下，展开或折叠子树
    </td>
    </tr>
    <tr>
    <td>
        a (在有多处理器的机器上)
    </td>
    <td>
        设置 CPU affinity: 标记一个进程允许使用哪些CPU
    </td>
    </tr>
    <tr>
    <td>
        u
    </td>
    <td>
        显示特定用户进程
    </td>
    </tr>
    <tr>
    <td>
        M
    </td>
    <td>
        按Memory使用排序
    </td>
    </tr>
    <tr>
    <td>
        P
    </td>
    <td>
        按CPU使用排序
    </td>
    </tr>
    <tr>
    <td>
        T
    </td>
    <td>
        按Time+使用排序
    </td>
    </tr>
    <tr>
    <td>
        F
    </td>
    <td>
        跟踪进程: 如果排序顺序引起选定的进程在列表上到处移动，让选定条跟随该进程。这对监视一个进程非常有用：通过这种方式，你可以让一个进程在屏幕上一直可见。使用方向键会停止该功能
    </td>
    </tr>
    <tr>
    <td>
        K
    </td>
    <td>
        显示/隐藏内核线程
    </td>
    </tr>
    <tr>
    <td>
        H
    </td>
    <td>
        显示/隐藏用户线程
    </td>
    </tr>
    <tr>
    <td>
        Ctrl-L
    </td>
    <td>
        刷新
    </td>
    </tr>
    <tr>
    <td>
        Numbers
    </td>
    <td>
        PID 查找: 输入PID，光标将移动到相应的进程上
    </td>
    </tr>
    </tbody>
    </table>


6. 替代top

    用htop替换top，可添加别名，编辑`~/.bashrc`文件，添加如下代码

        alias top=htop
