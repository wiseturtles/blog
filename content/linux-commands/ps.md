Title: ps
Date: 2015-01-13 09:51
Tags: linux, command, ps
Slug: linux-ps
Author: crazygit
Summary: the usage of ps


本文参考：

* [10 basic examples of Linux ps command](http://www.binarytides.com/linux-ps-command/)
* <http://man.linuxde.net/ps>


## 作用

ps命令用来列出系统中当前运行的那些进程。ps命令列出的是当前那些进程的快照，就是执行ps命令的那个时刻的那些进程，如果想要动态的显示进程信息，可以使用top命令
。


## 参数形式

* Unix风格的参数，前面加单破折线
* BSD风格的参数， 前面不加破折线
* GNU风格的长参数，前面加双破折线

不同风格的参数可以混合使用, 但是要注意避免冲突。

如:

命令`ps -aux`和`ps aux`是不一样的。`ps -aux`是显示所有'x'用户的进程, 如果用户'x'不存在的话，会给出警告，并当做`ps aux`来处理。

## 使用示例


1. 显示所有进程

        :::bash
        $ ps aux
        $ ps -ef

2. 显示指定用户的进程

        :::bash
        $ ps -f -u www-data

        # 多个用户用','隔开
        $ ps -f -u www-data,root

3. 按照进程名来指定

        :::bash
        $ ps -C nginx

    -C 选项必须提供精确的进程名，不提供模糊匹配，一般使用grep来搜索

        :::bash
        $ ps -ef |grep nginx

4. 按照进程id来查找

        :::bash
        $ ps -f -p 3150,7298,6455

5. 按照CPU或内存使用情况排序

    使用--sort选项可以按照一定的顺序排序，并且可以在指定的排序列前添加'-'或'+' 来指定降序或升序排列

        :::bash
        # cpu 使用前５
        $ ps aux --sort=-pcpu | head -5

        # 内存 使用前５
        $ ps aux --sort=-pmem | head -5

        # 指定多个排序
        $ ps jax --sort=uid,-ppid,+pid

    排序选项参见man page `STANDARD FORMAT SPECIFIERS`部分

    部分选项列出如下
    <pre>
    cmd          simple name of executable
    pcpu         cpu utilization
    pmem         ratio of the process's resident set size to the
                physical memory on the machine, expressed as a
                percentage
    flags        flags as in long format F field
    pgrp         process group ID
    tpgid        controlling tty process group ID
    cutime       cumulative user time
    cstime       cumulative system time
    utime        user time
    min_flt      number of minor page faults
    maj_flt      number of major page faults
    cmin_flt     cumulative minor page faults
    cmaj_flt     cumulative major page faults
    session      session ID
    pid          process ID
    ppid         parent process ID
    rss          resident set size
    resident     resident pages
    size         approximate amount of swap space that would be
                required if the process were to dirty all writable
                pages and then be swapped out. This number is
                very rough!
    share        amount of shared pages
    tty          the device number of the controlling tty
    start_time   time process was started
    uid          user ID number
    user         user name
    vsize        total VM size in kB
    priority     kernel scheduling priority
    </pre>

6. 按照树状结构显示

    使用`--forest`选项

        :::bash
        $ ps -f --forest -C nginx
        UID        PID  PPID  C STIME TTY          TIME CMD
        root      1344     1  0  2014 ?        00:00:00 nginx: master process /usr/sbin/nginx
        www-data  1345  1344  0  2014 ?        00:01:52  \_ nginx: worker process
        www-data  1346  1344  0  2014 ?        00:02:05  \_ nginx: worker process
        www-data  1348  1344  0  2014 ?        00:02:00  \_ nginx: worker process
        www-data  1349  1344  0  2014 ?        00:01:04  \_ nginx: worker process

    不要把`--forest`和`--sort`选项混合使用，因为他们都会影响结果

7. 列出子进程

        :::bash
        ＃先列出所有nginx进程
        $ ps -o pid,uname,comm -C nginx
        PID USER     COMMAND
        1344 root     nginx
        1345 www-data nginx
        1346 www-data nginx
        1348 www-data nginx
        1349 www-data nginx

        # 使用--ppid选项列出子进程
        $ ps --ppid 2359
        PID TTY          TIME CMD
        4524 ?        00:00:00 apache2
        4525 ?        00:00:00 apache2
        4526 ?        00:00:00 apache2
        4527 ?        00:00:00 apache2
        4528 ?        00:00:00 apache2

8. 列出进程的线程

    使用`-L`选项

        :::bash
        $ ps -p 3150 -L

9. 指定输出结果的列

    可以输出的列信息与`--sort`选项一样，可以查看man page 的`STANDARD FORMAT SPECIFIERS`部分

        :::bash
        $ ps -e -o pid,uname,pcpu,pmem,comm

        # 显示指定的列并给出别名
        $ ps -e -o pid,uname=USERNAME,pcpu=CPU_USAGE,pmem,comm

10. 将ps转变为实时更新的效果

        :::bash
        $  watch -n 1 'ps -e -o pid,uname,cmd,pmem,pcpu --sort=-pmem,-pcpu | head -15'

11. 部分选项解释

<pre>
-a： 显示所有终端机下执行的程序，除了阶段作业领导者之外。
a：  显示现行终端机下的所有程序，包括其他用户的程序。
-A： 显示所有程序。
-c： 显示CLS和PRI栏位。
c：  列出程序时，显示每个程序真正的指令名称，而不包含路径，选项或常驻服务的标示。
-C<指令名称>： 指定执行指令的名称，并列出该指令的程序的状况。
-d： 显示所有程序，但不包括阶段作业领导者的程序。
-e： 此选项的效果和指定"A"选项相同。
e：  列出程序时，显示每个程序所使用的环境变量。
-f： 显示UID,PPIP,C与STIME栏位。
f：  用ASCII字符显示树状结构，表达程序间的相互关系。
-g<群组名称>： 此选项的效果和指定"-G"选项相同，当亦能使用阶段作业领导者的名称来指定。
g：  显示现行终端机下的所有程序，包括群组领导者的程序。 -G<群组识别码>：列出属于该群组的程序的状况，也可使用群组名称来指定。
h：  不显示标题列。
-H： 显示树状结构，表示程序间的相互关系。
-j或j： 采用工作控制的格式显示程序状况。
-l或l： 采用详细的格式来显示程序状况。
L：  列出栏位的相关信息。
-m或m： 显示所有的执行绪。
n：  以数字来表示USER和WCHAN栏位。
-N： 显示所有的程序，除了执行ps指令终端机下的程序之外。
-p<程序识别码>： 指定程序识别码，并列出该程序的状况。
p<程序识别码>：  此选项的效果和指定"-p"选项相同，只在列表格式方面稍有差异。
r：  只列出现行终端机正在执行中的程序。
-s<阶段作业>：   指定阶段作业的程序识别码，并列出隶属该阶段作业的程序的状况。
s：  采用程序信号的格式显示程序状况。
S：  列出程序时，包括已中断的子程序资料。
-t<终端机编号>：  指定终端机编号，并列出属于该终端机的程序的状况。
t<终端机编号>：   此选项的效果和指定"-t"选项相同，只在列表格式方面稍有差异。
-T：   显示现行终端机下的所有程序。
-u<用户识别码>：  此选项的效果和指定"-U"选项相同。
u：  以用户为主的格式来显示程序状况。
-U<用户识别码>：  列出属于该用户的程序的状况，也可使用用户名称来指定。
U<用户名称>：  列出属于该用户的程序的状况。
v：  采用虚拟内存的格式显示程序状况。
-V或V：  显示版本信息。
-w或w：  采用宽阔的格式来显示程序状况。　
x：  显示所有程序，不以终端机来区分。
X：  采用旧式的Linux i386登陆格式显示程序状况。
-y：  配合选项"-l"使用时，不显示F(flag)栏位，并以RSS栏位取代ADDR栏位　。
-<程序识别码>：  此选项的效果和指定"p"选项相同。
--cols<每列字符数>：  设置每列的最大字符数。
--columns<每列字符数>：  此选项的效果和指定"--cols"选项相同。
--cumulative：  此选项的效果和指定"S"选项相同。
--deselect：  此选项的效果和指定"-N"选项相同。
--forest：  此选项的效果和指定"f"选项相同。
--headers：  重复显示标题列。
--help：  在线帮助。
--info：  显示排错信息。
--lines<显示列数>：  设置显示画面的列数。
--no-headers：  此选项的效果和指定"h"选项相同，只在列表格式方面稍有差异。
--group<群组名称>：  此选项的效果和指定"-G"选项相同。
--Group<群组识别码>：  此选项的效果和指定"-G"选项相同。
--pid<程序识别码>：  此选项的效果和指定"-p"选项相同。
--rows<显示列数>：  此选项的效果和指定"--lines"选项相同。
--sid<阶段作业>：  此选项的效果和指定"-s"选项相同。
--tty<终端机编号>：  此选项的效果和指定"-t"选项相同。
--user<用户名称>：  此选项的效果和指定"-U"选项相同。
--User<用户识别码>：  此选项的效果和指定"-U"选项相同。
--version：  此选项的效果和指定"-V"选项相同。
--widty<每列字符数>：  此选项的效果和指定"-cols"选项相同。
</pre>
