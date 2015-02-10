Title: OpenResty
Date: 2015-02-06 15:45
Tags: nginx, openresty
Slug: openresty-install
Author: crazygit
Summary: OpenResty安装及常用配置

## 什么是OpenResty

OpenResty（也称为 ngx_openresty）是一个全功能的 Web 应用服务器，它打包了标准
的Nginx 核心，很多的常用的第三方模块，以及它们的大多数依赖项。对于经常需要使用
nginx第三方模块的人来说，是一个非常不错的选择.


## 下载及安装

关于如何下载及安装OpenResty, [官网](http://openresty.org/cn/)已经有很详细的介
绍，不再赘述。


## 添加开机启动脚本

1. 创建如下文件:

        :::bash
        $ cat /etc/init.d/nginx

        #!/bin/bash
        #
        # chkconfig: 2345 55 25
        # Description: Nginx init.d script, put in /etc/init.d, chmod +x /etc/init.d/nginx
        #              For Debian, run: update-rc.d -f nginx defaults
        #              For CentOS, run: chkconfig --add nginx
        #
        ### BEGIN INIT INFO
        # Provides:          nginx
        # Required-Start:    $all
        # Required-Stop:     $all
        # Default-Start:     2 3 4 5
        # Default-Stop:      0 1 6
        # Short-Description: nginx init.d script
        # Description:       OpenResty (aka. ngx_openresty) is a full-fledged web application server by bundling the standard Nginx core,
        #                    lots of 3rd-party Nginx modules, as well as most of their external dependencies.
        ### END INIT INFO
        #

        PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
        DESC="Nginx Daemon"
        NAME=nginx
        PREFIX=/etc/openresty/nginx
        DAEMON=$PREFIX/sbin/$NAME
        CONF=$PREFIX/conf/$NAME.conf
        PID=$PREFIX/logs/$NAME.pid
        SCRIPT=/etc/init.d/$NAME

        if [ ! -x "$DAEMON" ] || [ ! -f "$CONF" ]; then
            echo -e "\033[33m $DAEMON has no permission to run. \033[0m"
            echo -e "\033[33m Or $CONF doesn't exist. \033[0m"
            sleep 1
            exit 1
        fi

        do_start() {
            if [ -f $PID ]; then
                echo -e "\033[33m $PID already exists. \033[0m"
                echo -e "\033[33m $DESC is already running or crashed. \033[0m"
                echo -e "\033[32m $DESC Reopening $CONF ... \033[0m"
                $DAEMON -s reopen -c $CONF
                sleep 1
                echo -e "\033[36m $DESC reopened. \033[0m"
            else
                echo -e "\033[32m $DESC Starting $CONF ... \033[0m"
                $DAEMON -c $CONF
                sleep 1
                echo -e "\033[36m $DESC started. \033[0m"
            fi
        }

        do_stop() {
            if [ ! -f $PID ]; then
                echo -e "\033[33m $PID doesn't exist. \033[0m"
                echo -e "\033[33m $DESC isn't running. \033[0m"
            else
                echo -e "\033[32m $DESC Stopping $CONF ... \033[0m"
                $DAEMON -s stop -c $CONF
                sleep 1
                echo -e "\033[36m $DESC stopped. \033[0m"
            fi
        }

        do_reload() {
            if [ ! -f $PID ]; then
                echo -e "\033[33m $PID doesn't exist. \033[0m"
                echo -e "\033[33m $DESC isn't running. \033[0m"
                echo -e "\033[32m $DESC Starting $CONF ... \033[0m"
                $DAEMON -c $CONF
                sleep 1
                echo -e "\033[36m $DESC started. \033[0m"
            else
                echo -e "\033[32m $DESC Reloading $CONF ... \033[0m"
                $DAEMON -s reload -c $CONF
                sleep 1
                echo -e "\033[36m $DESC reloaded. \033[0m"
            fi
        }

        do_quit() {
            if [ ! -f $PID ]; then
                echo -e "\033[33m $PID doesn't exist. \033[0m"
                echo -e "\033[33m $DESC isn't running. \033[0m"
            else
                echo -e "\033[32m $DESC Quitting $CONF ... \033[0m"
                $DAEMON -s quit -c $CONF
                sleep 1
                echo -e "\033[36m $DESC quitted. \033[0m"
            fi
        }

        do_test() {
            echo -e "\033[32m $DESC Testing $CONF ... \033[0m"
            $DAEMON -t -c $CONF
        }

        do_info() {
            $DAEMON -V
        }

        case "$1" in
        start)
        do_start
        ;;
        stop)
        do_stop
        ;;
        reload)
        do_reload
        ;;
        restart)
        do_stop
        do_start
        ;;
        quit)
        do_quit
        ;;
        test)
        do_test
        ;;
        info)
        do_info
        ;;
        *)
        echo "Usage: $SCRIPT {start|stop|reload|restart|quit|test|info}"
        exit 2
        ;;
        esac

        exit 0

2. 给文件设置执行权限`chmod +x /etc/init.d/nginx`
3. 添加到开机启动

    * CentOS系统

            :::bash
            chkconfig --list nginx   # 列出系统nginx服务启动情况
            chkconfig --add nginx    # 添加nginx服务
            chkconfig --level 35 nginx on # 设定nginx在等级3和5为开机运行服务，--level 35表示操作只在等级3和5执行，on表示启动，off表示关闭

    * Debian系统

            :::bash
            sudo update-rc.d -f nginx remove  # 删除nginx服务
            sudo update-rc.d apache2 defaults # 添加nginx服务


## 使用logrotate切割日志

创建如下文件

    :::bash
    $ cat /etc/logrotate.d/nginx
    /etc/openresty/nginx/logs/*.log {
        daily
        missingok
        rotate 52
        dateext
        dateformat  -%Y-%m-%d
        compress
        delaycompress
        notifempty
        create 0640 www-data adm
        sharedscripts
        postrotate
            [ ! -f /etc/openresty/nginx/logs/nginx.pid ] || kill -USR1 `cat /etc/openresty/nginx/logs/nginx.pid`
        endscript
    }


注释：

* `/etc/openresty/nginx/logs/*.log` 为OpenResty的log目录
* daily：每天轮询
* missingok: 如果日志丢失，不报错继续滚动下一个日志
* rotate 52：保留最多52次滚动的日志
* dateext：日期扩展
* dateformat: 日期格式
* compress：旧日志默认用gzip压缩
* notifempty:当日志为空时不进行滚动
* create: mode owner group 转储文件，使用指定的文件模式创建新的日志文件
* /etc/openresty/nginx/logs/nginx.pid：nginx主进程pid

测试:

    :::bash
    $ logroate -f /etc/logrotate.d/nginx
