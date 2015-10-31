Title: scrapyd和scrapyd-client使用教程
Date: 2015-10-29 17:42
Tags: scrapyd, scrapy, scrapyd-client
Slug: scrapyd
Author: crazygit
Summary: scrapyd和scrapyd-client使用整理


scrapyd是一个用于部署和运行scrapy爬虫的程序，它允许你通过JSON API来部署爬虫项目和控制爬虫运行

## 概览

### 项目和版本

scrapyd可以管理多个项目，并且每个项目允许有多个版本，但是只有最新的版本会被用来运行爬虫.

最方便的版本管理就是利用VCS工具来记录你的爬虫代码，版本比较不是简单的通过字母排序，而是通过智能的算法，和[distutils](https://docs.python.org/2/library/distutils.html)一样，例如: r10比r９更大.


### 工作原理

scrapyd是一个守护进程，监听爬虫的运行和请求，然后启动进程来执行它们

### 启动服务

```bash
$ scrapyd
```

### 调度爬虫运行

```bash
$ curl http://localhost:6800/schedule.json -d project=myproject -d spider=spider2
{"status": "ok", "jobid": "26d1b1a6d6f111e0be5c001e648c57f8"}
```

### web接口

<http://localhost:6800/>


## 安装

### 需求

* Python 2.6+
* Twisted 8.0+
* Scrapy 0.17+

### 安装

```bash
$ pip install scrapyd
```

或

```bash
$ sudo apt-get install scrapyd
```

## 项目部署

直接使用[scrapyd-client](https://github.com/scrapy/scrapyd-client)提供的`scrapyd-deploy`工具.

### 安装scrapyd-client

```bash
$ pip install scrapyd-client
```

### scrapyd-client工作原理

打包项目，然后调用`scrapyd`的[`addversion.json`](https://scrapyd.readthedocs.org/en/latest/api.html#addversion-json)接口部署项目

### 配置服务器信息

为了方便叙述，整个部署流程以部署[豆瓣电影](https://github.com/crazygit/scrapy_demo/tree/master/douban_movie)爬虫为例。
配置服务器和项目信息, 需要编辑`scrapy.cfg`文件，添加如下内容

```
[deploy:server-douban]
url = http://localhost:6800/
```
其中`server-douban`为服务器名称, `url`为服务器地址，即运行了`scrapyd`命令的服务器。

检查配置, 列出当前可用的服务器

```bash
$ scrapyd-deploy -l
server-douban        http://localhost:6800/
```

列出服务器上所有的项目, 需要确保服务器上的`scrapyd`命令正在执行，否则会报连接失败.首次运行的话，可以看到只有一个`default`项目

```bash
$ scrapyd-deploy -L server-douban
default
```

打开<http://localhost:6800/>, 可以看到`Available projects: default`

### 部署项目

在爬虫项目根目录下执行下面的命令, 其中`target`为上一步配置的服务器名称，`project`为项目名称，可以根据实际情况自己指定。

```
scrapyd-deploy <target> -p <project>
```

```bash
$ scrapyd-deploy server-douban -p douban-movies
Packing version 1446102534
Deploying to project "douban-movies" in http://localhost:6800/addversion.json
Server response (200):
{"status": "ok", "project": "douban-movies", "version": "1446102534", "spiders": 1, "node_name": "sky"}

```

部署操作会打包你的当前项目，如果当前项目下有`setup.py`文件，就会使用它，没有的会就会自动创建一个。(如果后期项目需要打包的话，可以根据自己的需要修改里面的信息，也可以暂时不管它).
从返回的结果里面，我们可以看到部署的状态，项目名称，版本号和爬虫个数，以及当前的主机名称.

检查部署结果

```bash
$ scrapyd-deploy -L server-douban
default
douban-movies
```
或再次打开<http://localhost:6800/>, 也可以看到`Available projects: default, douban-movies`

我们也可以把项目信息写入到配置文件中，部署时就不用指定项目信息，编辑`scrapy.cfg`文件，添加项目信息

```
[deploy:server-douban]
url = http://localhost:6800/
project = douban-movies
```

下次部署可以直接执行

```bash
$ scrapyd-deploy
```

如果配置了多个服务器的话，可以将项目直接部署到多台服务器

```bash
$ scrapyd-deploy -a -p <project>
```

### 指定版本号

默认情况下, `scrapyd-deploy`使用当前的时间戳作为版本号，我们可以使用`--version`来指定版本号

```
scrapyd-deploy <target> -p <project> --version <version>
```

版本号的格式必须满足[LooseVersion](http://epydoc.sourceforge.net/stdlib/distutils.version.LooseVersion-class.html)

如：
```bash
# 设置版本号为0.1
$ scrapyd-deploy server-douban -p douban-movies --version 0.1
Packing version 0.1
Deploying to project "douban-movies" in http://localhost:6800/addversion.json
Server response (200):
{"status": "ok", "project": "douban-movies", "version": "0.1", "spiders": 1, "node_name": "sky"}
```

如果使用了`Mercurial`或`Git`管理代码，　可以使用`HG`和`GIT`作为version的参数，也可以将它写入`scrapy.cfg`文件，那么就会使用当前的reversion作为版本号。
```
[deploy:target]
...
version = GIT
```

```bash
$ cat scrapy.cfg
...
[deploy:server-douban]
url = http://localhost:6800/
project = douban-movies
version = GIT

# 当前版本号为r7-master
$ scrapyd-deploy server-douban -p douban-movies 
fatal: No names found, cannot describe anything.
Packing version r7-master
Deploying to project "douban-movies" in http://localhost:6800/addversion.json
Server response (200):
{"status": "ok", "project": "douban-movies", "version": "r7-master", "spiders": 1, "node_name": "sky"}
```

关于从GIT获取版本号的方式，可以参看`scrapyd-client`源码部分
```python
  elif version == 'GIT':
        p = Popen(['git', 'describe'], stdout=PIPE)
        d = p.communicate()[0].strip('\n')
        if p.wait() != 0:
            p = Popen(['git', 'rev-list', '--count', 'HEAD'], stdout=PIPE)
            d = 'r%s' % p.communicate()[0].strip('\n')

        p = Popen(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stdout=PIPE)
        b = p.communicate()[0].strip('\n')
        return '%s-%s' % (d, b)
```

### 服务器添加认证信息

我们也可以在scrapyd前面加一层反向代理来实现用户认证。以nginx为例, 配置nginx

```
server {
       listen 6801;
       location / {
            proxy_pass            http://127.0.0.1:6800/;
            auth_basic            "Restricted";
            auth_basic_user_file  /etc/nginx/htpasswd/user.htpasswd;
        }
}

```

`/etc/nginx/htpasswd/user.htpasswd`里设置的用户名和密码都是`test`
修改配置文件，添加用户信息信息

```
...
[deploy:server-douban]
url = http://localhost:6801/
project = douban-movies
version = GIT
username = test
password = test

```
注意上面的`url`已经修改为了nginx监听的端口。

**提醒**: 记得修改服务器上scrapyd的配置`bind_address`字段为`127.0.0.1`，以免可以从外面绕过nginx, 直接访问6800端口。
关于配置可以参看本文后面的配置文件设置.

## API

scrapyd的web界面比较简单，主要用于监控，所有的调度工作全部依靠接口实现.
具体可以参考[官方文档](http://scrapyd.readthedocs.org/en/stable/api.html)

常用接口:

* 调度爬虫

        $ curl http://localhost:6800/schedule.json -d project=myproject -d
        spider=somespider
        # 带上参数
        $ curl http://localhost:6800/schedule.json -d project=myproject -d spider=somespider -d setting=DOWNLOAD_DELAY=2 -d arg1=val1

* 取消

        $ curl http://localhost:6800/cancel.json -d project=myproject -d job=6487ec79947edab326d6db28a2d86511e8247444

* 列出项目

        $ curl http://localhost:6800/listprojects.json

* 列出版本
    
        $ curl http://localhost:6800/listversions.json?project=myproject

* 列出爬虫

        $ curl http://localhost:6800/listspiders.json?project=myproject

* 列出job

        $ curl http://localhost:6800/listjobs.json?project=myproject

* 删除版本

        $ curl http://localhost:6800/delversion.json -d project=myproject -d version=r99

* 删除项目

        $ curl http://localhost:6800/delproject.json -d project=myproject


## 配置文件

`scrapyd`启动的时候会自动搜索配置文件，配置文件的加载顺序为

* `/etc/scrapyd/scrapyd.conf`
* `/etc/scrapyd/conf.d/*`
* `scrapyd.conf`
* `~/.scrapyd.conf`

最后加载的会覆盖前面的设置

默认配置文件如下, 可以根据需要修改

```
[scrapyd]
eggs_dir    = eggs
logs_dir    = logs
items_dir   = items
jobs_to_keep = 5
dbs_dir     = dbs
max_proc    = 0
max_proc_per_cpu = 4
finished_to_keep = 100
poll_interval = 5
http_port   = 6800
debug       = off
runner      = scrapyd.runner
application = scrapyd.app.application
launcher    = scrapyd.launcher.Launcher

[services]
schedule.json     = scrapyd.webservice.Schedule
cancel.json       = scrapyd.webservice.Cancel
addversion.json   = scrapyd.webservice.AddVersion
listprojects.json = scrapyd.webservice.ListProjects
listversions.json = scrapyd.webservice.ListVersions
listspiders.json  = scrapyd.webservice.ListSpiders
delproject.json   = scrapyd.webservice.DeleteProject
delversion.json   = scrapyd.webservice.DeleteVersion
listjobs.json     = scrapyd.webservice.ListJobs
```
关于配置的各个参数具体含义，可以参考[官方文档](http://scrapyd.readthedocs.org/en/stable/config.html)
