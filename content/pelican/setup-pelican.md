Title: pelican + github 搭建个人Blog
Date: 2014-11-30 22:42
Tags: pelican, blog, github
Slug: setup-pelican
Author: crazygit
Summary: how to use pelican to setup personal blog


## 为什么选择Pelican

想搭建一个博客，不想受门户网站博客的限制，想用更纯净的方式写作，方便数据转移，
专注内容而不是格式，在这个页面<https://www.staticgen.com>罗列了各种语言的静态博客引擎, 最终选择了Pelican，

为什么呢？
> 因为人生苦短，我用python


特色：

* 它是一个基于python语言的静态博客引擎
* 使用Jinjia作为主题的模板语言
* 支持Markdown, reStructuredText格式
* 其他特色


## 安装Pelican

> 官方入门指南：<http://docs.getpelican.com/en/latest/getting_started.html>.

本文以Pelican3.5为例，使用Pelican需要python环境，官方推荐的python版本是2.7.X，因此开始之前，最好是检查一下当前系统的python版本是否满足情况。

    :::bash
    $ python --version
    Python 2.7.6


### 创建虚拟环境

如果当前系统默认是2.7.X, 我们则可以直接创建一个虚拟环境来为安装pelican做准备。
关于python虚拟环境的创建，详细可以参考: <http://liuzhijun.iteye.com/blog/1872241>。

下面说说主要步骤

    :::bash
    $ sudo pip install virtualenv virtualenvwrapper
    $ echo '[[ -s /usr/local/bin/virtualenvwrapper.sh ]] && source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc
    $ source ~/.bashrc
    $ mkvirtualenv pelican # 创建名字为pelican的虚拟环境，这里可以将pelican替换成任意你喜欢的名字
    $ workon pelican # 激活虚拟环境


另一个情况是当前系统默认python版本不是2.7.X的，
为了方便及不影响当前系统的python版本，可以使用[pythonbrew](https://github.com/utahta/pythonbrew)来搭建Python2.7.x环境。
安装步骤: <https://github.com/utahta/pythonbrew/blob/master/README.rst>

    :::bash
    # 安装pythonbrew
    $ curl -kL http://xrl.us/pythonbrewinstall | bash    # 这步执行成功后会生成目录: ~/.pythonbrew
    $ echo "[[ -s $HOME/.pythonbrew/etc/bashrc ]] && source $HOME/.pythonbrew/etc/bashrc" >> ~/.bashrc
    $ source ~/.bashrc
    $ pythonbrew --version      # 检查是否安装成功
    $ pythonbrew install --verbose 2.7.5       # 安装python 2.7.5
    $ pythonbrew use 2.7.5      # 临时在当前会话使用python 2.7.5
    $ which python              # 检查python版本信息是否正确

    # 一些关于pythonbrew的常用命令
    $ pythonbrew list           # 查看已经安装了的python版本
    $ pythonbrew off            # 禁用pythonbrew，使用系统默认的python环境
    $ pythonbrew list -k        # 查看pythonbrew提供了哪些python版本可以安装
    $ pythonbrew switch 2.7.5   # 永久切换到python 2.7.5,与use有点不同
    # 更多命令可以参考官方文档


 使用pythonbrew自带的virtualenv

    :::bash
    $ pythonbrew use 2.7.5
    $ pythonbrew venv init       # 初始化虚拟环境
    $ pythonbrew venv create pelican  # 创建名字为pelican的虚拟环境，这里可以将pelican替换成任意你喜欢的名字
    $ pythonbrew venv use pelican     # 开启虚拟环境

    # 为了以后使用方便,设置penv为开启虚拟环境的别名
    $ echo "alias  penv='pythonbrew use 2.7.5 && pythonbrew venv use pelican'" >> ~/.bashrc
    $ source ~/.bashrc

    # 一些常用的命令
    $ pythonbrew venv list
    $ pythonbrew venv use proj
    $ pythonbrew venv delete proj
    $ pythonbrew venv rename proj proj2
    $ pythonbrew venv clone proj proj2


### 安装pelican

在配置好了虚拟环境之后，就让我们进入虚拟环境安装pelican吧

    :::bash
    # 需要先激活虚拟环境
    $ workon pelican  # 如果是使用的pythonbrew ,则是“penv”
    $ pip install pelican markdown typogrif  # 安装必须的python包


## 博客配置

现在一切环境都好了，就让我们开始动手写博客吧

    :::bash
    $ mkdir myblog           # 创建一个目录，用于存放博客
    $ cd myblog
    $ pelican-quickstart     # 开始创建博客的向导

运行`pelican-quickstart`命令，会有一些问题，根据实际情况选择即可, 暂时不理解的也无所谓，直接回车就行了，后面都可以在配置文件里面修改。
通过上面的向导，博客的基本框架就建立起来了。

默认Pelican提供了Fabric文件和Makefile封装了常用操作, 可以根据自身的喜好选择。
下面介绍一些常用的make命令，以后会用得比较频繁。

<pre>
    $ make     # 直接运行make， 查看命令帮助

    make html                        (re)generate the web site(生成网站)
    make clean                       remove the generated files
    make regenerate                  regenerate files upon modification(每当本地文件被修改时，都自动生存网站）
    make publish                     generate using production settings
    make serve                       serve site at http://localhost:8000 （开始本地服务，可以通过http://localhost:8000查看）
    make devserver                   start/restart develop_server.sh (make regenerate 和make serve两个命令的集合）
    make stopserver                  stop local server (关闭本地服务)
    ssh_upload                       upload the web site via SSH
    rsync_upload                     upload the web site via rsync+ssh
    dropbox_upload                   upload the web site via Dropbox
    ftp_upload                       upload the web site via FTP
    s3_upload                        upload the web site via S3
    github                           upload the web site via gh-pages
</pre>


### 创建第一篇文章

说了这么多了，都还没有开始写呢，让我们开始写第一篇文章吧。
pelican 支持三种格式的文件，reStructuredText， markdown和html。
个人偏好于markdwon。下面就主要介绍markdown的吧，其他的可以到[官网查看](http://docs.getpelican.com/en/3.2/getting_started.html#kickstart-your-site).
上面写得很清楚。

创建第一篇文章，直接使用官网的例子。文章看起来应该大致像如下模板：

    Title: 文章标题
    Date: 2014-11-30 23:15(日期)
    Category: Python
    Tags: pelican, publishing
    Slug: my-super-post
    Author: crazygit
    Summary: hello

    这里是文章内容。
    ##你好，pelican

将上面的内容保存到`content`目录下，取名为`test.md`
。现在就要用到前面的命令了。

    $ make html
    $ make devserver

现在打开<http://localhost:8000/>，怎么样? 看到了我们的第一篇文章了吧。

### 配置文件修改

博客的配置通过修改`publishconf.py`
文件来实现，由于可以pelican比较灵活，可以配置的地方比较的多，就不介绍了，可以
查看[官方文档](http://docs.getpelican.com/en/3.2/settings.html)查找自己需要的
。其实，默认的配置基本上已经很好了，我自己除了在配置文件里面加上了时区之外，其他的基本上没有修改什么了。 
给一个官方的配置文件示例:

    # -*- coding: utf-8 -*-
    from __future__ import unicode_literals

    AUTHOR = 'Alexis Métaireau'
    SITENAME = "Alexis' log"
    SITEURL = 'http://blog.notmyidea.org'
    TIMEZONE = "Europe/Paris"

    # can be useful in development, but set to False when you're ready to publish
    RELATIVE_URLS = True

    GITHUB_URL = 'http://github.com/ametaireau/'
    DISQUS_SITENAME = "blog-notmyidea"
    PDF_GENERATOR = False
    REVERSE_CATEGORY_ORDER = True
    LOCALE = "C"
    DEFAULT_PAGINATION = 4
    DEFAULT_DATE = (2012, 3, 2, 14, 1, 1)

    FEED_ALL_RSS = 'feeds/all.rss.xml'
    CATEGORY_FEED_RSS = 'feeds/%s.rss.xml'

    LINKS = (('Biologeek', 'http://biologeek.org'),
            ('Filyb', "http://filyb.info/"),
            ('Libert-fr', "http://www.libert-fr.com"),
            ('N1k0', "http://prendreuncafe.com/blog/"),
            ('Tarek Ziadé', "http://ziade.org/blog"),
            ('Zubin Mithra', "http://zubin71.wordpress.com/"),)

    SOCIAL = (('twitter', 'http://twitter.com/ametaireau'),
            ('lastfm', 'http://lastfm.com/user/akounet'),
            ('github', 'http://github.com/ametaireau'),)

    # global metadata to all the contents
    DEFAULT_METADATA = (('yeah', 'it is'),)

    # static paths will be copied under the same name
    STATIC_PATHS = ["pictures", ]

    # A list of files to copy from the source to the destination
    FILES_TO_COPY = (('extra/robots.txt', 'robots.txt'),)

    # custom page generated with a jinja2 template
    TEMPLATE_PAGES = {'pages/jinja2_template.html': 'jinja2_template.html'}

    # foobar will not be used, because it's not in caps. All configuration keys
    # have to be in caps
    foobar = "barbaz"


### 主题安装

默认的博客主题是不是不符合你自己的胃口呢？没关系，pelican已经有很多漂亮的主题
供你选择了，在

<https://github.com/getpelican/pelican-themes>

已经有很多现成的主题了，打开每个主题的文件夹都有一张主题效果的截图，可以方便选择自己喜欢的主题。什么？这些主题都不满意。好吧，你还可以选择[创建属于自己独有的主题](http://docs.getpelican.com/en/3.2/themes.html#theming-pelican)。由于个人比较懒，信奉拿来主义，所以就选择了`tuxlite_tbs`这个主题，自己只做了一些细节的修改。

废话不多说，让我们开始安装主题吧。

    :::bash
    $ git clone git://github.com/getpelican/pelican-themes.git ~/pelican-themes # 下载主题到`~/pelican-themes/`目录下
    $ cd ~/pelican-themes/
    $ git submodule init  # 由于这个git库里面的一些主题是单独的一个子模块，所以将它们一起下载下来
    $ git submodule update

好了，现在已经有了所有的主题了，打开每个主题的文件夹都有一张主题效果的截图，选择自己喜欢的主题。

修改`publishconf.py` 文件，添加`THEME`关键字，如果已经有了，则直接修改值即可，我选择的是`tuxlite-tbs`

    THEME = "~/pelican-themes/tuxlite-tbs"

然后重新执行

    $ make html
    $ make devserver

访问<http://localhost:8000/>看看新的主题效果吧。

### 主题定制
新的主题怎么样呢？是不是还是有点遗憾呢？老外制作的主题总是弄Twitter，Google Plus等。这些东西虽然好，但是我们身在天朝，又用不上，要是我们能够把自己的新浪微博，QQ，等添加到自己的博客里面，看起来是不是更爽一点呢？ 下面就来添加吧!

### 添加新浪微博关注按钮

首先到[新浪开放平台](http://open.weibo.com/widget/followbutton.php)获取关注按钮的代码吧。在我使用的时候，它主要提供了两中样式，一种是WBML标准版，一种是JavaScript简化版本。在实际使用的时候发现JavaScript版本时候会有一些问题。
[提示client.js没有sendMessage方法](http://open.weibo.com/qa/index.php?qa=11802&qa_1=%E4%BD%BF%E7%94%A8%E5%85%B3%E6%B3%A8%E6%8C%89%E9%92%AEjavascript%E7%AE%80%E5%8C%96%E7%89%88%EF%BC%8C%E6%8F%90%E7%A4%BAclient-js%E6%B2%A1%E6%9C%89sendmessage%E6%96%B9%E6%B3%95&code=4b3704c5bce7d8cc46de2fe229687bdb).

因此下面主要介绍如何添加WBML标准版本的。取得类似下面的代码

    <wb:follow-button uid="2991975565" type="red_1" width="67" height="24" ></wb:follow-button>

注意上面的uid就是自己微博帐号的id，type就是选择的样式。
为了让这个代码有通用性。我将它修改为如下：

    <wb:follow-button uid="{{WEIBO_UID}}" type="{{WEIBO_TYPE}}" width="100%" height="64" ></wb:follow-button>

这样我们就可以通过在`pelicanconf.py`通过配置`WEIBO_UID`和`WEIBO_TYPE`灵活地设置帐号和样式。
将上面的代码保存在weibo.html文件中，并将文件保存到主题代码库的`~/pelican-themes/tuxlite-tbs/templates`目录下。
再修改这个目录下的base.html文件，引用我们的weibo.html。具体改动如下:

在HTML标签中增加XML命名空间

    <html xmlns:wb=“http://open.weibo.com/wb”>

在HEAD头中引入WB.JS

    <script src="http://tjs.sjs.sinajs.cn/open/api/js/wb.js" type="text/javascript" charset="utf-8"></script>

在需要显示微博关注按钮的地方includ刚刚的weibo.html，我把它添加在了社交下面.同时设置了WEIBO变量来设置是否显示微博关注按钮

    :::jinjia
    {% if WEIBO %}
    <div class="social">
    <div class="well" style="padding: 8px 0; background-color: #FBFBFB;">
    <ul class="nav nav-list">
        <li class="nav-header">
        新浪微博
        </li>
        {% include "weibo.html" %}
    </ul>
    </div>
    </div>
    {% endif %}

修改`pelicanconf.py`, 添加如下字段：

    :::python
    # 新浪微博新关注按钮
    WEIBO = True
    WEIBO_UID = 1768615155        # 填入uid
    WEIBO_TYPE = "red_3"

编译发布并预览。在本地预览的时候可能不会看到效果。需要发布到github pages上面才能看到.下面马上会讲如何部署到github上面.

    :::bash
    $ make html
    $ make devserver


### 部署到Github上面

如何利用github pages功能来创建个人的博客，网上和官网已经有很多教程了，就不再细讲具体步骤的，唯一需要注意的是，它主要分两类

*  用户级别的pages
*  项目级别的pages

上面两个不同之处是提交代码的时候一个是master分支，另一个是gh-pages分支.
因此，我们只需要将output 目录下的内容提交到上面的分支中。
为了做这件事情，我们可以使用前面介绍的ghp-import工具. 同时在我们的Makefile文件中也有封装这个命令
具体使用[参考这里](http://docs.getpelican.com/en/3.2/tips.html#publishing-to-github).

但是需要根据实际修改Makefile文件中的

    :::makefile
    github: publish
        ghp-import $(OUTPUTDIR)
        git push origin gh-pages   # 根据实际使用的pages情况修改这里

修改好了之后，可以直接使用`make github` 发布博客了.

我使用的用户级别的pages时，具体修改如下：

    :::bash
    $ cd myblog # 进入博客代码目录
    $ git init
    $ git remote add origin git@github.com:username/username.github.io.git # 需要替换username
    $ git add .
    $ git commit -m 'init pelican source code'
    $ penv  #打开虚拟环境
    $ make html 编译代码

修改Makefile文件如下内容：

    :::makefile
    github: publish
        ghp-import $(OUTPUTDIR) # 这一步会在本地创建一个gh-pages分支。并将OUTPUTDIR里面的内容拷贝到这个分支
        git push -f origin gh-pages:master
    # 注意我这里添加了参数f，在后面每次往master 分支提交代码的时候，如果有冲突，会强制覆盖master的代码

最后一步，提交代码

    :::bash
    $ make github

好了，打开你自己的github pages, 如<http://username.github.io/>查看效果。**注意**： 首次部署到github pages 需要等15分钟才有效


### 使用google在线字体

有些时候，我们想在文章中使用一些好看的字体，怎么办呢？伟大的Google替我们解决了这个问题，提供了[Google Web Fonts](http://www.google.com/fonts/)。
在这里可以选择一些好看的字体来用。怎么用也写得很清楚，就不再这里叙述了。
一些效果如下：
<p class="googlefont">Hello Google Web Fonts</p>
<p class="font-effect-fire-animation">Hello Google Fonts</p>

需要注意的是上面的字体有些老的浏览器不支持，所以在使用的时候注意下当前的浏览器是否支持这些字体。

### 图片添加

有时候，再多的语言，也比不上一张图片来得直白，虽然我们可以将图片直接放在写博客的代码库里面再直接引用。但是个人感觉这样做并不好。图片一多，代码库就明显变大。一点也不方便。最好的方法是选用一个第三方的图片托管，支持外链的。这样我们只需要在图片托管处上传图片，然后在博客里面引用即可。在网上搜寻一番之后，在[这里](http://c7sky.com/image-storage-server.html)找到了一些关于各种图片托管的介绍。在这里我选择了yupoo。大家也可以根据自己的需求任意选择一款。不说了，直接上图吧.

![第一张图片](http://pic.yupoo.com/crazygit/CQBeKErP/medish.jpg)

由于markdown语法本身没有代办设置图片布局，所以可以用html标签来设置

    <p align="center"><img src="http://pic.yupoo.com/crazygit/CQBeKErP/medish.jpg" title="Test Image"/></p>

<p align="center"><img src="http://pic.yupoo.com/crazygit/CQBeKErP/medish.jpg" title="Test Image"/></p>


### 添加文章评论系统，分享按钮，访问统计

这些步骤与添加新浪关注按钮一样，就不再赘述了。
这些设置再我当前使用的主题中都添加了，如果有需要的话大家可以[参考一下](https://github.com/crazygit/pelican-themes-tuxlite-tbs-mine)


### 其他功能

* 导入已经存在的博客
* 文字的多语言设置
* 个人私有文章和草稿箱
* 插件使用
* 标签云
* RSS订阅
* 文章分类
* ...

这些功能[官方文档](http://docs.getpelican.com)都有介绍，可以自己查找。


### 结束语

暂时使用到的功能就这么多了，以后有什么新的添加我会更新的，由于小弟也是刚刚接触这个，加上文笔不怎么好，如果有什么不明白的地方或错误的地方，欢迎留言，大家一起交流下。
