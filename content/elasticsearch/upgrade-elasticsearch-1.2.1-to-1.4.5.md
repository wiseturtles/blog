Title: Upgrade Elasticsearch 1.2.1 to 1.4.5
Date: 2015-06-19
Category: Elasticsearch
Tags: Dashboard, Elasticsearch, Logstash, ELK
Slug:-Upgrade-Elasticsearch-1.2.1-to-1.4.5
Authors: Zhang Wanming
Summary: 将Elasticsearch 1.2.1升级到1.4.5

一年前刚开始做应用市场数据统计，团队选用了ELK中的EL (Elasticsearch, Logstash)，没有用Kibana；而且根据产品、运营需求调用ES Restful API，自己做Web展示。
用了以下插件:analysis-icu, analysis-ik, analysis-mmseg, analysis-pinyin
当时ES版本为1.2.1，一直没有升级，最近升级到1.4.5。

我们之前服务器是Debian 7，现在服务器是CentOS 6.5；服务器版本和ES没有关系，至少我没碰到任何系统问题。

目前有两台ES 1.2.1，准备用三台ES 1.4.5替换。刚开始没有root权限，只好下载压缩包安装。

注: Elasticsearch和Logstash都需要安装JDK, 我们用的JDK 1.7


安装Logstash 1.4.3
=====================

安装需要的软件包
-----------------

    :::bash

    $ cd /data/software
    $ wget https://download.elastic.co/logstash/logstash/logstash-1.4.3.tar.gz
    $ tar zxf logstash-1.4.3.tar.gz


修改配置文件
-------------

    :::bash

    $ cat /data/softwares/logstash-1.4.3/logstash.conf | grep -Ev '^#|^$'
    input {
      redis {
        codec => "json"
        data_type => "list"
        host => "x.x.x.x"
        key => "appstore:logstash"
        password => "passwd"
        tags => ["appstore_logs"]
        db => 0
      }
      redis {
        codec => "json"
        data_type => "list"
        host => "x.x.x.x"
        password => "passwd"
        key => "appstore:overview_reports"
        tags => ["overview_reports"]
        db => 0
      }
      redis {
        codec => "json"
        data_type => "list"
        host => "x.x.x.x"
        password => "passwd"
        key => 'appstore:imei_reports'
        tags => ["imei_reports"]
        db => 1
      }
      redis { 
         codec => "json" 
         data_type => "list" 
         host => "x.x.x.x" 
         password => "tclonline"
         key => "appstore:overview_date_reports" 
         tags => ["overview_date_reports"] 
         db => 3
       } 
       redis { 
         codec => "json" 
         data_type => "list" 
         host => "x.x.x.x" 
         password => "pwd"
         key => "appstore:overview_model_reports" 
         tags => ["overview_model_reports"] 
         db => 3
      
       } 
    }
    filter {
      if "appstore_logs" in [tags] {
        date {
          match => [ "timestamp" , "UNIX" ]
        }
      }
      if "imei_reports" in [tags] {
        date {
          match => [ "timestamp" , "UNIX" ]
        }
      }
    }
    output {
      if "appstore_logs" in [tags] {
        elasticsearch { 
          index => logstash
          index_type => "appstore_stats"
          cluster => "elasticsearch_dashboard"
          node_name => "logstash_appstore_logs"
        }
        redis{
          data_type => "list"
          db => 3
          host => "x.x.x.x" 
          password => "passwd"
          key => "logstash:appstore_logs"
        }
      }
      if "overview_reports" in [tags] {
        elasticsearch { 
          index => dashboard
          index_type => "overview_records"
          cluster => "elasticsearch_dashboard"
          node_name => "logstash_overview_reports"
        }
      }
       if "imei_reports" in [tags] {
        elasticsearch {
          index => imei
          index_type => "imei_records"
          cluster => "elasticsearch_dashboard"
          node_name => "logstash_imei_reports"
        }
      }
       if "overview_date_reports" in [tags] { 
         elasticsearch { 
           cluster => "elasticsearch_dashboard" 
           index => dashboard 
           index_type => "overview_date_records" 
           node_name => "logstash_overview_date_reports"
         } 
       } 
        if "overview_model_reports" in [tags] { 
         elasticsearch { 
           cluster => "elasticsearch_dashboard" 
           index => dashboard 
           index_type => "overview_model_records" 
           node_name => "logstash_overview_model_reports"
         } 
       }   
    }


启动测试
----------

    :::bash

    $ cd /data/softwares/logstash-1.4.3
    $ bin/logstash -f logstash.conf


安装Elasticsearch 1.4.5
========================

安装需要的软件包
-----------------

    :::bash

    $ cd /data/software
    $ wget https://download.elastic.co/elasticsearch/elasticsearch/elasticsearch-1.4.5.tar.gz
    $ tar zxf elasticsearch-1.4.5.tar.gz


安装插件：

    :::bash

    $ cd /data/software # 安装分词插件
    $ git clone -b 1.4.0 https://github.com/medcl/elasticsearch-rtf.git
    $ cd elasticsearch-rtf
    $ cp -vrf plugins/analysis-ik /data/softwares/elasticsearch-1.4.5/plugins/
    $ cp -vrf config/ik config/mmseg /data/softwares/elasticsearch-1.4.5/config/


    :::bash

    $ cd /data/software # 监控插件
    $ cd elasticsearch-1.4.5
    $ bin/plugin -install mobz/elasticsearch-head # head插件
    $ bin/plugin -install lukas-vlcek/bigdesk     # bigdesk插件


修改配置文件
-------------

    :::bash

    $ cat /data/softwares/elasticsearch-1.4.5/config/elasticsearch.yml | grep -Ev '^#|^$'
    cluster.name: elasticsearch_dashboard
    node.name: "es1"
    node.master: true
    node.data: true
    index.number_of_shards: 5
    index.number_of_replicas: 2
    path.data: /data/softwares/elasticsearch-1.4.5/data
    path.work: /data/softwares/elasticsearch-1.4.5/work
    path.logs: /data/log/elasticsearch
    path.plugins: /data/softwares/elasticsearch-1.4.5/plugins
    network.bind_host: 192.168.1.2
    network.publish_host: 192.168.1.2
    network.host: 192.168.1.2
    transport.tcp.port: 9300
    http.port: 9200
    indices.recovery.max_bytes_per_sec: 200mb
    indices.recovery.concurrent_streams: 8
    discovery.zen.minimum_master_nodes: 2
    discovery.zen.ping.timeout: 10s
    discovery.zen.ping.multicast.enabled: true
    discovery.zen.ping.unicast.hosts: ["192.168.1.2", "192.168.1.6", "192.168.1.7"]
    index:
      analysis:
        analyzer:
          standardPlusWordDelimiter:
            type: custom
            tokenizer: standard
            filter: [standard, wordDelim, lowercase, stop, dict]
          ik:
            alias: [ik_analyzer]
            type: ik
          ik_max_word:
            type: ik
            use_smart: false
          ik_smart:
            type: ik
            use_smart: true
          pinyin_ngram_analyzer:
            type: custom
            tokenizer: my_pinyin
            filter: [standard,lowercase,nGram,trim,unique]     
        tokenizer:
          my_pinyin:
            type: pinyin
            first_letter: prefix
            padding_char : ""
        filter:
          wordDelim:
            type: word_delimiter
            preserve_original: true
          dict:
            type: dictionary_decompounder
            word_list: [cool, iris, fire, bug, flag, fox, grease, monkey, flash, block, forecast, screen, grab, cookie, auto, fill, text, all, so, think, mega, upload, download, video, map, spring, fix, input, clip, fly, lang, up, down, persona, css, html, all, http, ball, firefox, bookmark, chat, zilla, edit, menu, menus, status, bar, with, easy, sync, search, google, time, window, js, super, scroll, title, close, undo, user, inspect, inspector, browser, context, dictionary, mail, button, url, password, secure, image, new, tab, delete, click, name, smart, down, manager, open, query, net, link, blog, this, color, select, key, keys, foxy, translate, word]


注：
1. 删除了注释
2. 其它机器配置文件类似，只需要修改和IP相关的字段值


启动Elasticsearch
-------------------

测试能否正常启动：

    :::bash

    $ cd /data/software/elasticsearch-1.4.5
    $ bin/elasticsearch  # 启动ES，测试是否可以正常启动
    $ tail -f /data/log/elasticsearch/elasticsearch_dashboard.log # 查看日志


监控插件使用
--------------

head: http://<your-es-ip>:9200/_plugin/head/
bigdesk: http://<your-es-ip>:9200/_plugin/bigdesk/


配置supervisor
================

如果可以正常启动，我们通过supervisor管理Elasticsearch和Logstash。

    :::bash

    $ sudo pip install supervisor # 后来拿到root权限，否则还要先弄Python virtual env
    $ 修改/etc/init.d/supervisor 以及 chkconfig 添加系统启动就不说了


    :::bash

    $ cat /etc/supervisor/supervisord.conf | grep -Ev '^;|^$'
    [unix_http_server]
    file=/var/run/supervisor.sock    ; (the path to the socket file)
    chmod=0700                       ; sockef file mode (default 0700)
    [rpcinterface:supervisor]
    supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface
    [supervisord]
    http_port=/var/run/supervisor.sock ; (default is to run a UNIX domain socket server)
    logfile=/data/log/supervisor/supervisord.log ; (main log file;default $CWD/supervisord.log)
    logfile_maxbytes=50MB       ; (max main logfile bytes b4 rotation;default 50MB)
    logfile_backups=10          ; (num of main logfile rotation backups;default 10)
    loglevel=debug              ; (logging level;default info; others: debug,warn)
    pidfile=/var/run/supervisord.pid ; (supervisord pidfile;default supervisord.pid)
    nodaemon=false              ; (start in foreground if true;default false)
    minfds=1024                 ; (min. avail startup file descriptors;default 1024)
    minprocs=200                ; (min. avail process descriptors;default 200)
    childlogdir=/data/log/supervisor ; ('AUTO' child log dir, default $TEMP)
    [supervisorctl]
    serverurl=unix:////var/run/supervisor.sock ; use a unix:// URL  for a unix socket
    [include]
    files = /etc/supervisor/conf.d/*.conf


    :::bash

    $ cat /etc/supervisor/conf.d/elasticsearch.conf 
    [program:elasticsearch]
    command=/data/softwares/elasticsearch-1.4.5/bin/elasticsearch -Xmx6g -Xms6g -XX:PermSize=512m -Des.max-open-files=true
    directory=/data/softwares/elasticsearch-1.4.5
    user=work
    autostart=true
    autorestart=true
    stdout_logfile=/data/log/supervisor/elasticsearch.stdout
    stderr_logfile=/data/log/supervisor/elasticsearch.stderr


    :::bash

    $ cat /etc/supervisor/conf.d/logstash.conf 
    [program:logstash]
    command=/data/softwares/logstash-1.4.3/bin/logstash -f logstash.conf
    directory=/data/softwares/logstash-1.4.3
    user=work
    autostart=true
    autorestart=true
    stdout_logfile=/data/log/supervisor/logstash.stdout
    stderr_logfile=/data/log/supervisor/logstash.stderr


常用的ES命令别名
=================

    :::bash

    $ tail -n3 ~/.bashrc 
    alias esh="curl $(ip -4 -o addr show dev eth0 | awk '{split($4,a,"/");print a[1]}'):9200/_cluster/health?pretty"
    alias esi="curl $(ip -4 -o addr show dev eth0 | awk '{split($4,a,"/");print a[1]}'):9200/_cat/indices?pretty"
    alias ess="curl $(ip -4 -o addr show dev eth0 | awk '{split($4,a,"/");print a[1]}'):9200/_cat/shards"
    alias esdownlocal="curl $(ip -4 -o addr show dev eth0 | awk '{split($4,a,"/");print a[1]}'):9200/_cluster/nodes/_local/_shutdown"
    alias esdownall="curl $(ip -4 -o addr show dev eth0 | awk '{split($4,a,"/");print a[1]}'):9200/_shutdown"


升级
=======

通过上面步骤，配置好3台Elasticsearch 1.4.5，然后，将这三台ES机器加入以前的Elasticsearch 1.2.1的集群。
数据逐步同步到ES 1.4.5后，逐步将ES 1.2.1的机器停掉。


碰到的问题
============

没有将shard同步到新加入的ES 1.4.5机器上
------------------------------------------

修改number_of_replicas，根据机器个数修改。

    :::bash

    $ curl -XPUT '<your-ip>:9200/<your-index>/_settings' -d '{
         "index" : {
             "number_of_replicas" : 2
          }
    }'


明确让某个index的某个shard分配到指定机器上。

    :::bash

    $ curl -XPOST '<your-es-ip>:9200/_cluster/reroute' -d '{
        "commands" : [ {
            "move" :
                {
                  "index" : "your-index", "shard" : shard-no,
                  "from_node" : "es-node-name", "to_node" : "es-node-name"
                }
            },
            {
              "allocate" : {
                  "index" : "your-index", "shard" : shard-no, "node" : "es-node-name"
              }
            }
        ]
    }'


比如：

    :::bash

    $ curl -XPOST 'localhost:9200/_cluster/reroute' -d '{
        "commands" : [ {
            "move" :
                {
                  "index" : "logstash_v1_new", "shard" : 4,
                  "from_node" : "Yojimbo", "to_node" : "es3"
                }
            },
            {
              "allocate" : {
                  "index" : "logstash_v1_new", "shard" : 4, "node" : "es2"
              }
            }
        ]
    }'


参考：

1. http://stackoverflow.com/questions/23656458/elasticsearch-what-to-do-with-unassigned-shards/
2. http://stackoverflow.com/questions/25135869/how-to-rebalance-shard-elasticsearch
3. https://t37.net/how-to-fix-your-elasticsearch-cluster-stuck-in-initializing-shards-mode.html
4. http://stackoverflow.com/questions/19967472/elasticsearch-unassigned-shards-how-to-fix
