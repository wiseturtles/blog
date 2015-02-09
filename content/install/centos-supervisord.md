Title: CentOS上安装Supervisor
Date: 2015-02-09 23:49
Tags: centos, supervisor
Slug: centos-supervisor
Author: crazygit
Summary: CentOS上安装Supervisor


## 安装
部署项目从Ubuntu转战到CentOS, 使用yum命令安装supervisor后，发现无法正常使用，因此只有使用pip安装.

    :::bash
    $ sudo pip install supervisor


## 配置supervisor

1. 添加配置文件

        :::bash
        $ sudo mkdir /etc/supervisor
        $ sudo mkdir /etc/supervisor/conf.d
        # 添加如下配置文件
        $ cat /etc/supervisor/supervisord.conf
        [unix_http_server]
        file=/var/tmp/supervisor.sock    ; (the path to the socket file)
        chmod=0700                       ; sockef file mode (default 0700)

        ; the below section must remain in the config file for RPC
        ; (supervisorctl/web interface) to work, additional interfaces may be
        ; added by defining them in separate rpcinterface: sections
        [rpcinterface:supervisor]
        supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface


        [supervisord]
        http_port=/var/run/supervisor.sock ; (default is to run a UNIX domain socket server)
        ;http_port=127.0.0.1:9001  ; (alternately, ip_address:port specifies AF_INET)
        ;sockchmod=0700              ; AF_UNIX socketmode (AF_INET ignore, default 0700)
        ;sockchown=nobody.nogroup     ; AF_UNIX socket uid.gid owner (AF_INET ignores)
        ;umask=022                   ; (process file creation umask;default 022)
        logfile=/data/log/supervisor/supervisord.log ; (main log file;default $CWD/supervisord.log)
        logfile_maxbytes=50MB       ; (max main logfile bytes b4 rotation;default 50MB)
        logfile_backups=10          ; (num of main logfile rotation backups;default 10)
        loglevel=debug              ; (logging level;default info; others: debug,warn)
        pidfile=/var/run/supervisord.pid ; (supervisord pidfile;default supervisord.pid)
        nodaemon=false              ; (start in foreground if true;default false)
        minfds=1024                 ; (min. avail startup file descriptors;default 1024)
        minprocs=200                ; (min. avail process descriptors;default 200)
        childlogdir=/data/log/supervisor ; ('AUTO' child log dir, default $TEMP)

        ;nocleanup=true              ; (don't clean up tempfiles at start;default false)
        ;http_username=user          ; (default is no username (open system))
        ;http_password=123           ; (default is no password (open system))
        ;user=chrism                 ; (default is current user, required if root)
        ;directory=/tmp              ; (default is not to cd during start)
        ;environment=KEY=value       ; (key value pairs to add to environment)

        [supervisorctl]
        serverurl=unix:///var/tmp/supervisor.sock ; use a unix:// URL  for a unix socket
        ;serverurl=http://127.0.0.1:9001 ; use an http:// url to specify an inet socket
        ;username=chris              ; should be same as http_username if set
        ;password=123                ; should be same as http_password if set
        ;prompt=mysupervisor         ; cmd line prompt (default "supervisor")

        ; The below sample program section shows all possible program subsection values,
        ; create one or more 'real' program: sections to be able to control them under
        ; supervisor.

        ;[program:theprogramname]
        ;command=/bin/cat            ; the program (relative uses PATH, can take args)
        ;priority=999                ; the relative start priority (default 999)
        ;autostart=true              ; start at supervisord start (default: true)
        ;autorestart=true            ; retstart at unexpected quit (default: true)
        ;startsecs=10                ; number of secs prog must stay running (def. 10)
        ;startretries=3              ; max # of serial start failures (default 3)
        ;exitcodes=0,2               ; 'expected' exit codes for process (default 0,2)
        ;stopsignal=QUIT             ; signal used to kill process (default TERM)
        ;stopwaitsecs=10             ; max num secs to wait before SIGKILL (default 10)
        ;user=chrism                 ; setuid to this UNIX account to run the program
        ;log_stdout=true             ; if true, log program stdout (default true)
        ;log_stderr=true             ; if true, log program stderr (def false)
        ;logfile=/var/log/cat.log    ; child log path, use NONE for none; default AUTO
        ;logfile_maxbytes=1MB        ; max # logfile bytes b4 rotation (default 50MB)
        ;logfile_backups=10          ; # of logfile backups (default 10)


        [include]
        files = /etc/supervisor/conf.d/*.conf


项目的配置文件写入 /etc/supervisor/conf.d/目录即可


## 添加开机启动

    :::bash
    # 添加如下配置文件
    $ cat /etc/init.d/supervisord

    #!/bin/bash
    #
    # /etc/rc.d/init.d/supervisord
    #
    # Supervisor is a client/server system that
    # allows its users to monitor and control a
    # number of processes on UNIX-like operating
    # systems.
    #
    # chkconfig: - 64 36
    # description: Supervisor Server
    # processname: supervisord

    # Source init functions
    . /etc/rc.d/init.d/functions

    prog="supervisord"

    prefix="/usr"
    exec_prefix="${prefix}"
    prog_bin="${exec_prefix}/bin/supervisord"
    PIDFILE="/var/run/$prog.pid"
    DAEMON_OPTS="-c /etc/supervisor/supervisord.conf $DAEMON_OPTS"

    start()
    {
        echo -n $"Starting $prog: "
        daemon $prog_bin $DAEMON_OPTS --pidfile $PIDFILE
        [ -f $PIDFILE ] && success $"$prog startup" || failure $"$prog startup"
        echo
    }

    stop()
    {
        echo -n $"Shutting down $prog: "
        [ -f $PIDFILE ] && killproc $prog || success $"$prog shutdown"
        echo
    }

    case "$1" in

    start)
    start
    ;;

    stop)
    stop
    ;;

    status)
        status $prog
    ;;

    restart)
    stop
    start
    ;;

    *)
    echo "Usage: $0 {start|stop|restart|status}"
    ;;

    esac


设置如下:

    :::bash
    $ sudo chmod +x /etc/init.d/supervisord
    $ sudo chkconfig --add supervisord
    $ sudo chkconfig supervisord on
    $ sudo service supervisord start
