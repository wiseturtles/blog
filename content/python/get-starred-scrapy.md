Title: Scrapy入门
Date: 2015-08-27 15:47
Tags: python, scrapy
Slug: get-started-scrapy
Author: crazygit
Summary: scrapy入门
status: draft

## 常用命令

```bash
# 运行一个爬虫
$ scrapy runspider stackoverflow_spider.py -o top-stackoverflow-questions.json

# 创建项目
$ scrapy startproject tutorial

# 开始爬取
$ scrapy crawl dmoz


```

## 有用的代码片段

* <http://snipplr.com/all/tags/scrapy/>


## 命令行工具

命令行工具运行时会加载Scrapy的配置文件，加载顺序如下：

* 系统级别: /etc/scrapy.cfg 或 c:\scrapy\scrapy.cfg
* 用户级别: ~/.config/scrapy.cfg ($XDG_CONFIG_HOME) 或 ~/.scrapy.cfg ($HOME)
* 项目级别: scrapy.cfg

常用命令

```
# 创建项目
$ scrapy startproject <project_name>

# 创建爬虫
$ scrapy genspider [-t template] <name> <domain>

# 运行爬虫
$ scrapy crawl <spider>

# contract检查
$ scrapy check [-l] <spider>

# 列出可用的爬虫
$ scrapy list

# 使用`EDITOR`编辑爬虫
$ scrapy edit <spider>

# 下载链接
$ scrapy fetch <url>

# 使用浏览器打开链接
$ scrapy view <url>

# 进入命令行交互环境(如果有装ipython则使用ipython)
$ scrapy shell

# 解析URL
$ scrapy parse <url> [options]


# 获取设置信息
$ scrapy settings [options]

# 运行一个爬虫
$ scrapy runspider <spider_file.py>

# 运行测试用例
$ scrapy bench
```

自定义命令

设置`COMMANDS_MODULE = 'mybot.commands'`

命令的定义方式可以参考
<https://github.com/scrapy/scrapy/tree/master/scrapy/commands>


## 蜘蛛分类

* scrapy.spiders.Spider
* scrapy.spiders.CrawlSpider
* scrapy.spiders.XMLFeedSpider
* crapy.spiders.CSVFeedSpider
* scrapy.spiders.SitemapSpider

## 选择器

* Xpath
        - [Xpath指南](http://www.zvon.org/comp/r/tut-XPath_1.html)
        - [Xpath使用技巧](http://blog.scrapinghub.com/2014/07/17/xpath-tips-from-the-web-scraping-trenches/)

* CSS

可以使用`BeautifulSoup`和`lxml`来解析网页
使用Xpath取不到想要的节点时，需要考虑命名空间的影响


## Items
<http://doc.scrapy.org/en/1.0/topics/items.html>

## ItemLoaders
<http://doc.scrapy.org/en/1.0/topics/loaders.html>
输入输出的处理器优先级(由高到低)
ItemLoader field属性 > Item input_processor 或output_processor > ItemLoader的default_input_processor 和defualt_output_processor


## Scrapy Shell

可以在Spider代码中使用shell

```
from scrapy.shell import inspect_response
inspect_response(response, self)
```


## 调试技巧

* 使用
```
# 调试CrawlSpider的Rules
scrapy parse --spider=douban --noitems http://movie.douban.com/top250
```

## 其他
* [scrapyd](http://scrapyd.readthedocs.org/en/latest/)
* [scrapyrt](https://github.com/scrapinghub/scrapyrt)
* [scrapy-jsonrpc](https://github.com/scrapy-plugins/scrapy-jsonrpc)
