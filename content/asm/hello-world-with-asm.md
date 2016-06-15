Title: Hello World with asm
Date: 2016-06-15 22:09
Tags: asm, Linux
Slug: hello-world-with-asm
Author: ox0spy
Summary: Hello World with asm on Linux.

用汇编写个Hello World，同时看看如何一步一步将c程序编译成可执行文件。

## 开发环境准备

所有开发都在Ubuntu上完成，需要用的binutils, gcc, gdb。

Ubuntu上安装软件很方便，指令如下：

    $ sudo apt-get install binutils gcc gdb

## asm Hello World

用asm写个Hello World，.data数据段中定义msg变量为 "Hello World\n"，.text指令段从\_start开始，否则需要ld时指定-e label。
程序调用了printf输出msg，然后调用exit(0)退出。

	$ cat hello.s
    #hello.s Just a Hello World in asm.
    .section .data
    msg:
        .ascii "Hello World\n"
    .section .text
    .globl _start
    _start:
        movl $4, %eax
        movl $1, %ebx
        movl $msg, %ecx
        movl $12, %edx
        int $0x80
        movl $1, %eax
        movl $0, %ebx
        int $0x80
	$ as -o hello.o hello.s
	$ ld -o hello hello.o
	$ ./hello
    Hello World

## 下面看下如何一步一步编译、链接c程序

	$ cat helloc.c
    #include <stdio.h>
    #include <stdlib.h>

    int main()
    {
        printf("Hello World\n");
        exit(0);
    }

    $ gcc -S helloc.c
    $ as -o helloc.o helloc.s
    $ ld -e main -lc -dynamic-linker /lib64/ld-linux-x86-64.so.2 -o helloc helloc.o
    $ ./helloc
    Hello World

说明：
- gcc -S生成c代码对应的汇编代码，但是汇编代码中的.globl label为main
- 因为汇编代码的`.globl label`是`main`，所以必须使用`-e`参数指定label为`main`；默认是`_start`
- 因为汇编代码直接使用了c的库函数printf、exit，所以必须指定-lc链接c标准库
- -lc动态链接c标准库，所以，必须指定运行时加载动态库的程序，即：`-dynamic-linker /lib64/ld-linux-x86-64.so.2`

## asm Hello World (改进版)

既然汇编代码中可以直接调用c的标准库函数，那就看看怎么改进之前的hello.s。
下面代码调用c库中的puts和exit函数。
可以用gcc编译、链接汇编代码，而gcc默认只认`.globl main`而不是`.globl _start`，所以，我们下面用`.globl main`。

	$ cat new_hello.s
    #new_hello.s Just a "Hello World"
    .section .data
    msg:
        .string "Hello World"
    .section .text
    .global main
    main:
        movl $msg, %edi
        call puts
        movl $0, %edi
        call exit
    $ as -o new_hello.o new_hello.s
    $ ld -e main -lc -dynamic-linker /lib64/ld-linux-x86-64.so.2 -o new_hello new_hello.o
    $ ./new_hello
    Hello World

    $ gcc -o new_hello new_hello.s  # 当然可以直接用这条指令编译、链接生成可执行文件
