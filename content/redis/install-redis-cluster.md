Title: Redis集群搭建
Date: 2015-09-18 23:48
Tags: redis,cluster,install
Slug: install-redis-cluster
Author: crazygit
Summary: install-redis-cluster


## Redis集群搭建


```bash
# 下载
$ wget http://download.redis.io/releases/redis-3.0.4.tar.gz
$ tar -zxvf redis-3.0.4.tar.gz
$ cd redis-3.0.4

# 编译
$ make

# 检查依赖， 如果有错误就修复
# 如果遇到错误“Test replication partial resync: ok psync”, 可以忽略或再重复执
# 行几次make test就可以通过了
$ make test

# 安装
$ sudo make install

# 添加开机启动, 会有一些交互提问，按需选择即可
$ sudo utils/install_server.sh
Welcome to the redis service installer
This script will help you easily set up a running redis server

Please select the redis port for this instance: [6379] 
Selecting default: 6379 
Please select the redis config file name [/etc/redis/6379.conf] 
Selected default - /etc/redis/6379.conf
Please select the redis log file name [/var/log/redis_6379.log] 
Selected default - /var/log/redis_6379.log
Please select the data directory for this instance [/var/lib/redis/6379] 
Selected default - /var/lib/redis/6379
Please select the redis executable path [/usr/local/bin/redis-server] 
Selected config:
Port           : 6379 
Config file    : /etc/redis/6379.conf
Log file       : /var/log/redis_6379.log
Data dir       : /var/lib/redis/6379
Executable     : /usr/local/bin/redis-server
Cli Executable : /usr/local/bin/redis-cli
Is this ok? Then press ENTER to go on or Ctrl-C to abort.
Copied /tmp/6379.conf => /etc/init.d/redis_6379
Installing service...
 Adding system startup for /etc/init.d/redis_6379 ...
   /etc/rc0.d/K20redis_6379 -> ../init.d/redis_6379
   /etc/rc1.d/K20redis_6379 -> ../init.d/redis_6379
   /etc/rc6.d/K20redis_6379 -> ../init.d/redis_6379
   /etc/rc2.d/S20redis_6379 -> ../init.d/redis_6379
   /etc/rc3.d/S20redis_6379 -> ../init.d/redis_6379
   /etc/rc4.d/S20redis_6379 -> ../init.d/redis_6379
   /etc/rc5.d/S20redis_6379 -> ../init.d/redis_6379
Success!
Starting Redis server...
Installation successful!


# 因为要搭建单机集群，重复执行上面的命令，同时设置6380, 6381
# 完成后，可以看到如下文件
$ ls /etc/init.d/redis_*
/etc/init.d/redis_6379  /etc/init.d/redis_6380  /etc/init.d/redis_6381
$ ls /etc/redis/
6379.conf  6380.conf  6381.conf


# 开启集群
$ sudo sed -i 's/# cluster-enabled yes/cluster-enabled yes/' /etc/redis/*.conf

# 同时去掉/etc/redis/*.conf 文件的`cluster-config-file` 的注释，并分别设置为
# cluster-config-file /etc/redis/nodes-6379.conf
# cluster-config-file /etc/redis/nodes-6380.conf
# cluster-config-file /etc/redis/nodes-6381.conf

# 重启redis服务
$ ps -ef |grep redis
root     31033     1  0 00:18 ?        00:00:00 /usr/local/bin/redis-server *:6379 [cluster]    
root     31072     1  0 00:18 ?        00:00:00 /usr/local/bin/redis-server *:6380 [cluster]    
root     31111     1  0 00:18 ?        00:00:00 /usr/local/bin/redis-server *:6381 [cluster]    

# 安装redis client需要的依赖
$ sudo apt-get install ruby
$ sudo gem install redis

# 查看可用的命令
$ src/redis-trib.rb help 
Usage: redis-trib <command> <options> <arguments ...>

  create          host1:port1 ... hostN:portN
                  --replicas <arg>
  check           host:port
  fix             host:port
  reshard         host:port
                  --from <arg>
                  --to <arg>
                  --slots <arg>
                  --yes
  add-node        new_host:new_port existing_host:existing_port
                  --slave
                  --master-id <arg>
  del-node        host:port node_id
  set-timeout     host:port milliseconds
  call            host:port command arg arg .. arg
  import          host:port
                  --from <arg>
  help            (show this help)

For check, fix, reshard, del-node, set-timeout you can specify the host and port of any working node in the cluster.


# 创建集群
$ sudo src/redis-trib.rb create 127.0.0.1:6379 127.0.0.1:6380 127.0.0.1:6381
>>> Creating cluster
Connecting to node 127.0.0.1:6379: OK
Connecting to node 127.0.0.1:6380: OK
Connecting to node 127.0.0.1:6381: OK
>>> Performing hash slots allocation on 3 nodes...
Using 3 masters:
127.0.0.1:6379
127.0.0.1:6380
127.0.0.1:6381
M: 50eee84811854ce707bb25ce05f1688eafa46c8d 127.0.0.1:6379
   slots:0-5460 (5461 slots) master
M: 3cdc94999a66c325dd91ca4af70fa9a9fe1bc623 127.0.0.1:6380
   slots:5461-10922 (5462 slots) master
M: 059fd2e13499b22aedfa0f0ad3707fe7534d96db 127.0.0.1:6381
   slots:10923-16383 (5461 slots) master
Can I set the above configuration? (type 'yes' to accept): yes
>>> Nodes configuration updated
>>> Assign a different config epoch to each node
>>> Sending CLUSTER MEET messages to join the cluster
Waiting for the cluster to join.
>>> Performing Cluster Check (using node 127.0.0.1:6379)
M: 50eee84811854ce707bb25ce05f1688eafa46c8d 127.0.0.1:6379
   slots:0-5460 (5461 slots) master
M: 3cdc94999a66c325dd91ca4af70fa9a9fe1bc623 127.0.0.1:6380
   slots:5461-10922 (5462 slots) master
M: 059fd2e13499b22aedfa0f0ad3707fe7534d96db 127.0.0.1:6381
   slots:10923-16383 (5461 slots) master
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.

# 也可以设置主从, 但是需要注意，如果设置了replicas，则需要更多的结点
# --replicas 1 需要6个结点
# --replicas 2 需要12个结点
$ sudo src/redis-trib.rb create --replicas 1 127.0.0.1:6379 127.0.0.1:6380 127.0.0.1:6381 ip:port....


# 检查集群状态
$ sudo src/redis-trib.rb check 127.0.0.1:6379
Connecting to node 127.0.0.1:6379: OK
Connecting to node 127.0.0.1:6380: OK
Connecting to node 127.0.0.1:6381: OK
>>> Performing Cluster Check (using node 127.0.0.1:6379)
M: 50eee84811854ce707bb25ce05f1688eafa46c8d 127.0.0.1:6379
   slots:0-5460 (5461 slots) master
   0 additional replica(s)
M: 3cdc94999a66c325dd91ca4af70fa9a9fe1bc623 127.0.0.1:6380
   slots:5461-10922 (5462 slots) master
   0 additional replica(s)
M: 059fd2e13499b22aedfa0f0ad3707fe7534d96db 127.0.0.1:6381
   slots:10923-16383 (5461 slots) master
   0 additional replica(s)
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.

# 使用了集群之后，不能像以前一样使用命令行客户端了, 需要加参数`-c`
$ redis-cli
127.0.0.1:6379> ping
PONG
127.0.0.1:6379> set a b
(error) MOVED 15495 127.0.0.1:6381   # 设置失败

$ redis-cli -c
127.0.0.1:6379> set a b
-> Redirected to slot [15495] located at 127.0.0.1:6381
OK

# 同理python redis模块也是不能直接用集群模式了，需要替换成支持redis cluster的python模块
# 完毕
```


