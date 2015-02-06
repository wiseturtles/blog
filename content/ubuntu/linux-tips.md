Title: linux 小贴士
Date: 2015-01-20 18:16
Tags: linux, tips
Slug: linux-tips
Author: crazygit
Summary: the tips of use linux


## ssh端口转发

由于服务器上一些服务的端口没有对外开发，但是在开发时又想直接使用服务器上的这些服务，该怎么办？


以我们服务器A(192.167.0.1) 为例, 上面有Elasticsheach数据库为例, 由于Elasticsearch数据库比较
大，从服务器上将数据拷贝到本地不太现实，便可以通过ssh端口转发来实现。

前提: 本地服务器可以通过ssh登陆到服务器A(192.167.0.1)

    :::bash
    $ ssh -fNL 9200:localhost:9200 192.167.0.1

通过上面命令可以在本地机器和服务器A的9200端口之间做一个隧道，访问本地的9200端
口就跟直接访问服务器A上的9200端口一样。

为了使用方便，可以为上面的命令设置一个别名,添加到`~/.bashrc`中， 如

    :::bash
    $ alias sshes="ssh -fNL 9200:localhost:9200 192.167.0.1"

那么以后使用`sshes`就可以方便的建立一个ssh隧道连接,　同理，此法可用于连接服务器上的mysql及其它服务.


另外一个常用的是通过ssh翻墙的命令

    :::bash
    $ ssh -qTfnN -D 7070 192.167.0.2

前提是172.167.0.2是一台可以直接翻墙的机器(如国外的云主机),执行上面的命令后便可以通过本地的7070端口翻墙.

更多关于ssh转发的可以查看下面的文章:

* [三种不同类型的ssh隧道](http://codelife.me/blog/2012/12/09/three-types-of-ssh-turneling/)


## ssh登陆配置

登陆到远程服务器时,当服务器上的用户名和本地的用户名不一致且端口也不是默认端口时.
以服务器A(192.168.0.1), 用户名为root, 端口为4455。我们每次登陆到远程主机或拷贝
文件时, 都需要带上用户名和端口信息。如:

    :::bash
    # ssh登陆
    $ ssh -p 4455 root@192.168.0.1
    # scp拷贝
    $ scp -P 4455 root@192.168.0.1:/tmp/a a

这样比较繁琐。稍微配置一下便可以化繁为简

    :::bash
    $ cat ~/.ssh/config
    Host 192.168.0.1
        User root
        Port 4455

这样以后每次访问该服务器都不需要带上用户及端口信息

    :::bash
    # ssh登陆
    $ ssh 192.168.0.1
    # scp拷贝
    $ scp -P 192.168.0.1:/tmp/a a

当本机需要通过不同的key登陆到不同的服务器时，我们都是通过`-i`来临时指定key.

    :::bash
    # 使用a.key登陆192.168.0.1
    $ ssh -i ~/.ssh/a.key 192.168.0.1
    # 使用b.key登陆192.168.0.2
    $ ssh -i ~/.ssh/b.key 192.168.0.2

稍微配置一下

    :::bash
    $ cat ~/.ssh/config
    Host 192.168.0.1
        User root
        Port 4455
        IdentityFile ~/.ssh/a.key

    Host 192.168.0.2
        User root
        Port 4455
        IdentityFile ~/.ssh/b.key

配置之后每次登陆不同的服务器也不需要通过`-i`参数指定key了。



## ~/.bashrc配置

下面介绍的都是可以添加到`~/.bashrc`中的一些配置.

### 让man page不再单调

平时使用man page的时候，都是黑白的文字。看起来很是不方便，稍微配置一下，可以让
你的man page充满颜色。

    :::bash
    # color man pages
    export LESS_TERMCAP_mb=$'\E[01;31m'
    export LESS_TERMCAP_md=$'\E[01;31m'
    export LESS_TERMCAP_me=$'\E[0m'
    export LESS_TERMCAP_se=$'\E[0m'
    export LESS_TERMCAP_so=$'\E[01;44;33m'
    export LESS_TERMCAP_ue=$'\E[0m'
    export LESS_TERMCAP_us=$'\E[01;32m'

`source ~/.bashrc`后，man一个命令可以看到效果


### 终端操作使用vim模式

从`@WanMing`处习得的技能，vim控必备

    :::bash
    set -o vi

效果如何，谁用谁知道

### python自动激活项目的虚拟环境

重写`cd`命令，使它在进入到python项目时，自动激活与项目名一样的虚拟环境

    :::bash
    function workon_cwd {
        # Check that this is a Git repo
        GIT_DIR=`git rev-parse --git-dir 2> /dev/null`
        if [ $? == 0 ]; then
            # Find the repo root and check for virtualenv name override
            GIT_DIR=`\cd $GIT_DIR; pwd`
            PROJECT_ROOT=`dirname "$GIT_DIR"`
            ENV_NAME=`basename "$PROJECT_ROOT"`
            if [ -f "$PROJECT_ROOT/.venv" ]; then
                ENV_NAME=`cat "$PROJECT_ROOT/.venv"`
            fi
            # Activate the environment only if it is not already active
            if [ "$VIRTUAL_ENV" != "$WORKON_HOME/$ENV_NAME" ]; then
                if [ -e "$WORKON_HOME/$ENV_NAME/bin/activate" ]; then
                    workon "$ENV_NAME" && export CD_VIRTUAL_ENV="$ENV_NAME"
                fi
            fi
        elif [ $CD_VIRTUAL_ENV ]; then
            # We've just left the repo, deactivate the environment
            # Note: this only happens if the virtualenv was activated automatically
            deactivate && unset CD_VIRTUAL_ENV
        fi
    }

    # New cd function that does the virtualenv magic
    function venv_cd {
        cd "$@" && workon_cwd
    }

    alias cd="venv_cd"
    # init for create new terminal tab
    workon_cwd

### 个性化终端提示符

通过设置PS1变量, 可以个性化终端提示符, 展示更多有用信息.

如我的终端设置, 里面包含了项目的分支，当前HEAD值，及git库的状态信息

![PS1 screenshot](http://pic.yupoo.com/crazygit_v/En4dALxz/medium.jpg)


    :::bash
    PS1="${TITLEBAR}
    ${SAVE_CURSOR}${MOVE_CURSOR_RIGHTMOST}${MOVE_CURSOR_5_LEFT}\
    ${RESTORE_CURSOR}\
    ${VIRTUALENV:+($VIRTUALENV)}${D_USER_COLOR}\u ${D_INTERMEDIATE_COLOR}\
    at ${D_MACHINE_COLOR}\h ${D_INTERMEDIATE_COLOR}\
    in ${D_DIR_COLOR}\w ${D_INTERMEDIATE_COLOR}\
    $(demula_vcprompt)\
    $(is_vim_shell)

如下是一个在线生成PS1变量的网站，可以根据自己的需求定制PS1变量:

<http://bashrcgenerator.com/>
