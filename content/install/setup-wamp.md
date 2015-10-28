Title: WAMP(Windows + Apache + Mysql + PHP) 环境搭建
Date: 2013-09-30 13:44
Tags: php, wamp
Slug: setup-wamp
Author: crazygit
Summary: how to use pelican to setup wamp


最近开始学习PHP，工欲善其事，必先利其器。第一步当然是环境搭建啦！

PHP开发基本也就是在不同平台下，要么是LAMP(Linux + Apache + Mysql + PHP)，要么就是WAMP(Windows + Apache + Mysql +PHP), 
个人感觉在ubuntu环境下搭建环境比较简单，只需要一个命令

    $ sudo apt-get install -y apache2 mysql-server-5.5 php5 php5-gd php5-mysql php5-xdebug libapache2-mod-php5 phpmyadmin 

然后通过少许配置， LAMP环境就基本上搭建好了。系统默认帮我们做了很多事情，但是为了学习，我们还是尝试下在windows下搭建吧！虽然在windows下面也有很多WAMP的集成环境，如：
>XAMPP - XAMPP是一款具有中文说明的功能全面的集成环境，XAMPP并不仅仅针对Windows，而是一个适用于Linux、Windows、Mac OS X 和Solaris 的易于安装的Apache 发行版。软件包中包含Apache 服务器、MySQL、SQLite、PHP、Perl、FileZilla FTP Server、Tomcat等等。默认安装开放了所有功能，安全性有问题，需要进行额外的安全设定。
>
>WampServer - WampServe集成了Apache、MySQL、PHP、phpmyadmin，支持Apache的mod_rewrite，PHP扩展、Apache模块只需要在菜单“开启/关闭”上点点就搞定，省去了修改配置文件的麻烦。
>
>AppServ - 集成了Apache、PHP、MySQL、phpMyAdmin，较为轻量。
>
>总的来说，无论从安全性和性能上来讲，LAMP（Linux + Apache + MySQL + PHP）都优于WAMP（Windows + Apache + MySQL + PHP），不过由于Windows具有易用的特点，WAMP也未尝不是初学者的一个不错的选择。 
>

上面WAMP集成环境的内容介绍引用自  
<http://www.williamlong.info/archives/1281.html>

关于集成的开发环境，还不得不提到ZendServer， 这个也是一个相当不错的环境，相比XAMPP更加精简一些。

如果我们可以自己搭建一次整个开发环境的话，对这个过程将会更加熟悉。废话不多说，下面就让我们开始搭建吧！


## Apache安装

### 1.下载安装Apache包

根据http://httpd.apache.org/docs/2.4/platform/windows.html中如下一段话：

>The Apache HTTP Server Project itself does not provide binary releases of software, only source code. If you cannot compile the Apache HTTP Server yourself, you can obtain a binary package from numerous binary >distributions available on the Internet.
>Popular options for deploying Apache httpd, and, optionally, PHP and MySQL, on Microsoft Windows, include:
>
>•	ApacheHaus
>
>•	Apache Lounge
>
>•	WampServer
>
>•	XAMPP

从上面可以知道，Apache官方并没有提供windows下的二进制安装包，
可以从它推荐的站点下载apache二进制安装包。
在此选择  
<https://www.apachelounge.com/download/> 
网站上的  
<https://www.apachelounge.com/download/win32/binaries/httpd-2.4.4-win32.zip>

由于上面这个安装包是根据Visual Studio C++ 2010 SP1 VC10 环境下编译的。
>Be sure that you have installed the Visual C++ 2010 SP1 Redistributable Package x86 : VC10 SP1 vcredist_x86.exe

因此需要额外从
http://www.microsoft.com/en-us/download/confirmation.aspx?id=8328  

下载vcredist_x86.exe（这里根据自己的系统类型选择安装，我的是32位的系统，因此选择这个）

### 2. 安装和修改Apache配置文件

首先安装vcredist_x86.exe。再将下载的httpd-2.4.4-win32.zip解压到任意目录下，如：`D:\wamp\Apache24`.
修改配置文件`D:\wamp\Apache24\conf\httpd.conf`.

由于在`httpd.conf`中默认为httpd-2.4.4-win32.zip解压是解压到`c:\Apache24`目录下面的。
因此需要将`httpd.conf`文件中所有的`c:/Apache24`替换成`D:/wamp/Apache24`（**注意**:在`httpd.conf`文件中表示文件路径都是用的正斜杠，而不是反斜杠）。跟大部分网上讲的配置方法一样，在`httpd.conf` 中有如下几处是需要注意修改的

<pre>
    ServerRoot "D:/wamp/Apache24"  # apache服务器安装路径
    Listen 80                      # 服务器监听的端口
    ServerName localhost:80        # 服务器的域名，测试环境下一般是localhost
    ServerAdmin lianglin999@gmail.com   # 服务器维护人员的邮箱
    DocumentRoot "D:/wamp/Apache24/htdocs"  # 服务器的根目录
    &lt;Directory "D:/wamp/Apache24/htdocs"&gt;    # 这里和服务器的根目录路径一致
</pre>

### 3. 安装和启动Apache服务

先将`D:\wamp\Apache24\bin\`添加到系统环境变量中。方便后面安装和启动服务。
运行cmd窗口，执行如下命令

    httpd -k install -n service_name            # 安装apache服务 -n 是可选的，表示指定服务名字，不加-n使用默认的服务名字
    httpd -k start/stop/restart -n service_name # 运行/停止/重启 apache服务, 同样，如果上面没有使用-n参数，这里也可以省去
    httpd -k uninstall -n service_name          # 卸载apache服务
    net start/stop service_name                 # 也可以运行/停止 apache服务
    httpd -help                                 # 查看更多帮助信息

安装并运行Apache服务

    httpd -k install
    httpd -k start

如果没有修改配置文件中的默认80端口的话，访问  
<http://localhost/>
如果修改了端口号为8000，则访问    
<http://localhost:8000>

最后看到It works页面。表示apache服务器安装成功。
如果没有，请检查上述步骤是不是有什么错误。

## Mysql安装

### 1. 下载安装包

从<http://dev.mysql.com/downloads/>上面，可以获取Mysql的安装包，在Windows下面，Mysql的安装包主要有两种：一种是MySQL Community Server Windows msi安装包， 另一种是自己配置的zip包。
msi类型的的安装简单方面，根据需求选择，直接一直“下一步”就可以了。zip包您想的需要自己修改配置文件，在安装包解压路径下，复制my-default.ini到my.ini进行配置，具体配置内容可以网上查询。

在这里可以查看一篇别人介绍的[配置方法](
http://www.chenyudong.com/archives/installing-mysql-on-microsoft-windows-using-a-noinstall-zip-archive.html)

其实，也可以暂时不管配置什么的，先把Mysql用起来，需要的配置等要用时再来修改也不迟，那样印象更深刻，直接借鉴别人的配置，有些地方也不知道为什么要那么做。
所以，我的做法就是不管配置什么的，直接用吧。

### 2. 安装Mysql服务和使用

假设我使用的是zip包类型的Mysql，解压在`D:\wamp\mysql-5.6.13-win32\`目录下, 先把`D:\wamp\mysql-5.6.13-win32\bin`添加到环境变量，方便使用命令行。

运行CMD窗口，跟安装Apache服务类似，直接运行

    mysqld --install MySQL5.5(service_name)  # Mysql5.5 是service_name，是可选的，不指定的话它会默认使用一个服务名
    net start/stop MySQL5.5                  # 启动/停止Mysql服务
    mysqld --remove MySQL5.5                 # 移除Mysql服务

    # 更改Mysql数据库密码，第一次使用时，密码默认为空
    mysql -u root -p                        # 从命令行中进入mysql的客户端
    use mysql;                              # 使用mysql这个数据库
    update user set password=password("root_passwd") where user="root";      # 对root密码进行更改
    FLUSH PRIVILEGES;                       
    # 现在退出，便可以使用root_passwd密码登录了

更多安装细节可以查看[Mysql手册](http://dev.mysql.com/doc/refman/5.6/en/windows-installation.html)。

为了方便对数据库进行管理，我们可以安装phpmyadmin，一个web版本的Mysql数据库管理工具，具体安装方法网上比较多，也比较简单这里就不在讲解咯。

## PHP安装

### 1. 下载并配置

PHP安装包的版本分线程安全和非线程安全两种，具体两种有什么区别，网上有一大推讲解，本人也不是很了解，但是如果要使用apache服务器的话，只有下载线程安全的版本，非线程安全的版本没有php5apache2_4.dll文件。

根据PHP安装手册，在安装PHP的时候，需要先进行一些配置。假设我们将安装包解压在`D:\wamp\php-5.5.3-Win32-VC11-x86`。
首先复制`php.ini-development`为`php.ini`, 然后修改`php.ini`进行如下配置：

<pre>
# 把;error_log = php_errors.log 修改为
    error_log = D:\wamp\php-5.5.3-Win32-VC11-x86\logs

# ;date.timezone =修改为
    date.timezone = PRC
    
# 下面这2个,自己决定了
    post_max_size = 100M
# upload_max_filesize通常比post_max_size小
    upload_max_filesize = 50M
    
# 修改相关路径
# 上传暂存路径,别忘了创建对应的文件夹
    upload_tmp_dir = D:\wamp\php-5.5.3-Win32-VC11-x86\tmp\upload
    session.save_path = D:\wamp\php-5.5.3-Win32-VC11-x86\tmp\session
    extension_dir = D:\wamp\php-5.5.3-Win32-VC11-x86\ext

# 取消常用的扩展前面的分号注释
    extension=php_curl.dll
    extension=php_gd2.dll
    extension=php_mbstring.dll
    extension=php_mysql.dll
    extension=php_mysqli.dll
    extension=php_pdo_mysql.dll
</pre>
最后再创建相对应的目录`D:\wamp\php-5.5.3-Win32-VC11-x86\logs`,`D:\wamp\php-5.5.3-Win32-VC11-x86\tmp\upload`,`D:\wamp\php-5.5.3-Win32-VC11-x86\tmp\session`

最后，让apache认识php，修改apache的配置文件`D:\wamp\Apache24\conf\httpd.conf`添加下面的内容

    # php配置 
    LoadModule php5_module "E:/wamp_x64/php-5.5.3-Win32-VC11-x64/php5apache2_4.dll"
    AddHandler application/x-httpd-php .php

    # 配置 php.ini 的路径
    PHPIniDir "E:/wamp_x64/php-5.5.3-Win32-VC11-x64

    # 同时修改
    DirectoryIndex index.html index.php

在apache根目录下创建`D:/wamp/Apache24/htdocs/phpinfo.php`文件，内容如下:
<pre>
    &lt;?php phpinfo() ?&gt;
</pre>

重启apache服务，访问 http://localhost/phpinfo.php, 如果看到php相关信息，表示php安装成功。

## Xdebug安装

Xdebug 是一个PHP开发的调试工具，跟它齐名的另一个叫`Zend Debugger`, 也是一个很不错的东西。
安装xdebug，首先需要下载适合版本的xdebug，如果不知道自己应该下载哪个版本的话，可以将你phpinfo();方法得到的页面内容粘贴到[这里](http://xdebug.org/wizard.php)，它会自动分析出哪个版本的xdebug插件适合你。
将下载下来的dll文件保存到php的安装路径`D:\wamp\php-5.5.3-Win32-VC11-x86\ext`目录下，然后修改`D:\wamp\php-5.5.3-Win32-VC11-x86\php.ini`文件，添加如下内容：

    [XDebug]
    zend_extension = "D:\wamp\php-5.5.3-Win32-VC11-x86\extphp_xdebug.dll"
    xdebug.auto_trace = 1
    xdebug.collect_params = 1
    xdebug.collect_return = 1
    xdebug.profiler_append = 0
    xdebug.profiler_enable = 1
    xdebug.profiler_enable_trigger = 0
    xdebug.profiler_output_dir = "D:\wamp\php-5.5.3-Win32-VC11-x86\tmp"
    xdebug.profiler_output_name = "cachegrind.out.%t-%s"
    xdebug.remote_enable = 1
    xdebug.remote_handler = "dbgp"
    xdebug.remote_host = "localhost"
    xdebug.remote_port = 9000
    xdebug.trace_output_dir = "D:\wamp\php-5.5.3-Win32-VC11-x86\tmp"

最后，重新启动apache即可。访问phpinfo();页面检查是否有xdebug，如果有，表示安装成功。

## PHP集成开发环境

PHP的集成开发环境比较多: 如Zend Studio，Eclipse + PDT， Eclipse + PHPEclipse等。这些环境经过简单的配置之后都支持远程调试，还有一些浏览器的工具，如FireFox浏览器的"FireBug + FirePHP"插件，这些资料比较多，就不在这里重复了。

