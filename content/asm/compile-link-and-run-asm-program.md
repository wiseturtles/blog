Title: 编译、链接、运行汇编程序
Date: 2016-06-17 00:09
Tags: asm, Linux
Slug: Compile-Link-and-Run-ASM-Program
Author: ox0spy
Summary: 编译、链接、运行汇编程序的小脚本


学习汇编过程中每次输入as, ld的一堆命令行参数编译、链接程序实在很麻烦。

所以，写个小脚本完成汇编程序的编译、链接及运行。


	#!/bin/bash -e

    function usage()
    {
        echo "usage: $0 <asm-file-path>, the <asm-file-path> must end by '.s'"
        exit 0
    }

    test $# -ne 1 && usage

    if ! echo $1 | grep -Eq '\.s$'; then
        usage
    elif [ ! -f $1 ]; then
        echo "can not access the asm source code: <$1>"
        usage
    fi

    src="$1"
    dir="$(dirname $src)"
    basename="$(basename -s '.s' $src)"
    obj="$dir/${basename}.o"
    bin="$dir/$basename"
    as_opts="--32"
    ld_opts="-m elf_i386"

    # check if .global label is not the default "_start"; if not "_start", then using "-e label"
    global_label="$(grep -Eo '\.globl\s+\w+' $src | awk '{print $NF}')"
    if [ x"$global_label" != x"_start" ]; then
        ld_opts="$ld_opts -e $global_label"
    fi

    # if asm source code invoke C stdlib, then link C stdlib
    if grep -qE '\s+call\s+\w+' "$src"; then
        ld_opts="$ld_opts -lc -dynamic-linker /lib32/ld-linux.so.2"
    fi

    echo "as $as_opts -o $obj $src"
    as $as_opts -o $obj $src
    echo "ld $ld_opts -o $bin $obj"
    ld $ld_opts -o $bin $obj
    echo "run $bin ..."
    $bin


注：上篇文章已经讲过学习资料是AT&T 32位汇编，而个人电脑是64位系统，所以，指定了 `as --32` 和 `ld -m elf_i386`。
