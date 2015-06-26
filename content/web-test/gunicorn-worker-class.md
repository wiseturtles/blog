Title: Gunicorn 几种 Worker class 性能测试比较
Date: 2015-06-26 09:30
Tags: gunicorn, flask, gevent, eventlet, tornado
Slug: gunicorn-worker-class-compare
Author: crazygit
Summary: Gunicorn 几种 worker class 性能测试比较


## 简介

* Gunicorn, 一个支持WSGI协议的web服务器
* Flask, 一个轻量级的python web框架

Gunicorn目前自带支持几种工作方式:

* sync (默认值)
* eventlet
* gevent
* tornado


## 测试环境准备

1. python 2.7+
2. redis-server 2.8.4
3. 压力测试工具ab
4. 代码及相关python包准备
    创建虚一个新的虚拟环境并安装需要的包

        :::bash
        $ mkvirtualenv test
        $ workon test

        $ cat requirements.txt
        gunicorn==19.3.0
        flask==0.10.1
        flask-redis==0.1.0
        gevent==1.0.2
        tornado==4.2
        eventlet==0.17.4

        $ pip install -r requirements.txt

    测试程序`app.py`

        :::python
        from flask import Flask
        from flask_redis import FlaskRedis

        REDIS_URL = "redis://:password-string@localhost:6379/0"
        app = Flask(__name__)
        app.config.from_object(__name__)

        redis = FlaskRedis(app, True)

        @app.route("/")
        def index():
            redis.incr("hit", 1)
            return redis.get("hit")

        if __name__ == '__main__':
            app.run()


## 开始测试

1. 使用ab工具,并行500个客户端, 发送50000次请求

        $ ab -c 500 -t 30 -r "http://127.0.0.1:8000/"

2. 分别使用四种方式启动使用服务， 并开启４个worker

        $ gunicorn -w 4 app:app --error-logfile - --worker-class sync
        $ gunicorn -w 4 app:app --error-logfile - --worker-class gevent
        $ gunicorn -w 4 app:app --error-logfile - --worker-class tornado
        $ gunicorn -w 4 app:app --error-logfile - --worker-class eventlet

3. 结果比较

<table class="table table-striped table-bordered table-hover table-condensed">
    <tbody>
        <tr>
            <td>
                Worker class
            </td>
            <td>
                Time taken for tests
            </td>
            <td>
                Complete requests
            </td>
            <td>
                Failed requests
            </td>
            <td>
                Requests per second
            </td>
            <td>
                用户平均请求等待时间
            </td>
            <td>
                服务器平均处理时间
            </td>
            <td>
                最小连接时间
            </td>
            <td>
                平均连接时间
            </td>
            <td>
                50%的连接时间
            </td>
            <td>
                最大连接时间
            </td>
        </tr>
        <tr>
            <td>
                sync
            </td>
            <td>
                37.363 s
            </td>
            <td>
                49928
            </td>
            <td>
                793
            </td>
            <td>
                1336.29
            </td>
            <td>
                374.169 ms
            </td>
            <td>
                0.748 ms
            </td>
            <td>
                5 ms
            </td>
            <td>
                75 ms
            </td>
            <td>
                17 ms
            </td>
            <td>
                31746 ms
            </td>
        </tr>
        <tr>
            <td>
               tornado
            </td>
            <td>
               13.995
            </td>
            <td>
                50000
            </td>
            <td>
                543
            </td>
            <td>
               3572.64
            </td>
            <td>
                139.953 ms
            </td>
            <td>
                0.280 ms
            </td>
            <td>
                6 ms
            </td>
            <td>
                110 ms
            </td>
            <td>
                24 ms
            </td>
            <td>
                13837 ms
            </td>
        </tr>
        <tr>
            <td>
              eventlet
            </td>
            <td>
              8.156
            </td>
            <td>
                50000
            </td>
            <td>
                0
            </td>
            <td>
               6130.74
            </td>
            <td>
               81.556
            </td>
            <td>
                0.163 ms
            </td>
            <td>
                2 ms
            </td>
            <td>
                80 ms
            </td>
            <td>
               62 ms
            </td>
            <td>
               3153 ms
            </td>
        </tr>
        <tr>
            <td>
                gevent
            </td>
            <td>
                7.647 s
            </td>
            <td>
                50000
            </td>
            <td>
                0
            </td>
            <td>
               6538.23
            </td>
            <td>
                76.473 ms
            </td>
            <td>
                0.153 ms
            </td>
            <td>
                1 ms
            </td>
            <td>
                74 ms
            </td>
            <td>
                52 ms
            </td>
            <td>
                1122 ms
            </td>
        </tr>
    </tbody>
</table>


从测试结果来看，默认自带sync效率很低，并且在测试时发现，采用sync方式在高并发时
会出现woker重启的情况, 如下:

<pre>
[2015-06-25 11:31:06 +0000] [27040] [CRITICAL] WORKER TIMEOUT (pid:27064)
[2015-06-25 11:31:06 +0000] [27040] [CRITICAL] WORKER TIMEOUT (pid:27051)
[2015-06-25 11:31:06 +0000] [27040] [CRITICAL] WORKER TIMEOUT (pid:27045)
[2015-06-25 11:31:06 +0000] [27040] [CRITICAL] WORKER TIMEOUT (pid:27046)
[2015-06-25 11:31:06 +0000] [27064] [INFO] Worker exiting (pid: 27064)
[2015-06-25 11:31:06 +0000] [27051] [INFO] Worker exiting (pid: 27051)
[2015-06-25 11:31:06 +0000] [27045] [INFO] Worker exiting (pid: 27045)
[2015-06-25 11:31:06 +0000] [27046] [INFO] Worker exiting (pid: 27046)
[2015-06-25 11:31:06 +0000] [27263] [INFO] Booting worker with pid: 27263
[2015-06-25 11:31:06 +0000] [27264] [INFO] Booting worker with pid: 27264
[2015-06-25 11:31:06 +0000] [27277] [INFO] Booting worker with pid: 27277
[2015-06-25 11:31:06 +0000] [27280] [INFO] Booting worker with pid: 27280
</pre>

eventlet 和gevent两种方式效果最好，数据基本差不多.
