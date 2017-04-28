Title: 在Mac OSX上安装Hadoop
Date: 2017-04-28 13:00
Tags: Mac, Hadoop, BigData
Slug: install-hadoop-on-mac-osx
Author: ox0spy
Summary: install hadoop on mac osx

## 安装Hadoop

我希望尽可能的通过包管理安装软件，而不是手动下载安装。

	$ brew install hadoop

### 修改配置文件

Hadoop安装路径: `brew --prefix hadoop` 。

配置文件路径: `$(brew --prefix hadoop)/libexec/etc/hadoop/`。

**core-site.xml:**

	<configuration>
		<property>
		    <name>fs.defaultFS</name>
		    <value>hdfs://localhost:9000</value>
		</property>
	</configuration>

**hdfs-site.xml:**

	<configuration>
		<property>
		    <name>dfs.replication</name>
		    <value>1</value>
		</property>
	</configuration>

**mapred-site.xml:**

	<configuration>
		<property>
		    <name>mapreduce.framework.name</name>
		    <value>yarn</value>
		</property>
	</configuration>

**yarn-site.xml:**

	<configuration>
		<property>
		    <name>yarn.nodemanager.aux-services</name>
		    <value>mapreduce_shuffle</value>
		</property>
	</configuration>

### 启动HDFS (NameNode, DataNode)

1. 格式化HDFS文件系统：`$ bin/hdfs namenode -format`
2. 启动NameNode 和 DataNode：`$ sbin/start-dfs.sh`
3. 创建HDFS目录，为运行MapReduce做准备

	```
	$ bin/hdfs dfs -mkdir /user
	$ bin/hdfs dfs -mkdir /user/<username>
	$ bin/hdfs dfs -put libexec/etc/hadoop input
	```

4. 运行demo:

	```
	$ bin/hadoop jar libexec/share/hadoop/mapreduce/hadoop-mapreduce-examples-2.8.0.jar grep input output 'dfs[a-z.]+'
	```

5. 查看demo输出: `$ bin/hdfs dfs -cat outpu/*`
6. 停止NameNode 和 DataNode: `$ sbin/stop-dfs.sh`

修改 ~/.zshrc ，将hadoop的bin, sbin加入PATH环境变量：

	# hadoop
	HADOOP_HOME=$(brew --prefix hadoop)
	export PATH="$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH"

### YARN (ResourceManager)

1. 启动:

	```
	$ sbin/start-yarn.sh
	```

2. 查看: [http://localhost:8088/](http://localhost:8088/)

3. 停止:

	```
	$ sbin/stop-yarn.sh
	```
