Title: 压力测试工具ab && webbench
Date: 2015-06-26 07:29
Tags: ab, workbench
Slug: server-benchmarkingt-tool-ab-and-webbench
Author: crazygit
Summary: HTTP server benchmarking tool

## ab

ab是apache自带的压力测试工具。使用简单，便于一些简单的压力测试.


### 安装

    :::bash
    $ sudo apt-get install apache2-utils

### 使用帮助

    :::bash
    $ ab -h
    Usage: ab [options] [http[s]://]hostname[:port]/path
    Options are:
        -n requests     Number of requests to perform # 请求次数
        -c concurrency  Number of multiple requests to make at a time # 并发数
        -t timelimit    Seconds to max. to spend on benchmarking # 压力测试的最大时间
                        This implies -n 50000
        -s timeout      Seconds to max. wait for each response
                        Default is 30 seconds
        -b windowsize   Size of TCP send/receive buffer, in bytes
        -B address      Address to bind to when making outgoing connections
        -p postfile     File containing data to POST. Remember also to set -T  # POST方式，同时必须使用-T指定“Content-Type”
        -u putfile      File containing data to PUT. Remember also to set -T   # PUT方式
        -T content-type Content-type header to use for POST/PUT data, eg.
                        'application/x-www-form-urlencoded'
                        Default is 'text/plain'
        -v verbosity    How much troubleshooting info to print
        -w              Print out results in HTML tables # 以html表格形式输出结果
        -i              Use HEAD instead of GET # 使用Head请求
        -x attributes   String to insert as table attributes
        -y attributes   String to insert as tr attributes
        -z attributes   String to insert as td or th attributes
        -C attribute    Add cookie, eg. 'Apache=1234'. (repeatable)
        -H attribute    Add Arbitrary header line, eg. 'Accept-Encoding: gzip'  # 添加HTTP头信息
                        Inserted after all normal header lines. (repeatable)
        -A attribute    Add Basic WWW Authentication, the attributes   # 添加认证信息
                        are a colon separated username and password.
        -P attribute    Add Basic Proxy Authentication, the attributes
                        are a colon separated username and password.
        -X proxy:port   Proxyserver and port number to use
        -V              Print version number and exit
        -k              Use HTTP KeepAlive feature
        -d              Do not show percentiles served table.
        -S              Do not show confidence estimators and warnings.
        -q              Do not show progress when doing more than 150 requests
        -l              Accept variable document length (use this for dynamic pages)
        -g filename     Output collected data to gnuplot format file.
        -e filename     Output CSV file with percentages served
        -r              Don't exit on socket receive errors.   # 在接收到socket错误时不退出
        -h              Display usage information (this message)
        -Z ciphersuite  Specify SSL/TLS cipher suite (See openssl ciphers)
        -f protocol     Specify SSL/TLS protocol
                        (SSL3, TLS1, TLS1.1, TLS1.2 or ALL)

### 使用示例

    :::bash

    # GET

    # 30秒内并行1000个客户端，请求默认的50000次请求
    $ ab -c 1000 -t  30 http://www.baidu.com/
    # 并发100个客户端，请求10000次
    $ ab -c 100 -n 10000 http://www.baidu.com/

    # POST

    $ cat data.json
    {"apps": [{"package_name": "com.baidu.browser.apps", "app_name":"百度浏览器", "version_code": 1, "version_name": "5.3.4.1"}], "pm_name":"TCL M2M"}

    # post json 数据
    $ ab -c 1000 -t 30 -p data.json -T "application/json" -r "127.0.0.1:8888/m3/apps/update"

### 更多

关于其他的命令选项及命令的结果输出介绍，可以参看：

<http://httpd.apache.org/docs/2.2/programs/ab.html>


## webbench

另一个轻量级的压力测试工具，据说比ab好用，但是好像不支持模拟POST请求


### 安装

可以到<http://home.tiscali.cz/~cz210552/webbench.html>获取最新版本的下载地址

    $ wget http://home.tiscali.cz/~cz210552/distfiles/webbench-1.5.tar.gz

解压之后

    $ make && sudo make install


### 使用帮助

使用上和ab差不多，具体参数可以参考下面

    :::bash
    $ webbench
    webbench [option]... URL
    -f|--force               Don't wait for reply from server.
    -r|--reload              Send reload request - Pragma: no-cache.
    -t|--time <sec>          Run benchmark for <sec> seconds. Default 30.
    -p|--proxy <server:port> Use proxy server for request.
    -c|--clients <n>         Run <n> HTTP clients at once. Default one.
    -9|--http09              Use HTTP/0.9 style requests.
    -1|--http10              Use HTTP/1.0 protocol.
    -2|--http11              Use HTTP/1.1 protocol.
    --get                    Use GET request method.
    --head                   Use HEAD request method.
    --options                Use OPTIONS request method.
    --trace                  Use TRACE request method.
    -?|-h|--help             This information.
    -V|--version             Display program version.
