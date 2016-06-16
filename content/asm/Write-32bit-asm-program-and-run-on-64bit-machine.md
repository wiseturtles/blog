Title: 在64位机器上编写、运行32位汇编代码
Date: 2016-06-16 12:37
Tags: asm, Linux
Slug: Write-32bit-asm-program-and-run-on-64bit-machine
Author: ox0spy
Summary: 在64位机器上编写、运行32位汇编代码


我按照 `<<professional assembly language>>`（中文名为：编译语言程序设计) 学习汇编，但使用pushl在我的Ubuntu 64bit上报错`Error: invalid instruction suffix for 'push'`。
Google一圈发现需要在代码头部加上`.code32`，并且ld时需要额外指定些参数。


## 安装libc6-i386

ld链接时会用到libc-i386，所以，先安装并做个软链接。

    $ sudo apt-get install libc6-i386
    $ sudo ln -s /lib32/libc-2.19.so /lib32/libc.so

注：不做软链接可能会导致`ld -lc`报错：`ld: cannot find -lc`


## 在64位机器上编译、链接、运行32位汇编代码

源代码如下，代码中调用printf输出`Hello World\n`，然后调用exit(0)退出。

    $ cat myhello.s
	#myhello.s Just output "Hello World\n"
    .code32
    .section .data
    msg:
        .asciz "Hello World\n"
    .section .text
    .globl main
    main:
        pushl $msg
        call printf
        addl $4, %esp
        pushl $0
        call exit

    $ as --32 -o myhello.o myhello.s
    $ ld -e main -m elf_i386 -L/lib32 -lc -dynamic-linker /lib32/ld-linux.so.2 -o myhello myhello.o
    $ ./myhello
    Hello World


注：

- `as --32` 指定生成32位object文件
- `ld -e main` 因为程序中用了`.globl main` 而非 `.globl _start`，所以，用它指定汇编入口
- `ld -m elf_i386` 指定生成elf i386
- `-L/lib32 -lc`指定从`/lib32`目录下找`libc.so`；可以简写为`-lc`
- `-dynamic-linker /lib32/ld-linux.so.2` 指定操作系统用来动态地查找和加载库文件的程序


## 设置bash alias

每次都需要输入`as --32`和`ld -m elf_i386`很麻烦，我们可以通过bash alias简化输入。


    $ tail -2 ~/.bashrc
    alias as='as --32'
    alias ld='ld -m elf_i386'
    $ source ~/.bashrc
    $ as -o myhello.o myhello.s
    $ ld -e main -lc -dynamic-linker /lib32/ld-linux.so.2 -o myhello myhello.o
    $ ./myhello
    Hello World


这样就方便多了，当然也可以根据个人喜好把其它参数一起加入alias中。
