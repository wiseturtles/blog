Title: uptime
Date: 2014-12-15 10:08
Tags: linux, command, uptime
Slug: linux-uptime
Author: crazygit
Summary: the usage of uptime


## 用途

man page

>uptime gives a one line display of the following information.  The cur‐
>rent time, how long the system has been running,  how  many  users  are
>currently  logged  on,  and the system load averages for the past 1, 5,
>and 15 minutes.
>
>
>System load averages is the average number of processes that are either
>in a runnable or uninterruptable state.  A process in a runnable  state
>is  either  using the CPU or waiting to use the CPU. A process in unin‐
>terruptable state is waiting for some I/O access, eg waiting for  disk.
>The  averages  are  taken over the three time intervals. Load averages
>are not normalized for the number of CPUs in a system, so a load  aver‐
>age  of 1 means a single CPU system is loaded all the time while on a 4
>CPU system it means it was idle 75% of the time.


*Load averages are not normalized for the number of CPUs in a system, so a load  aver‐ age  of 1 means a single CPU system is loaded all the time while on a 4 CPU system it means it was idle 75% of the time.*


## 语法

    :::bash
    $ uptime
    10:14:31 up 10 days, 20:55,  6 users,  load average: 0.28, 0.42, 0.54

上面的结果显示的分别是系统的当前时间，运行时间，当前用户数，过去1, 5, 15分钟的系统平均负载
总体来说，值为1时，当只有单个CPU表示已经完全利用，当有４个CPU时，表示还有75%的空闲.

关于平均负载的值可以阅读

<http://blog.scoutapp.com/articles/2009/07/31/understanding-load-averages>
