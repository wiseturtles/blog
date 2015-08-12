Title: Elastichsearch数据备份，恢复，及迁移
Date: 2015-08-12 14:13
Category: Elasticsearch
Tags: elasticsearch, snapshot, restore, transfer
Slug: elasticsearch-snapshot-restore
Authors: craygit
Summary: Elastichsearch数据备份，恢复，及迁移


### 参考资料:

* <https://www.elastic.co/guide/en/elasticsearch/guide/current/backing-up-your-cluster.html>
* <https://www.elastic.co/guide/en/elasticsearch/guide/current/\_restoring_from_a_snapshot.html>
* <https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-snapshots.html>
* <https://www.elastic.co/blog/introducing-snapshot-restore>
* <http://stackoverflow.com/questions/27903929/elasticsearch-snapshot-across-cluster>


最近工作需要，要将一个索引的数据迁移到新的另一个集群，查阅了一些资料过后，便开始操作。由于数据量大，整个过程也花费了不少时间，遇到一些坑，特此整理一下整个过程。


### 迁移注意事项

* 保证ES集群不再接受新的数据(如果是备份的话，这一点可以不考虑，但是做数据迁移的话，建议这样做）.
* 不建议直接在生产环境做这些操作，最好是先在本地搭建一个和生产环境一样的集群环境，创建一些测试数据，把整个过程先跑一遍，然后再到生产环境操作。


本文假设ES集群有3个节点，IP分别是: 192.168.0.1, 193.168.0.2, 192.168.0.3

### 注册快照仓库

ES是通过快照的方式来实现数据备份，并且是以增量的方式，所以一般第一次做的话会花费较长的时间。为了做快照，那么就需要注册一个快照仓库，告诉ES我们的快照应该如何保存以及将快照保存到哪里.

ES的快照仓库支持如下几种形式：

* 共享的文件系统，如NAS
* Amazon S3
* HDFS (Hadoop Distributed File System)
* Azure Cloud

通常选择注册第一种形式。

任意选择一个节点，执行如下命令

```bash
$ curl -XPUT  http://192.168.0.1:9200/_snapshot/my_backup -d '
{
    "type": "fs",
    "settings": {
        "location": "/data/backups/elasticsearch"
    }
}
'
```

这样就注册了一个名为`my_backup`的仓库，这里的`location`需要注意，最好是设置一个每个节点都能访问并且有写权限的共享目录，如smb目录等(如果整个集群就一个节点那么设置为本地目录也无所谓)。
我自己在做的时候由于设置了本地目录`/data/backups/elasticsearch`, 最后做出来发现快照被分别保存在集群每个节点的`/data/backups/elasticsearch`目录下，并且一个节点保存了一些信息。最后做数据迁移的时候，不得不从每个节点将快照文件拷贝出来，然后合并到一起。

除了`location`外，还有一些其他选项可以设置:

* compress 是否压缩
* max_snapshot_bytes_per_sec 制作快照的速度，默认20mb/s
* max_restore_bytes_per_sec  快照恢复的速度，默认20mb/s


更新仓库设置如下:

```bash
curl -XPOST http://192.168.0.1:9200/_snapshot/my_backup/
{
    "type": "fs",
    "settings": {
        "location": "/data/backups/elasticsearch",
        "max_snapshot_bytes_per_sec" : "50mb",
        "max_restore_bytes_per_sec" : "50mb",
        "compress" : true
    }
}

```
这里需要注意一点是，注册仓库用的是`PUT`, 而更新仓库设置用的是`POST`.

### 检查注册的仓库信息

```bash
$ curl -XGET http://192.168.0.1:9200/_snapshot/my_backup
```

### 开始备份

指定快照名称为`snapshot_20150812`
```bash
$ curl -XPUT  http://192.168.0.1:9200/_snapshot/my_backup/snapshot_20150812

```
执行上面的上面的命令会马上返回，并在后台执行备份操作, 如果想等到备份完成，可以加上参数`wait_for_completion=true`

```bash
$ curl -XPUT  http://192.168.0.1:9200/_snapshot/my_backup/snapshot_20150812?wait_for_completion=true
```

默认是备份所有的索引indices, 如果要指定index,可以

```bash
curl -XPUT http://192.168.0.1:9200/_snapshot/my_backup/snapshot_20150812
{
    "indices": "index_1,index_2"
}
```

这个备份过程需要的时间视数据量而定.


### 查看备份状态

整个备份过程中，可以通过如下命令查看备份进度

```bash
curl -XGET http://192.168.0.1:9200/_snapshot/my_backup/snapshot_20150812/_status
```

主要由如下几种状态：

* INITIALIZING  集群状态检查，检查当前集群是否可以做快照，通常这个过程会非常快
* STARTED  正在转移数据到仓库
* FINALIZING 数据转移完成，正在转移元信息
* DONE　完成
* FAILED 备份失败

### 取消备份

```bash
curl -XDELETE http://192.168.0.1:9200/_snapshot/my_backup/snapshot_20150812
```

### 恢复备份

```bash
curl -XPOST http://192.168.0.1:9200/_snapshot/my_backup/snapshot_20150812/_restore
```

同备份一样，也可以设置wait_for_completion=true等待恢复结果
```bash
curl -XPOST http://192.168.0.1:9200/_snapshot/my_backup/snapshot_20150812/_restore?wait_for_completion=true

```

默认情况下，是恢复所有的索引，我们也可以设置一些参数来指定恢复的索引，以及重命令恢复的索引，这样可以避免覆盖原有的数据.

```bash
curl -XPOST http://192.168.0.1:9200/_snapshot/my_backup/snapshot_20150812/_restore
{
    "indices": "index_1",
    "rename_pattern": "index_(.+)",
    "rename_replacement": "restored_index_$1"
}
```

* 上面的indices, 表示只恢复索引'index_1'
* rename_pattern: 表示重命名索引以'index_'开头的索引.
* rename_replacement: 表示将所有的索引重命名为'restored_index_xxx'.如index_1会被重命名为restored_index_1.


### 查看恢复进度

```bash
# 查看所有索引的恢复进度
curl -XGET http://192.168.0.1:9200/_recovery/

# 查看索引restored_index_1的恢复进度
curl -XGET http://192.168.0.1:9200/_recovery/restored_index_1
```

### 取消恢复

只需要删除索引，即可取消恢复
```bash
curl -XDELETE http://192.168.0.1:9200/restored_index_1
```


### 备份快照迁移

如果需要将快照迁移到另一个集群.只需要将备份文件全部拷贝到要迁移的机器上, 然后再在新的集群上注册一个快照仓库,设置`location`的位置为备份文件所在的地方，然后执行恢复备份的命令即可。
