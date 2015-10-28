Title: OpenGrok安装使用指南
Date: 2012-12-14 18:09
Tags: opengrok
Slug: setup-opengrok
Author: crazygit
Summary: how to set up OpenGrok
comments: true


本文主要参考了下面的文章:

* <http://hub.opensolaris.org/bin/view/Project+opengrok/installdescription>
* <http://src.opensolaris.org/source/xref/opengrok/trunk/README.txt>

注意：最好是单独建立一个用户，并保证该用户对代码和后面创建索引的目录读写权限

## 准备工作

以opengrok用户身份登录安装jdk和Exuberant Ctags.

    $ sudo apt-get install sun-java6-jdk ctags

获取opengrok安装包（opengrok-0.11.1.tar.gz）和tomcat安装包(apachetomcat-7.0.6.tar.gz)解压安装包到任意目录下面

    $ cd /var/local/
    $ tar -zxvf /path/to/opengrok-0.11.1.tar.gz
    $ tar -zxvf /path/to/apachetomcat-7.0.6.tar.gz

下载需要使用的代码到一个目录下面

    $ mkdir -p ~/opengrok/projects/project1
    $ mkdir -p ~/opnegrok/projects/project2
    $ cd ~/opengrok/projects/project1
    $ download code of project1 (such as: git clone ... or repo init ... && repo sync)
    $ cd ~/opengrok/projects/project2
    $ download code of project2 (such as: git clone ... or repo init ... && repo sync)

目录结构如下:

<pre>
opengrok/projects----project1
            |----project2
            |----project3
            |----.......
</pre>

启动tomcat，确认tomcat没有问题

    $ /var/local/apache-tomcat-7.0.6/bin/startup.sh

访问<http://127.0.0.1:8080>检查tomcat 是否正常工作

##  部署OpenGrok

执行命令

    $ sudo OPENGROK_TOMCAT_BASE=/var/local/apache-tomcat-7.0.6 /var/local/opengrok-0.11.1/bin/OpenGrok deploy

这一步实际操作是`/var/local/opengrok-0.11.1/lib/source.war`部署到`/var/local/apache-tomcat-7.0.6/webapps/`
访问
<http://127.0.0.1:8080/source>
已经可以看到opengrok页面了，但是没有项目的数据信息。
在`/var/local/apache-tomcat-7.0.6/webapps/`目录下面可以看到一个source目录和source.war，就是刚刚部属的产物。
source.war已经没有什么用了，可以删除。

###  创建索引

 创建索引时，会创建三个目录，一个data目录来存放索引信息，一个etc目录创建配置信息和一个log目录。
 如想让~/opengrok/来存放索引,则指定`OPENGROK_INSTANCE_BASE=~/opengrok`, 则指定`OPENGROK_INSTANCE_BASE=~/opengrok`

    $ OPENGROK_VERBOSE=true OPENGROK_INSTANCE_BASE=~/opengrok/ ./OpenGrok index ~/opengrok/projects/

 这一步命令的执行时间视~/opengrok/projects/的代码数量决定。 最后会在~/opengrok 目录下面看到data,etc,log 三个目录

访问<http://127.0.0.1:8080/source>,enjoy it!


###  项目代码更新或者添加新的项目

首先更新项目代码或者下载新的项目到~/opengrok/projects目录下面。
然后重新执行

    $ OPENGROK_VERBOSE=true OPENGROK_INSTANCE_BASE=~/opengrok/ ./OpenGrok index ~/opengrok/projects/

命令即可。


###  可选操作

可以通过修改`/var/local/apache-tomcat-7.0.6/webapps/source/index_body.html`来定制化你的OpenGrok首页。
如添加公司LOGO或一些有用的帮助信息。

###  直接调用命令行接口
上面创建索引的命令其实

    $ OPENGROK_VERBOSE=true OPENGROK_INSTANCE_BASE=~/opengrok/ ./OpenGrok index ~/opengrok/projects/

其实调用的是opengrok lib目录下的jar包：

    java -Xmx2048m -Dorg.opensolaris.opengrok.history.cvs=/usr/bin/cvs
    -Dorg.opensolaris.opengrok.history.git=/usr/bin/git
    -Djava.util.logging.config.file=/data/opengrok/opengrok_data/logging.properties
    -jar /data/opengrok/opengrok-0.11.1/bin/../lib/opengrok.jar
    -P -S -r on -v -c /usr/bin/ctags-exuberant -a on
    -W /data/opengrok/opengrok_data/etc/configuration.xml
    -U localhost:2424 -s /data/opengrok/projects/
    -d /data/opengrok/opengrok_data/data -H..

上面各个参数的意思如下:

    $ java -jar opengrok.jar

    Usage: opengrok.jar [options]
    -?
        Help

    -A ext:analyzer
        Files with the named extension should be analyzed with the specified class

    -a on/off
        Allow or disallow leading wildcards in a search

    -B url
        Base URL of the user Information provider. Default: "http://www.opensolaris.org/viewProfile.jspa?username="

    -C
        Print per project percentage progress information(I/O extensive, since one read through dir structure is made before indexing, needs -v, otherwise it just goes to the log)

    -c /path/to/ctags
        Path to Exuberant Ctags from http://ctags.sf.net by default takes the Exuberant Ctags in PATH.

    -D
        Store history cache in a database (needs the JDBC driver in the classpath, typically derbyclient.jar or derby.jar)

    -d /path/to/data/root
        The directory where OpenGrok stores the generated data

    -e
        Economical - consumes less disk space. It does not generate hyper text cross reference files offline, but will do so on demand - which could be sightly slow.

    -H
        Generate history cache for all repositories

    -h /path/to/repository
        just generate history cache for the specified repos (absolute path from source root)

    -I pattern
        Only files matching this pattern will be examined (supports wildcards, example: -I *.java -I *.c)

    -i pattern
        Ignore the named files or directories (supports wildcards, example: -i *.so -i *.dll)

    -j class
        Name of the JDBC driver class used by the history cache. Can use one of the shorthands "client" (org.apache.derby.jdbc.ClientDriver) or "embedded" (org.apache.derby.jdbc.EmbeddedDriver). Default: "client"

    -k /path/to/repository
        Kill the history cache for the given repository and exit. Use '*' to delete the cache for all repositories.

    -K
        List all repository pathes and exit.

    -L path
        Path to the subdirectory in the web-application containing the requested stylesheet. The following factory-defaults exist: "default", "offwhite" and "polished"

    -l on/off
        Turn on/off locking of the Lucene database during index generation

    -m number
        The maximum words to index in a file

    -N /path/to/symlink
        Allow this symlink to be followed. Option may be repeated.

    -n
        Do not generate indexes, but process all other command line options

    -O on/off
        Turn on/off the optimization of the index database as part of the indexing step

    -P
        Generate a project for each of the top-level directories in source root

    -p /path/to/default/project
        This is the path to the project that should be selected by default in the web application(when no other project set either in cookie or in parameter). You should strip off the source root.

    -Q on/off
        Turn on/off quick context scan. By default only the first 32k of a file is scanned, and a '[..all..]' link is inserted if the file is bigger. Activating this may slow the server down (Note: this is setting only affects the web application)

    -q
        Run as quietly as possible

    -R /path/to/configuration
        Read configuration from the specified file

    -r on/off
        Turn on/off support for remote SCM systems

    -S
        Search for "external" source repositories and add them

    -s /path/to/source/root
        The root directory of the source tree

    -T number
        The number of threads to use for index generation. By default the number of threads will be set to the number of available CPUs

    -t number
        Default tabsize to use (number of spaces per tab character)

    -U host:port
        Send the current configuration to the specified address (This is most likely the web-app configured with ConfigAddress)

    -u url
        URL to the database that contains the history cache. Default: If -j specifies "embedded", "jdbc:derby:$DATA_ROOT/cachedb;create=true"; otherwise, "jdbc:derby://localhost/cachedb;create=true"

    -V
        Print version and quit

    -v
        Print progress information as we go along

    -W /path/to/configuration
        Write the current configuration to the specified file (so that the web application can use the same configuration

    -w webapp-context
        Context of webapp. Default is /source. If you specify a different name, make sure to rename source.war to that name.

    -X url:suffix
        URL Suffix for the user Information provider. Default: ""

    -z number
        depth of scanning for repositories in directory structure relative to source root

-------------------------------------------------------------------------------------------------
__PS:默认情况下，调用OpenGork脚本是会生成项目的历史记录的，如果不想生成脚本的历史记录, 可以修改
OpenGrok脚本的`UpdateGeneratedData` 方法，去掉`StdInvocation -H`的`-H`__
