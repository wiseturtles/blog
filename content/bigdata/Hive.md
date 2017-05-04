Title: 在Mac OSX练习Hive
Date: 2017-05-04 13:00
Tags: Mac, Hive, BigData
Slug: learn-hive-on-mac-osx
Author: ox0spy
Summary: learn hive on mac osx

# Hive

## 安装

将Hive的metastore存在MySQL中。

Mac OSX 上安装 Hive

	$ brew install hive mysql
	$ brew services start mysql
	$ tail -n 3 ~/.zshrc
	# Hive
	export HIVE_HOME="/usr/local/opt/hive"
	export HCAT_HOME="$HIVE_HOME/libexec/hcatalog"
	$ source ~/.zshrc

为Hive在MySQL中创建数据库，并分配用户访问权限。

	$ mysql -u root -p
	mysql> create database metastore;
	mysql> grant all privileges on metastore.* to 'hive'@'localhost' identified by 'hive';

下载MySQL jdbc connector：

	$ wget -P /tmp/ https://cdn.mysql.com//Downloads/Connector-J/mysql-connector-java-5.1.42.tar.gz
	$ cd /tmp/ && tar zxf mysql-connector-java-5.1.42.tar.gz
	$ mv mysql-connector-java-5.1.42/mysql-connector-java-5.1.42-bin.jar $(brew --prefix hive)/libexec/lib/

修改 libexec/conf/hive-site.xml

	$ cd $(brew --prefix hive)
	$ cp libexec/conf/hive-default.xml.template libexec/conf/hive-site.xml
	$ 修改 hive-site.xml
	<property>
		<name>javax.jdo.option.ConnectionURL</name>
		<value>jdbc:mysql://localhost/metastore?useSSL=false</value>
		<description>
		JDBC connect string for a JDBC metastore.
		To use SSL to encrypt/authenticate the connection, provide database-specific SSL flag in the connection URL.
		For example, jdbc:postgresql://myhost/db?ssl=true for postgres database.
		</description>
	</property>
	<property>
   		<name>javax.jdo.option.ConnectionDriverName</name>
   		<value>com.mysql.jdbc.Driver</value>
		<description>Driver class name for a JDBC metastore</description>
	</property>
	<property>
		<name>javax.jdo.option.ConnectionUserName</name>
		<value>hive</value>
		<description>Username to use against metastore database</description>
	</property>
	<property>
		<name>javax.jdo.option.ConnectionPassword</name>
		<value>hive</value>
		<description>password to use against metastore database</description>
	</property>

运行 Hive：

	$ hive
	hive> show tables;

### 参考

- [Configuring the Hive Metastore](https://www.cloudera.com/documentation/enterprise/5-6-x/topics/cdh_ig_hive_metastore_configure.html)