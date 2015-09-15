Title:  Golang评价
Date: 2015-09-15 13:47
Tags: go
Slug: golang-chaos
Author: ox0spy
Summary: 收集牛人对Golang的评价

### djvu9

> - 作为一具码了差不多20年C++的C++11爱好者，我觉得对于大部分后端半栈码农，golang才是未来的方向。C++缺乏可用的标准库，Java的问题是JVM，python/php没有static typing，这些问题看来都没什么解决希望。golang的toolchain，runtime和标准库，目前来看是配合的最好的没有之一。语言本身其实不太重要。

> - golang的最大特点就是方便，比如goroutine不用创建线程，chan通信不用消息队列，自带网络、压缩、加密、协议、编解码、图像、文本处理的库，全部用go实现所以交叉编译很简单，还有parser/serializer的支持，静态编译部署简单不担心运行库的版本问题。所以即使没有模版，代码累赘且丑也能接受了。 

> - 有人问JVM有什么问题。软件的基本原理就是"We can solve any problem by introducing an extra level of indirection"。但是抽象就会带来新的问题：维护成本，跟外界的交互限制，信息的缺失等，所以要调gc，jni会影响优化，debug起来麻烦。JVM当年要解决的问题现在都不存在了所以它自己就成问题了。
>> + 操作系统和体系结构的多样性减少，编译器基础设施的改进，以及开放源代码的发展。基本上现在换个平台重新编译下代码就好了。

### yinwang

- [对 Go 语言的综合评价](http://www.yinwang.org/blog-cn/2014/04/18/golang/)
