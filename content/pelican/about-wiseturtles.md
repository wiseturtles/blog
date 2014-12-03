Title: 如何发表文章
Date: 2014-12-03 00:04
Tags: pelican, blog, github
Slug: about-wiseturtles
Author: crazygit
Summary: 如何在本博客发表文章


## 为什么要有这个博客

方便知识的整理，分享和交流。更主要的是慢慢感觉年纪越来越大(黑线！！！)，记性越来越差，需要一个可以记录东西的地方.

古话说得好
> 好记性不如烂笔头嘛!


## 名字的由来

为什么取名叫Wise Turtles？在这里我不得不吐槽一下咯。取名字，本来就是一件很难的事情，取一个有意义的名字就更难了，让一个理工宅男来取就难到吐血啦。
为了取一个有意义的名字，同时又能注册到域名和github组织名，我简直是使出了吃奶的力气, 从dota3一直试到了dota100， 域名都被注册了，想死的心都有。
伤心欲绝时，突然灵光一闪，想到了不久前热映的电影《忍者神龟》， 四兄弟团结, 幽默, 充满活力, 这不是我们所追求的团队精神吗? 所以决定以忍者神龟作为名字啦！
悲剧的是turtles竟然也被注册了，坚持着不放弃的原则，我觉得我们团队的兄弟姐妹们比起忍着神龟更加睿智，于是就用Wise Turtles啦！（实在不想再为名字纠结咯），
赶紧去注册了域名和github组织名，大功告成！


## 如何加入组织

请大家把github的**用户名**（注意是用户名：而不是登陆邮箱）发给我， 我会逐一给大家发送邀请。然后大家用自己的账号登陆github，访问

<https://github.com/wiseturtles>

即可接受邀请。


## 博客的功能介绍

博客采用开源的[pelican](<http://blog.getpelican.com/)静态博客引擎，集成了Disqus评论，百度分享，百度统计(不要问我为什么用百度，你懂的)，支持Atom/RSS feeds
订阅，响应式布局（移动端访问排版依然良好），Travis-ci自动构建文章。文章格式支持Markdown， reStructuredText, html语法。通过jinjia定义主题模板，git版本控制，以及程序员喜欢的语法高亮。

附上一些常用语法的链接:

* [Markdown 语法说明 (简体中文版)](http://wowubuntu.com/markdown/index.html)
* [Rst语法](http://docutils.sourceforge.net/rst.html)


## 与博客有关的repo介绍

我们的blog主要用到了三个repo

* wiseturtles.github.io  (博客静态html文件库，也就是博客展示的最终库，由travis-ci自动修改, 不需要手动修改）
* blog     （博客源码库，大家平时写文章时需要提交的库）
* theme    （主题库，可以定制博客的排版，样式和布局, 感觉现在博客难看的同学可以修改）

大家平时主要使用到的也就是blog这个库，下面就blog的目录结构简单介绍一下。

    :::bash
    # 下载blog库
    $ git clone --recursive git@github.com:wiseturtles/blog.git
    $ cd blog
    $ tree -aL 1
    .
    ├── cache       # 编译生成静态文件的cache库，加快编译速度
    ├── content     # 博客内容库，所有写的文章都按照目录来分类并放在这个目录下面
    ├── deploy.sh   # 部署编译出来的静态文件到wiseturtles.github.io库的脚本，由travis-ci调用
    ├── develop_server.sh
    ├── fabfile.py  # 封装了常用命令的fab文件
    ├── Makefile    # 封装了常用命令的makefile文件
    ├── output      # 编译生成静态html文件的目录，wiseturtles.github.io库里的内容就是这个目录下的
    ├── pelicanconf.py  # 博客的配置文件
    ├── publishconf.py  # 博客发布时调用的配置文件, 主要覆盖了pelicanconf.py里的一些配置
    ├── README.md
    ├── requirements.txt  # 记录安装本库需要使用的python包文件
    ├── theme       # 主题目录，其实就是theme库，作为一个子库放在blog里面
    └── .travis.yml # travis-ci的配置文件


所有的文章写好之后，都要放到coetent目录下， 所有的文章按照目录分类，可以根据自己的需要在content下创建需要的目录(目录名会出现在URL中，建议是英文的）。

## 如何搭建本地环境

为了使整个过程简洁，下面以**本地python版本为2.7.X, 不创建python虚拟为前提**。
如果不满足这两个条件，可以参考我的另一片文章 [pelican + github 搭建个人Blog](http://blog.wiseturtles.com/posts/setup-pelican.html)

    :::bash
    $ git clone --recursive git@github.com:wiseturtles/blog.git  # 下载代码
    $ cd blog
    $ sudo pip install -r requirements.txt  # 安装必要的python库, 如果不需要本地预览的话，可以跳过这一步
    $ touch content/test/hello.md   # 此处略去编辑content/test/hello.md文件过程的三千字
    $ make devserver    # 启动本地预览的server， 访问http://127.0.0.1:8000/查看文章那个效果
    # 重复上面两个步骤,直到决定发布文章
    $ git add content/test/hello.md
    $ git commit -m "add hello.md"
    $ git push origin master

OK， 打完收工！ 过一会访问我们的博客<http://blog.wiseturtles.com/>就可以看到自己刚刚发表的文章啦!

整个过程概述起来就跟把大象放进冰箱一样简单，只需要三步：

1. 下载blog代码
2. 写好文章
3. 提交文章


## 在线环境

如果感觉搭建本地环境麻烦的话，那就直接用github的在线编辑功能吧。
访问

<https://github.com/wiseturtles/blog>

即可在线编辑.


## 文件模板

无论选择Markdown， reStructuredText, html哪种语法，文章模板都应该像下面这样：

### reStructuredText（Rst）格式（文件名以.rst结尾）

<pre>
My super title
##############

:date: 2010-10-03 10:20
:modified: 2010-10-04 18:40
:tags: thats, awesome
:category: yeah
:slug: my-super-post
:authors: Alexis Metaireau, Conan Doyle
:summary: Short version for index and feeds

This is the content of my super blog post.
</pre>

### md格式(文件名以 .md, .markdown, .mkd, .mdown结尾）

<pre>
Title: My super title
Date: 2010-12-03 10:20
Modified: 2010-12-05 19:30
Category: Python
Tags: pelican, publishing
Slug: my-super-post
Authors: Alexis Metaireau, Conan Doyle
Summary: Short version for index and feeds

This is the content of my super blog post.

</pre>

### html格式(文件名以.html and .htm结尾）

<pre>
&lt;html&gt;
&lt;head&gt;
&lt;title&gt;My super title&lt;/title&gt;
&lt;meta name="tags" content="thats, awesome" /&gt;
&lt;meta name="date" content="2012-07-09 22:28" /&gt;
&lt;meta name="modified" content="2012-07-10 20:14" /&gt;
&lt;meta name="category" content="yeah" /&gt;
&lt;meta name="authors" content="Alexis Métaireau, Conan Doyle" /&gt;
&lt;meta name="summary" content="Short version for index and feeds" /&gt;
&lt;/head&gt;

&lt;body&gt;
This is the content of my super blog post.
&lt;/body&gt;
&lt;/html&gt;
</pre>


从上面的模板可以看出，无论选择哪种语言，都包含了共同的信息.

**需要注意的一点是slug标签的信息就是文章的URL链接，最好不要是中文的**


## 代码高亮

对于Rst格式, 用如下格式

<pre>

.. code-block:: identifier

   &lt;indented code block goes here&gt;

</pre>

md格式

<pre>

A block of text.

    :::identifier
    &lt;code goes here&gt;

</pre>


## 图片和附件管理

一般不建议将文章中要使用到的图片或附件提交到blog库中，避免引起blog库迅速增大， blog库建议只保存纯文本的东西。可以将要使用的图片或附件上传到支持外链的第三方存储，然后在文正里直接引用图片或附件的URL。或者单独建立一个git库来保存图片和附件。


## 最后

这里只是介绍了大体上的一些用法，更多请参阅: <http://docs.getpelican.com/en/3.5.0/content.html>
