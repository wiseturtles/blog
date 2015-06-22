Title: Install Nagios 4 on Ubuntu/Debian
Date: 2015-05-23
Category: Ubuntu
Tags: Ubuntu, Debian, Monitor, Management
Slug: install-nagios4-on-ubuntu-or-debian
Authors: Zhang Wanming
Summary: 在Ubuntu/Debian系统上部署Nagios 4

Ucloud后台监控系统功能很简单，最近发现之前设置过的监控项也无法正常显示，更不能编辑了。
虽然，马上就要将系统迁移到公司自己大家的云平台，但，最近Ucloud服务器压力很大，周末抽空先将Nagios搭建起来，让自己能及时收到报警。

我们Ucloud服务器都用的Debian 7 (wheezy)，源里只有nagios3，所以，自己编译、安装Nagios 4。

监控主机安装Nagios
====================

安装需要的软件包
-----------------

    :::bash

    $ sudo apt-get install build-essential libgd2-xpm-dev openssl libssl-dev apache2 php5 libapache2-mod-php5 apache2-utils postfix


创建用户、组
---------------

    :::bash

    $ sudo useradd nagios
    $ sudo groupadd nagcmd
    $ sudo usermod -a -G nagcmd nagios

安装nagios 4
---------------

    :::bash

    $ cd /data/software
    $ wget http://prdownloads.sourceforge.net/sourceforge/nagios/nagios-4.0.8.tar.gz
    $ tar zxf nagios-4.0.8.tar.gz
    $ cd nagios-4.0.8
    $ ./configure --with-nagios-group=nagios --with-command-group=nagcmd --with-mail=$(which sendmail)
    $ sudo make all
    $ sudo make install && make install-commandmode && make install-init && make install-config
    $ sudo ln -s /etc/init.d/nagios /etc/rcS.d/S99nagios # 开机自启动
    $ sudo service nagios restart


配置apache2

    :::bash

    $ sudo /usr/bin/install -c -m 644 sample-config/httpd.conf /etc/apache2/sites-available/nagios.conf
    $ sudo ln -s /etc/apache2/sites-available/nagios.conf /etc/apache2/sites-enabled/
    $ sudo a2enmod rewrite
    $ sudo a2enmod cgi
    $ sudo htpasswd -c /usr/local/nagios/etc/htpasswd.users nagiosadmin
    $ sudo service apache2 restart

浏览器访问 http://监控主机IP/nagios 查看监控情况, 登录用户名、密码就是 htpasswd 设置的。
nagios 4将被安装到 /usr/local/nagios 目录，该目录下的 etc 是配置文件夹。

安装nagios-plugins-2.0.3
--------------------------

    :::bash

    $ cd /data/software
    $ wget https://nagios-plugins.org/download/nagios-plugins-2.0.3.tar.gz
    $ tar zxf nagios-plugins-2.0.3.tar.gz
    $ cd nagios-plugins-2.0.3
    $ ./configure --with-nagios-user=nagios --with-nagios-group=nagios --with-openssl
    $ make all && make install


nagios-plugins 命令安装在 /usr/local/nagios/libexec 目录。


安装nagios-nrpe-2.15
----------------------

    :::bash

    $ cd /data/software
    $ wget -O nrpe-2.15.tar.gz "http://downloads.sourceforge.net/project/nagios/nrpe-2.x/nrpe-2.15/nrpe-2.15.tar.gz?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fnagios%2Ffiles%2Fnrpe-2.x%2Fnrpe-2.15%2F&ts=1432369927&use_mirror=liquidtelecom"
    $ tar zxf nrpe-2.15.tar.gz
    $ cd nrpe-2.15
    $ ./configure --with-nagios-user=nagios --with-nagios-group=nagios --with-ssl=/usr/bin/openssl --with-ssl-lib=/usr/lib/x86_64-linux-gnu 
    $ make all
    $ find -iname 'check_nrpe'
    $ sudo /usr/bin/install -c -m 755 ./src/check_nrpe /usr/local/nagios/libexec/


测试是否可以工作:

    :::bash

    $ /usr/local/nagios/libexec/check_nrpe -H 10.4.2.2 # 该IP是被监控主机的IP
    NRPE v2.13


被监控主机安装Nagios NRPE
==========================

安装nagios-plugins, nagios-nrpe-server

    :::bash
    $ sudo apt-get install nagios-plugins nagios-nrpe-server

配置nagios-nrpe-server，允许监控主机连接该被监控主机。

    :::bash
    $ sudo vim /etc/nagios/nrpe.cfg
    $ 将 监控主机IP 填入 allowed_hosts 字段，如: allowed_hosts=127.0.0.1,10.4.22.22
    $ sudo service nagios-nrpe-server restart


配置
=====

配置监控主机
-------------

/usr/local/nagios/etc/nagios.cfg

    :::bash
    $ diff -u nagios.cfg.back nagios.cfg
    --- nagios.cfg.back2015-05-23 11:07:51.436491931 +0800
    +++ nagios.cfg2015-05-23 22:08:09.872618927 +0800
    @@ -30,6 +30,9 @@
    cfg_file=/usr/local/nagios/etc/objects/contacts.cfg
    cfg_file=/usr/local/nagios/etc/objects/timeperiods.cfg
    cfg_file=/usr/local/nagios/etc/objects/templates.cfg
    +cfg_file=/usr/local/nagios/etc/objects/hosts.cfg
    +cfg_file=/usr/local/nagios/etc/objects/groups.cfg
    +cfg_file=/usr/local/nagios/etc/objects/services.cfg
        
    # Definitions for monitoring the local (Linux) host
    cfg_file=/usr/local/nagios/etc/objects/localhost.cfg
    @@ -1174,7 +1177,7 @@
    # using the $ADMINEMAIL$ and $ADMINPAGER$ macros in your notification
    # commands.
         
    -admin_email=nagios@localhost
    +admin_email=your-emai-address
    admin_pager=pagenagios@localhost


/usr/local/nagios/etc/objects/hosts.cfg

    :::bash

    $ # Define a host for the local machine
    ##############
    # appstore01 #
    ##############
    define host{
        use                             linux-server  ; Name of host template to use
                                        ; This host definition will inherit all variables that are defined
                                        ; in (or inherited by) the linux-server host template definition.
        host_name                       appstore01
        alias                           appstore01 on ucloud
        address                         10.4.2.2
        }

    ##############
    # appstore02 #
    ##############
    define host{
        use                             linux-server  ; Name of host template to use
                                        ; This host definition will inherit all variables that are defined
                                        ; in (or inherited by) the linux-server host template definition.
        host_name                       appstore02
        alias                           appstore02 on ucloud
        address                         10.4.2.22
        }

/usr/local/nagios/etc/objects/groups.cfg

    :::bash

    # Define an optional hostgroup for Linux machines
    define hostgroup{
        hostgroup_name  appstore-group ; The name of the hostgroup
        alias           appstore server group ; Long name of the group
        members         appstore01,appstore02     ; Comma separated list of hosts that belong to this group
        }

/etc/local/nagios/etc/objects/commands.cfg

    :::bash
    $ diff -u objects/commands.cfg.back objects/commands.cfg
    +########################
    +# add by zhang wanming #
    +########################
    +# 'check_mysql' command definition
    +define command{
    +   command_name    check_mysql
    +   command_line    $USER1$/check_mysql -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -d $ARG3$ -P 3306
    +   }
     
    +# 'check_http_with_url_port' command definition
    +define command{
    +        command_name    check_http_with_url_port
    +        command_line    $USER1$/check_http -I $HOSTADDRESS$ -u $ARG1$ -p $ARG2$
    +        }
    +
    +# 'check_nrpe' command definition
    +define command{
    +        command_name check_nrpe
    +        command_line $USER1$/check_nrpe -H $HOSTADDRESS$ -c $ARG1$
    +        }
    +
    +# 'check_memcached' command definition
    +define command{
    +        command_name check_memcached
    +        command_line $USER1$/check_tcp -H $HOSTADDRESS$ -p 11211 -t 5 -E -s 'stats\r\nquit\r\n' -e 'uptime' -M crit
    +        }


/etc/local/nagios/etc/objects/services.cfg

    :::bash

    $ cat objects/services.cfg 
    define service {
            use                             generic-service
            hostgroup_name                  appstore-group
            service_description             PING
            check_command                   check_ping!100.0,20%!500.0,60%
    }

    define service {
            use                             generic-service
            hostgroup_name                  appstore-group
            service_description             SSH
            check_command                   check_ssh!-p 1122
    }

    #################
    # HTTP services #
    #################
    define service {
            use                             generic-service
            hostgroup_name                  appstore-group
            service_description             Nginx
            check_command                   check_http
    }

    define service {
            use                             generic-service
            hostgroup_name                  appstore-group
            service_description             check http tdnaceweb
            check_command                   check_nrpe!check_http_tdanceweb
    }

    define service {
            use                             generic-service
            hostgroup_name                  appstore-group
            service_description             check http appstore
            check_command                   check_nrpe!check_http_appstore
    }

    define service {
            use                             generic-service
            hostgroup_name                  appstore-group
            service_description             check http launcher
            check_command                   check_nrpe!check_http_launcher
    }

    #########
    # Redis #
    #########
    define service {
            use                             generic-service
            hostgroup_name                  appstore-group
            service_description             Redis
            check_command                   check_nrpe!check_redis
    }

    #############
    # Memcached #
    #############
    define service {
            use                             generic-service
            hostgroup_name                  appstore-group
            service_description             Memcached
            check_command                   check_nrpe!check_memcached
    }

    #########
    # MySQL #
    #########
    define service {
            use                             generic-service
            host_name                       appstore01
            service_description             MySQL
            check_command                   check_nrpe!check_mysql
    }

    ################
    # disk/partion #
    ################
    define service {
            use                             generic-service
            hostgroup_name                  appstore-group
            service_description             check root disk
            check_command                   check_nrpe!check_disk_root
    }

    define service {
            use                             generic-service
            hostgroup_name                  appstore-group
            service_description             check root data
            check_command                   check_nrpe!check_disk_data
    }


配置被监控主机
---------------

    :::bash
    $ cat /etc/nagios/nrpe_local.cfg 
    ######################################
    # Do any local nrpe configuration here
    ######################################
    command[check_disk_root]=/usr/lib/nagios/plugins/check_disk -w 25% -c 10% -p /
    command[check_disk_data]=/usr/lib/nagios/plugins/check_disk -w 25% -c 10% -p /data
    command[check_redis]=/usr/lib/nagios/plugins/check_tcp -H localhost -p 6379 -t 5 -E -s 'info\r\n' -q 'quit\r\n' -e 'uptime_in_days' -M crit
    command[check_memcached]=/usr/lib/nagios/plugins/check_tcp -H localhost -p 11211 -t 5 -E -s 'stats\r\nquit\r\n' -e 'uptime' -M crit
    command[check_mysql]=/usr/lib/nagios/plugins/check_mysql -H localhost -u user -p passwd -d your-database
    command[check_http_tdanceweb]=/usr/lib/nagios/plugins/check_http -H localhost -p 6688 -t 3
    command[check_http_appstore]=/usr/lib/nagios/plugins/check_http -H localhost -p 8888 -t 3 -u /m3/subjects
    command[check_http_launcher]=/usr/lib/nagios/plugins/check_http -H localhost -p 9999 -t 3


配置过程中碰到的问题
=====================

监控服务器上没有check_nrpe命令
---------------------------

如果没有安装nrpe，请下载、编译、安装，请参考 安装nagios-nrpe-2.15


CHECK_NRPE: Error - Could not complete SSL handshake.
-------------------------------------------------------

编辑/etc/nagios/nrpe.cfg, 确定 allowed_hosts 中加入监控主机IP，多个IP以 "," 分隔。
如: allowed_hosts=127.0.0.1,10.4.13.14

然后，重新加载 nagios-nrpe-server 配置文件，如下：

    :::bash

    $ service nagios-nrpe-server reload


下次再学习并补充联系人及报警相关设置。


参考：

1. <https://www.digitalocean.com/community/tutorials/how-to-install-nagios-4-and-monitor-your-servers-on-ubuntu-14-04>
2. <http://netkiller.github.io/monitoring/nagios/>
