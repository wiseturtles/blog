#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
脚本作用:
解析从网页上复制的table html并转换成纯净的html样式
'''
from HTMLParser import HTMLParser
from BeautifulSoup import BeautifulSoup as bs


class TableHtmlParser(HTMLParser):

    table_tags = ['table', 'tr', 'td', 'tbody']
    table_class = "table table-striped table-bordered table-hover table-condensed"

    def __init__(self):
        HTMLParser.__init__(self)
        self.tidy_table = ""

    def handle_starttag(self, tag, attrs):
        if tag in self.table_tags:
            if tag == 'table':
                self.tidy_table += '<%s class="%s">' % (tag, self.table_class)
            else:
                self.tidy_table += "<%s>" % tag

    def handle_endtag(self, tag):
        if tag in self.table_tags:
            self.tidy_table += "</%s>" % tag

    def handle_data(self, data):
        self.tidy_table += data

    def pretty_table(self):
        soup = bs(self.tidy_table)
        return soup.prettify()

if __name__ == '__main__':

    table_html = '''
    <table class="ke-zeroborder" border="0" cellpadding="2" cellspacing="0" height="288" width="650">
<tbody>
<tr>
<td>
                上下键或PgUP, PgDn
            </td>
<td>
                选定想要的进程，左右键或Home, End 移动字段，当然也可以直接用鼠标选定进程
            </td>
</tr>
<tr>
<td>
                Space
            </td>
<td>
                标记/取消标记一个进程。命令可以作用于多个进程，例如 “kill”，将应用于所有已标记的进程
            </td>
</tr>
<tr>
<td>
                U
            </td>
<td>
                取消标记所有进程
            </td>
</tr>
<tr>
<td>
                s
            </td>
<td>
                选择某一进程，按s:用strace追踪进程的系统调用
            </td>
</tr>
<tr>
<td>
                l
            </td>
<td>
                显示进程打开的文件: 如果安装了lsof，按此键可以显示进程所打开的文件
            </td>
</tr>
<tr>
<td>
                I
            </td>
<td>
                倒转排序顺序，如果排序是正序的，则反转成倒序的，反之亦然
            </td>
</tr>
<tr>
<td>
                +, -
            </td>
<td>
                在树形模式下，展开或折叠子树
            </td>
</tr>
<tr>
<td>
                a (在有多处理器的机器上)
            </td>
<td>
                设置 CPU affinity: 标记一个进程允许使用哪些CPU
            </td>
</tr>
<tr>
<td>
                u
            </td>
<td>
                显示特定用户进程
            </td>
</tr>
<tr>
<td>
                M
            </td>
<td>
                按Memory使用排序
            </td>
</tr>
<tr>
<td>
                P
            </td>
<td>
                按CPU使用排序
            </td>
</tr>
<tr>
<td>
                T
            </td>
<td>
                按Time+使用排序
            </td>
</tr>
<tr>
<td>
                F
            </td>
<td>
                跟踪进程: 如果排序顺序引起选定的进程在列表上到处移动，让选定条跟随该进程。这对监视一个进程非常有用：通过这种方式，你可以让一个进程在屏幕上一直可见。使用方向键会停止该功能
            </td>
</tr>
<tr>
<td>
                K
            </td>
<td>
                显示/隐藏内核线程
            </td>
</tr>
<tr>
<td>
                H
            </td>
<td>
                显示/隐藏用户线程
            </td>
</tr>
<tr>
<td>
                Ctrl-L
            </td>
<td>
                刷新
            </td>
</tr>
<tr>
<td>
                Numbers
            </td>
<td>
                PID 查找: 输入PID，光标将移动到相应的进程上
            </td>
</tr>
</tbody>
</table>
    '''
    parser = TableHtmlParser()
    parser.feed(table_html)
    parser.close()
    print parser.pretty_table()
