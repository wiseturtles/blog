Title: 高并发下Flask中采用gevent方式启用导致redis连接数增加
Date: 2015-06-26 12:59
Tags: flask, redis, gevent
Slug: flask-redis-gevent
Author: crazygit
Summary: 高并发下Flask中采用gevent方式启用导致redis连接数增加,　引起redis服务器连接失败


### 现象

最近线上的redis服务器会莫名出现无法突然之间无法连接的情况，需要重启一下redis服务器才能正常工作，感觉很诡异.
查看redis日志，发现报如下错误:

> Error allocating resoures for the client

网上搜索之后，找到

<http://blog.sina.com.cn/s/blog_6262a50e0101cjyf.html>

根据描述, 怀疑可能是redis连接数太多导致,于是查看

    $ redis-cli -a password info | grep connected_clients
    connected_clients:6997

这还是我刚刚才重新启动了redis server不久看到的数据。

为什么会用这么高连接数?上面的文章中介绍的是由于代码引起不停地创建redis Connection pool导致。仔细检查了自己的代码之后，发现不会有这种情况，但为什么还是会有这么高的连接?


### 验证

经过调试发现。虽然使用py-redis连接redis, 它使用到了连接池，但是，连接池默认是没有设置连接数的上限(可以通过相关参数设置)，当高并发时，它会不断的创建连接，并且这些连接用完之后也不会自动释放。
由于我们的服务运行采用的gevent方式。 因此, 更容易引起这个问题。为了验证自己的
猜测, 写了个简单的计数程序`app.py`测试一下。

    :::python
    from flask import Flask
    from flask_redis import FlaskRedis

    REDIS_URL = "redis://:password@localhost:6379/0"
    DEBUG = True
    app = Flask(__name__)
    app.config.from_object(__name__)

    redis = FlaskRedis(app, True)


    @app.route("/")
    def index():
        redis.incr("hit", 1)
        return redis.get("hit")

    if __name__ == '__main__':
        app.run()


采用gevent方式, 单worker启动

    $ gunicorn -w 1 app:app --worker-class gevent --error-logfile -

使用ab模拟500个用户发送50000次请求的高并发

    $ ab  -c 500  -t 30 -r  "http://127.0.0.1:8000/"

查看连接数

    $ redis-cli -a password info |grep connected_clients
    connected_clients:232

可以看到, 在高并发, 单worker的条件下， 一个连接池的连接数会就有两百多。然后测试开启４个worker的话，能达到一千二百多。

这些连接在连接池里使用之后，基本上都长期处于idle状态，白白浪费资源.

    $ redis-cli -a password client list
    addr=127.0.0.1:45327 fd=170 name= age=35 idle=34 flags=N db=0 sub=0 psub=0
    multi=-1 qbuf=0 qbuf-free=0 obl=0 oll=0 omem=0 events=r cmd=get
    addr=127.0.0.1:43684 fd=44 name= age=36 idle=10 flags=N db=0 sub=0 psub=0
    multi=-1 qbuf=0 qbuf-free=0 obl=0 oll=0 omem=0 events=r cmd=get
    addr=127.0.0.1:43704 fd=45 name= age=36 idle=10 flags=N db=0 sub=0 psub=0
    multi=-1 qbuf=0 qbuf-free=0 obl=0 oll=0 omem=0 events=r cmd=get
    addr=127.0.0.1:43705 fd=46 name= age=36 idle=10 flags=N db=0 sub=0 psub=0
    multi=-1 qbuf=0 qbuf-free=0 obl=0 oll=0 omem=0 events=r cmd=get
    addr=127.0.0.1:43729 fd=47 name= age=36 idle=10 flags=N db=0 sub=0 psub=0
    multi=-1 qbuf=0 qbuf-free=0 obl=0 oll=0 omem=0 events=r cmd=get
    addr=127.0.0.1:43730 fd=48 name= age=36 idle=10 flags=N db=0 sub=0 psub=0
    multi=-1 qbuf=0 qbuf-free=0 obl=0 oll=0 omem=0 events=r cmd=get
    addr=127.0.0.1:43731 fd=49 name= age=36 idle=10 flags=N db=0 sub=0 psub=0
    multi=-1 qbuf=0 qbuf-free=0 obl=0 oll=0 omem=0 events=r cmd=get
    addr=127.0.0.1:43732 fd=50 name= age=36 idle=10 flags=N db=0 sub=0 psub=0
    .....



### 解决方式:

1. 从目前的情况来看，是由于连接池维持了太多的连接导致.　因此不用的连接池应该及
   时被释放掉。通过设置

        $ reidis-cli -a password CONFIG SET timeout 30

    让redis自动释放掉idle时间超过30秒的连接,　设置之后，服务器上redis连接数一
    下子降下来了。


2. 让redis连接也异步

    根据另一篇文章介绍使用redis异步, 自己测试之后发现没有什么效果，也不知道哪
    里没有做对, 有机会再研究。

    <https://gehrcke.de/2013/01/highly-concurrent-connections-to-redis-with-gevent-and-redis-py/>
