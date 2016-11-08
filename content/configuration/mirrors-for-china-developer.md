Title: 国内程序员常用镜像
Date: 2016-11-03 21:13
Tags: developer, mirrors
Slug: mirrors-for-china-developer
Author: ox0spy
Summary: mirrors for china developer

作为伟大国家中的一名码农，大家都经常会碰到莫名其妙的无法访问。所以，整理下我用的镜像。。

## mirrors

### 常使用的国内源

- [tuna](https://mirrors.tuna.tsinghua.edu.cn/)
- [aliyun](http://mirrors.aliyun.com/)
- [163](http://mirrors.163.com/)
- [ustc](https://mirrors.ustc.edu.cn/)

注：主流Linux的包都有同步。

### Python pypi

- Tuna: `https://pypi.tuna.tsinghua.edu.cn/simple`
- douban: `http://pypi.doubanio.com/simple/`
- ustc: `https://mirrors.ustc.edu.cn/pypi/web/simple/`

选一个访问最快的源，写到配置文件中：

    $ cat ~/.pip/pip.conf
    [global]
    index-url = https://pypi.tuna.tsinghua.edu.cn/simple

### NPM

使用 taobao 或者 tuna 的NPM源。

  # tuna 或者 taobao设置其一即可
  $ npm set registry https://registry.npm.taobao.org   # 淘宝
  $ npm set registry https://npm.tuna.tsinghua.edu.cn/ # tuna

  # 查看源设置
  $ npm get registry
  $ cat ~/.npmrc


### Java Maven

将如下源写到maven的conf/settings.xml文件中的mirrors节点中。

aliyun:

	 <mirror>
      	<id>alimaven</id>
      	<name>aliyun maven</name>
      	<url>http://maven.aliyun.com/nexus/content/groups/public/</url>
      	<mirrorOf>central</mirrorOf>
	</mirror>

### Java Gradle

创建 或 修改`~/.gradle/init.gradle` 文件，使用oschina 或者 aliyun 的源。

	
	$ cat ~/.gradle/init.gradle
	allprojects{
	  repositories {
	      // def REPOSITORY_URL = 'http://maven.oschina.net/content/groups/public'
	      def REPOSITORY_URL = 'http://maven.aliyun.com/nexus/content/groups/public/'
	      all { ArtifactRepository repo ->
	          if(repo instanceof MavenArtifactRepository){
	              def url = repo.url.toString()
	              if (url.startsWith('https://repo1.maven.org/maven2') || url.startsWith('https://jcenter.bintray.com/')) {
	                  project.logger.lifecycle "Repository ${repo.url} replaced by $REPOSITORY_URL."
	                  remove repo
	              }
	          }
	      }
	      maven {
	          url REPOSITORY_URL
	      }
	  }
	}


### Ruby gem

ruby-china:

	$ gem sources -l # 查看当前使用的源
	$ gem sources --add https://gems.ruby-china.org/ --remove https://rubygems.org/ # 删除当前使用的源，并添加ruby-china的源；假设你当前使用的是rubygems.org

详情请移步[ruby-china gem](https://gems.ruby-china.org/)

### homebrew

请参考:

- [tuna homebrew](https://mirrors.tuna.tsinghua.edu.cn/help/homebrew/)
- [tuna homebrew-bottles](https://mirrors.tuna.tsinghua.edu.cn/help/homebrew-bottles/)

### iOS CocoaPods

请参考[用CocoaPods做iOS程序的依赖管理](http://blog.devtang.com/2014/05/25/use-cocoapod-to-manage-ios-lib-dependency/)

文章中提到的ruby gem源可以用上文中的替换。
