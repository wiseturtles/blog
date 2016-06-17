Title: Ubuntu+Vim配置汇编程序开发环境
Date: 2016-06-17 20:00
Tags: asm, Linux, Vim
Slug: setup-asm-development-environment
Author: ox0spy
Summary: 基于Ubuntu + Vim的汇编程序开发环境配置


本文专门介绍Ubuntu系统上基于Vim配置汇编程序开发环境。


## Ubuntu系统配置

所有开发都在Ubuntu上完成，需要用的软件包：binutils, gcc, gdb等软件。

Ubuntu上安装软件很方便，指令如下：

    $ sudo apt-get install binutils gcc gdb libc6-i386 libc6-dev-i386


## Vim配置

个人比较喜欢[k-vim](https://github.com/wklken/k-vim)，根据项目的安装文档安装即可。

汇编源代码的基本结构类似，每次都写一遍 `.section .data` 之类的很麻烦，通过下面补丁，新建汇编源文件时，自动加载模板：


	diff --git a/vimrc b/vimrc
    index e073d53..596bcc1 100644
    --- a/vimrc
    +++ b/vimrc
    @@ -580,7 +580,7 @@ autocmd FileType c,cpp,java,go,php,javascript,puppet,python,rust,twig,xml,yml,pe


    " 定义函数AutoSetFileHead，自动插入文件头
    -autocmd BufNewFile *.sh,*.py exec ":call AutoSetFileHead()"
    +autocmd BufNewFile *.sh,*.py,*.s exec ":call AutoSetFileHead()"
    function! AutoSetFileHead()
        "如果文件类型为.sh文件
        if &filetype == 'sh'
    @@ -593,9 +593,23 @@ function! AutoSetFileHead()
            call append(1, "\# encoding: utf-8")
        endif

    -    normal G
    -    normal o
    -    normal o
    +    "如果文件类型为asm
    +    if &filetype == 'asm'
    +        call setline(1, ".section .data")
    +        call append(1, ".section .text")
    +        call append(2, ".globl _start")
    +        call append(3, "_start:")
    +    endif
    +
    +    if &filetype == 'asm'
    +        normal G
    +        normal o
    +    else
    +        normal G
    +        normal o
    +        normal o
    +    endif
    +
    endfunc


## 在Ubuntu 64位系统上编译、运行32位汇编

之前提到过我学习的参考书籍讲的是32位AT&T汇编，而我的系统是64位，所以，这里介绍在64位Ubuntu上编译、运行32位汇编程序需要做那些配置。


### 64位Ubuntu编译、链接32位汇编程序

在 `~/.bashrc` 中添加下面的行：


    # asm i386
    alias as='as --32 -gstabs'
    alias ld='ld -m elf_i386'
    alias gcc='gcc -m32'


每次输入指令编译、运行、查看返回值也很麻烦，可以写个脚本自动完成这些工作，参考：[编译、链接、运行汇编程序](http://blog.wiseturtles.com/posts/Compile-Link-and-Run-ASM-Program.html)

注：

- 上面链接中提到的那坨脚本基本可以用 `gcc -m32 -o myhello myhello.s` 代替😂
- 如果用上面的gcc指令编译汇编代码，只能在汇编代码中使用`.globl main`；而不能使用as默认的`.globl _start`


### Vim

#### asm在Vim中的语法检查

[k-vim](https://github.com/wklken/k-vim)使用`syntastic`做语法检查，`syntastic`对asm源码默认检查会使用`as`编译源码，如果不指定`as --32`有些32位处理器特有的指令会引起报错。

现象就是每次在Vim中`:w`保存时，可能会报：`Error: invalid instruction suffix for 'push'` 或 `Error: 'jcxz' is not supported in 64-bit mode` 之类的错误。

可以在vim配置中指定`g:syntastic_asm_compiler_options`参数，避免错误，补丁如下:

	diff --git a/vimrc.bundles b/vimrc.bundles
    index c7428e8..7a4555d 100644
    --- a/vimrc.bundles
    +++ b/vimrc.bundles
    @@ -299,6 +299,9 @@ call plug#end()
        " let g:syntastic_javascript_checkers = ['jsl', 'jshint']
        " let g:syntastic_html_checkers=['tidy', 'jshint']

    +    " FIXME: if asm, 在64位系统上写32位汇编才需要
    +    let g:syntastic_asm_compiler_options = "--32"
    +


注：参考syntastic文档 - [ASM: gcc](https://github.com/scrooloose/syntastic/wiki/ASM:---gcc)


### 64位Ubuntu通过gcc生成C代码对应的32位汇编代码

直接通过gcc生成C代码对应的汇编代码只需`gcc -S`，但生成32位汇编代码就需要：


    $ gcc -m32 -S hello.c

注：需要安装`libc6-dev-i386`，否则会报错。
