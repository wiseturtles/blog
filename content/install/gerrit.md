Title: Gerrit搭建指南
Date: 2015-01-15 17:09
Tags: git, gerrit
Slug: gerrit
Author: crazygit
Summary: install guide of gerrit

## 什么是Gerrit

Gerrit，一种免费、开放源代码的代码审查软件，使用网页界面。利用网页浏览器，同一个团队的软件程序员，可以相互审阅彼此修改后的程序代码，决定是否能够提交，退回或者继续修改。它使用Git作为底层版本控制系统。

本文以Ubuntu 12.04，Gerrit2.9.4(目前最新的版本)为例介绍整个搭建过程

## 参考文献

* <https://gerrit-documentation.storage.googleapis.com/Documentation/2.9.4/install.html>

## 环境要求

* JDK 1.7+

## 前期准备

1. 安装JDK1.7

        :::bash
        $ sudo add-apt-repository ppa:webupd8team/java
        $ sudo apt-get update
        $ sudo apt-get install oracle-java7-installer

2. 安装Git

        $ sudo apt-get install git

3. 安装Nginx服务器, 用于作为Gerrit网站的反向代理以及HTTP认证

        $ sudo apt-get install nginx


## 数据库设置

Gerrit的使用必须依赖于数据库，目前支持的数据库有H2(Gerrit内置的), PostgreSQL, MySQL, Oracle.

本文以MySQL为例，介绍数据库的设置。

    :::bash
    # 安装数据库
    $ sudo apt-get install mysql-server

    # 创建数据库reviewdb和用户gerrit2为后面做准备
    # 数据库名和用户名可以根据实际的使用情况自己选择
    mysql> CREATE USER 'gerrit2'@'localhost' IDENTIFIED BY 'secret';
    mysql> CREATE DATABASE reviewdb;
    mysql> GRANT ALL ON reviewdb.* TO 'gerrit2'@'localhost';
    mysql> FLUSH PRIVILEGES;

## 初始化Gerrit站点

由于Gerrit创建中需要保存自己的SSH Keys, 配置文件，代码库等信息，因此强烈建议单独创建一个用户来创建Gerrit站点。

    :::bash
    # 在系统上添加用户gerrit2
    $ sudo adduser gerrit2
    # 切换到当前用户
    $ sudo su gerrit2
    # 下载gerrit安装包
    $ wget http://gerrit-releases.storage.googleapis.com/gerrit-2.9.4.war
    # -d 指定站点的根目录, 本例以gerrit2 HOME目录下的gerrit为例
    $ java -jar gerrit-2.9.4.war init -d gerrit

    *** Gerrit Code Review 2.9.4
    ***

    Create '/home/gerrit2/gerrit'  [Y/n]?

    *** Git Repositories
    ***
    # 项目代码目录设置
    Location of Git repositories   [git]:

    *** SQL Database
    ***

    Database server type           [h2]: mysql

    Gerrit Code Review is not shipped with MySQL Connector/J 5.1.21
    **  This library is required for your configuration. **
    Download and install it now [Y/n]?
    Downloading http://repo2.maven.org/maven2/mysql/mysql-connector-java/5.1.21/mysql-connector-java-5.1.21.jar ... OK
    Checksum mysql-connector-java-5.1.21.jar OK
    Server hostname                [localhost]:           # 此处填写刚刚创建数据库时设置的信息
    Server port                    [(mysql default)]:
    Database name                  [reviewdb]:
    Database username              [gerrit2]:
    gerrit2's password             :
                confirm password :

    *** Index
    ***

    Type                           [LUCENE/?]:

    *** User Authentication
    ***

    # 认证方式设置, 根据实际情况自行选择，不清楚有哪些方式可以输入"?"查看
    Authentication method          [OPENID/?]: http
    Get username from custom HTTP header [y/N]?
    SSO logout URL                 :

    *** Review Labels
    ***

    Install Verified label         [y/N]?

    *** Email Delivery
    ***

    # 邮件服务器设置, 根据实际情况自行选择
    SMTP server hostname           [localhost]:
    SMTP server port               [(default)]:
    SMTP encryption                [NONE/?]:
    SMTP username                  :

    *** Container Process
    ***

    Run as                         [gerrit2]:
    Java runtime                   [/usr/lib/jvm/java-7-oracle/jre]:
    Copy gerrit-2.9.4.war to /home/gerrit2/gerrit/bin/gerrit.war [Y/n]?
    Copying gerrit-2.9.4.war to /home/gerrit2/gerrit/bin/gerrit.war

    *** SSH Daemon
    ***

    Listen on address              [*]:
    Listen on port                 [29418]:

    Gerrit Code Review is not shipped with Bouncy Castle Crypto SSL v149
    If available, Gerrit can take advantage of features
    in the library, but will also function without it.
    Download and install it now [Y/n]?
    Downloading http://www.bouncycastle.org/download/bcpkix-jdk15on-149.jar ... OK
    Checksum bcpkix-jdk15on-149.jar OK

    Gerrit Code Review is not shipped with Bouncy Castle Crypto Provider v149
    ** This library is required by Bouncy Castle Crypto SSL v149. **
    Download and install it now [Y/n]?
    Downloading http://www.bouncycastle.org/download/bcprov-jdk15on-149.jar ... OK
    Checksum bcprov-jdk15on-149.jar OK
    Generating SSH host key ... rsa... dsa... done

    *** HTTP Daemon
    ***

    # 启用反向代理
    Behind reverse proxy           [y/N]? y
    Proxy uses SSL (https://)      [y/N]?
    Subdirectory on proxy server   [/]:
    Listen on address              [*]:
    Listen on port                 [8081]:     # 设置gerrit网站监听端口
    Canonical URL                  [http://localhost/]:

    *** Plugins
    ***

    Install plugin commit-message-length-validator version v2.9.4 [y/N]?
    Install plugin download-commands version v2.9.4 [y/N]?
    Install plugin replication version v2.9.4 [y/N]?
    Install plugin reviewnotes version v2.9.4 [y/N]?
    Install plugin singleusergroup version v2.9.4 [y/N]?

    Initialized /home/gerrit2/gerrit
    Executing /home/gerrit2/gerrit/bin/gerrit.sh start
    Starting Gerrit Code Review: OK
    Waiting for server on localhost:80 ... OK
    Opening http://localhost/#/admin/projects/ ...No protocol specified
    No protocol specified
    OK

## 配置nginx反向代理

在nginx配置中间中配置如下:

<pre>
      location / {
            proxy_pass        http://localhost:8081;
            proxy_set_header  X-Forwarded-For $remote_addr;
            proxy_set_header  Host $host;
            auth_basic "Restricted";  # 配置访问限制和密码文件
            auth_basic_user_file  /home/gerrit2/gerrit/etc/auth_passwd;

    }
</pre>


创建用户密码文件

    :::bash
    # 创建用户名和密码都是admin的文件
    $ htpasswd -b -c /home/gerrit2/gerrit/etc/auth_passwd admin admin

## 测试

访问<http://localhost/>输入用户名和密码即可登陆到Gerrit


## Gerrit目录结构

    :::bash
    $ tree -L 1 gerrit
    gerrit
    ├── bin
    ├── cache
    ├── data
    ├── etc  # 配置信息, 创建站点时的配置信息都保存在这里，可以按照需要修改
    ├── git
    ├── index
    ├── lib
    ├── logs
    ├── plugins
    ├── static
    └── tmp


## 常用命令

    :::bash
    $ gerrit/bin/gerrit.sh start  # 启动gerrit服务
    $ gerrit/bin/gerrit.sh stop   # 关闭gerrit服务
    $ gerrit/bin/gerrit.sh restart # 重启gerrit服务

## 更多信息

关于gerrit主题设置，使用方法等更多信息，官方文档上已有详细描述, 请参考:

<https://gerrit-documentation.storage.googleapis.com/Documentation/2.9.4/index.html>

## 更新

_最近因工作需要，又重新搭建了一次gerrit, 遇到一些坑, 记录一下_.

1. 如果用MySQL作为数据库，Gerrit数据库的引擎应该是Innodb.
2. 配置邮件时，一直认证失败，除了在`etc/gerrt.conf`文件里指定`sendmail.smtpUser`, 还需要指定`sendmail.from`为发送邮件的用户信息, 格式为`username <youmail@mail.com>`
3. 认证可以使用github oauth认证[gerrit-oauth-provider](https://github.com/davido/gerrit-oauth-provider)

