Title: 在Mac OSX练习Pig使用
Date: 2017-05-03 13:00
Tags: Mac, Pig, BigData
Slug: learn-pig-on-mac-osx
Author: ox0spy
Summary: learn pig on mac osx

# Pig

看《Hadoop权威指南第三版》并记录在 Mac OSX 系统上练习Pig使用。

## 安装

在Mac OSX 上安装命令如下：

	$ brew install pig

## 命令行使用

## Pig Latin语言

Pig Latin的关系操作：

| 类型      | 操作  | 描述|
|----------|-------|----|
| 加载与存储 | LOAD  | 从文件系统或其他存储加载数据，存入关系 |
| 加载与存储 | STORE | 将一个关系存放在文件系统或者其他存储中 |
| 加载与存储 | DUMP  | 将关系打印到控制台 |
| 过滤      | FILTER| 将关系中删除不需要的行 |
| 过滤      | DISTINCT | 将关系中删除重复的行 |
| 过滤      | FOREACH ... GENERATE | 将关系中添加或删除字段 |
| 过滤      | MAPREDUCE | 以一个关系作为输入运行某个MapReduce 作业 |
| 过滤      | STREAM | 使用外部程序对一个关系进行变换 |
| 过滤      | SAMPLE | 对一个关系进行随机取样 |
| 分组与连接 | JOIN | 连接两个或多个关系 |
| 分组和连接 | COGROUP | 对两个或更多关系中的数据进行分组 |
| 分组和连接 | GROUP | 在一个关系中对数据进行分组 |
| 分组和连接 | CROSS | 创建两个或更多关系的乘积 (叉乘) |
| 排序      | ORDER | 根据一个或多个字段对某个关系进行排序 |
| 排序      | LIMIT | 将一个关系的元组个人限定在一定数量内 |
| 组合和切分 | UNION | 合并两个或多个关系为一个关系 |
| 组合和切分 | SPLIT | 把某个关系切分为两个或多个关系 |

Pig Latin的诊断操作

| 操作      | 描述  |
|----------|-------|
| DESCRIBE | 打印关系的模式 |
| EXPLAIN  | 打印逻辑和物理计划 |
| ILLUSTRATE | 使用生成的输入子集显示逻辑计划的试运行结果 |

注：

- 这些命令不会被加入逻辑计划中
- DUMP也是一种诊断操作

Pig Latin的宏和UDF语句

| 语句     | 描述    |
|----------|--------|
| REGISTER | 在Pig运行时环境中注册一个JAR文件 |
| DEFINE   | 为宏、UDF、流式脚本或命令规范新建别名 |
| IMPORT   | 把另一个文件中定义的宏导入脚本 |

注：

- 这些命令不处理关系，所以它们不会被加入逻辑计划
- 这些命令会被立即执行

Pig Latin 命令

|  类别         | 命令  | 描述                 |
|---------------|------|---------------------|
| Hadoop文件系统 | cat   | 打印一个或多个文件的内容 |
| Hadoop文件系统 | cd    | 改变当前目录 |
| Hadoop文件系统 | copyFromLocal | 复制本地文件或目录|
| Hadoop文件系统 | copyToLocal | 将一个文件或目录从Hadoop 文件系统复制到本地文件系统 |
| Hadoop文件系统 | cp | 把一个文件或目录复制到另一个目录 |
| Hadoop文件系统 | fs | 访问Hadoop文件系统外壳程序 |
| Hadoop文件系统 | ls | 打印文件列表信息 |
| Hadoop文件系统 | mkdir | 创建新目录 |
| Hadoop文件系统 | mv | 将一个文件或目录移动到另一个目录 |
| Hadoop文件系统 | pwd | 打印当前工作目录 |
| Hadoop文件系统 | rm | 删除一个文件或目录 |
| Hadoop文件系统 | rmf | 强制删除文件或目录 (文件或目录不存在也不会失败)|
| Hadoop MapReduce 工具 | kill | 终止某个MapReduce 作业 |
| Hadoop MapReduce 工具 | exec | 在新的 Grunt 外壳程序中以批处理模式运行脚本|
| Hadoop MapReduce 工具 | help | 显示可用的命令和选项 |
| Hadoop MapReduce 工具 | quit | 退出解释器 |
| Hadoop MapReduce 工具 | run | 在当前 Grunt 外壳程序中运行脚本 |
| Hadoop MapReduce 工具 | set | 设置 Pig 选项 和 MapReduce 作业属性 |
| Hadoop MapReduce 工具 | sh | 在 Grunt 中运行外壳命令 |

Pig Latin 表达式

| 类别 | 表达式 | 描述 | 示例 |
|-----|--------|-----|-----|
| 常量 | 文字  | 常量值 | 1.0, 'a' |
| 字段 (位置指定)| $n | 第n个字段(从0开始)| $0, $1 |
| 字段 (名字指定) | f | 字段名f | year |
| 字段 (消除歧义) | r::f | 分组或连接后，关系r中的名为f的字段 | A::year |
| 投影 | c.$n, c.f | 在容器c (关系、包或元组) 中的字段按位置 或 名称指定 |   records.$0, records.year |
| Map 查找 | m#k | 在映射m中键k所对应的值 | items#'Coat'
| 类型转换 | (t) f | 将字段f转换为类型t | (int) year |
| 算术 | +, -, *, /, % | 加、减、乘、除、取余 | $1 + $2, $1 - $2, $1 * $2, $1 / $2, $1 % $2 |
| 条件 | x ? y : z | 三元运算符，如果 x 为真，则y，否则为 z | quality == 0 ? 0 : 1 |
| 比较 | ==, !=, >, <, >=, <=, x matches y, x is null, x is not null | 相等、不等、大于、小于、大于等于、小于等于、正则匹配、是空值、不是空值 | `quality matches '[01459]'` |
| 布尔型 | or, and, not | 逻辑或，逻辑与，逻辑非 | `q == 0 or q == 1`, `not q matches '[01459]'` |
| 平面化 | FLATTEN(f) | 从包或元组中去除嵌套 | FLATTEN(group) |

Pig Latin 类型

| 类别 | 数据类型 | 描述 | 示例 |
|------|--------|------|-----|
| 数值 | int | 32位有符号整数 | 99 |
| 数值 | long | 64位有符号整数 | 199L |
| 数值 | float | 32位浮点数 | 0.8F |
| 数值 | double | 64位浮点数 | 0.88 |
| 文本 | chararray | UTF-16格式的字符数组 | 'hello world' |
| 二进制 | bytearray | 字节数组 | |
| 复杂类型 | tuple | 任何类型的字段序列 | (1, 'programmer') |
| 复杂类型 | bag | 元组的无序多重集合 (允许重复的元组) | {(1, 'hello'), (2)} |
| 复杂类型 | map | 一个键值对的集合。键必须是字符数组，值可以是任意类型的数据 | ['a'#'hello', 'b'#'world'] |

注：

- 内置函数：TOTUPLE, TOBAG, TOMAP 将表达式转换为元组、包以及映射。
- 包必须在某个关系中。

## Schema

Pig 中的一个关系可以关联一个模式。模式为关系的字段指定名称和类型。

Load语句的AS字句可以在关系上附以模式：

	grunt> records = LOAD 'input/ncdc/micro-tab/sample.txt' AS (year:int, temperature:int, quality:int);
	grunt> DESCRIBE records;
	records: {year:int,temperature:int,quality:int}
	
	注：不指定类型的话，默认是bytearray
	    DESCRIBE 用来查看模式 (Schema)

## 函数

Pig的函数有四种类型：

- 计算函数 (Eval function)
- 过滤函数 (Filter function)
- 加载函数 (Load function)
- 存储函数 (Store function)

## 宏

宏提供了在Pig Latin内对可重用的Pig Latin代码进行打包的功能。

示例：

	$ cat max_temp.macro
	DEFINE max_by_group(X, group_key, max_field) RETURNS Y {
	A = GROUP $X by $group_key;
	$Y = FOREACH A GENERATE group, MAX($X.$max_field);
	};

导入宏：

	grunt> IMPORT './max_temp.macro';

使用宏：

	grunt> records = LOAD '/input/ncdc/micro-tab/sample.txt' AS (year:chararray, temperature:int, quality:int);
	grunt> max_temp = max_by_group(records, year, temperature);
	grunt> DUMP max_temp;

## 用户自定义函数 (UDF)

以插件形式提供使用用户定制代码的能力。可以使用Java、Python、JavaScript写UDF。

下面是删除不符合质量要求的气温记录 (Java代码)：

	$ cat com/hadoopbook/pig/IsGoodQuality.java
	package com.hadoopbook.pig;
	
	import java.io.IOException;
	import java.util.ArrayList;
	import java.util.List;
	
	import org.apache.pig.FilterFunc;
	import org.apache.pig.backend.executionengine.ExecException;
	import org.apache.pig.data.DataType;
	import org.apache.pig.data.Tuple;
	import org.apache.pig.impl.logicalLayer.FrontendException;
	
	public class IsGoodQuality extends FilterFunc {
	
	  @Override
	  public Boolean exec(Tuple tuple) throws IOException {
	    if (tuple == null || tuple.size() == 0) {
	      return false;
	    }
	    try {
	      Object object = tuple.get(0);
	      if (object == null) {
	        return false;
	      }
	      int i = (Integer) object;
	      return i == 0 || i == 1 || i == 4 || i == 5 || i == 9;
	    } catch (ExecException e) {
	      throw new IOException(e);
	    }
	  }
	}

编译、打包：

	$ javac -cp $(brew --prefix pig)/libexec/pig-0.16.0-core-h2.jar:$(hadoop classpath) com/hadoopbook/pig/IsGoodQuality.java
	$ jar -cf com/hadoopbook/pig/IsGoodQuality.jar com/hadoopbook/pig/IsGoodQuality.class
	
	注：我通过brew安装的pig所以使用了$(brew --prefix pig)；可以手动指定pig.jar的具体路径。

在Pig中使用该UDF：

	$ pig
	grunt> REGISTER ./com/hadoopbook/pig/IsGoodQuality.jar;
	grunt> DEFINE isGood com.hadoopbook.pig.IsGoodQuality();
	grunt> records = LOAD '/input/ncdc/micro-tab/sample.txt' AS (year:chararray, temperature:int, quality:int);
	grunt> filtered_records = FILTER records BY temperature != 9999 AND isGood(quality);
	grunt> DUMP filtered_records;

写成pig程序：

	$ cat max_temp_filter_udf.pig
	--max_temp_filter_udf.pig
	REGISTER com/hadoopbook/pig/IsGoodQuality.jar;
	DEFINE isGood com.hadoopbook.pig.IsGoodQuality();
	records = LOAD '/input/ncdc/micro-tab/sample.txt' AS (year:chararray, temperature:int, quality:int);
	filtered_records = FILTER records BY temperature != 9999 AND isGood(quality);
	grouped_records = GROUP filtered_records BY year;
	max_temp = FOREACH grouped_records GENERATE group, MAX(filtered_records.temperature);
	DUMP max_temp;
	STORE max_temp INTO 'max_temp_output' USING PigStorage(':');

## 数据加载和存储

前面已经有用Load加载数据了。下面看看怎么存储数据：

	grunt> STORE max_temp INTO 'max_temp_output' USING PigStorage(':');
	grunt> cat max_temp_output

## 数据过滤

`FILTER` 、`LIMIT` 用来过滤行；`FOREACH ... GENERATE`用来删除、添加列(字段)。

	grunt> max_temp = FOREACH grouped_records GENERATE group, MAX(filtered_records.temperature);

### STREAM操作

STREAM操作可以让外部程序或脚本对关系中的数据进行变换。这一操作的命名对应于Hadoop的Streaming，后者为MapReduce提供类似能力。

	grunt> records = LOAD '/input/ncdc/micro-tab/sample.txt' AS (year:chararray, temperature:int, quality:int);
	grunt> second_field = STREAM records THROUGH `cut -f 2`;
	grunt> DUMP second_field;

#### Python写stream脚本

is_good_quality.py程序:

	$ cat is_good_quality.py
	#!/usr/bin/env python
	# encoding: utf-8
	import re
	import sys
	
	for line in sys.stdin:
	    (year, temp, q) = line.strip().split()
	    if temp != '9999' and re.match('[01459]', q):
	        print('{}\t{}'.format(year, temp))

Pig程序:
	
	$ cat max_temp_filter_stream.pig
	--max_temp_filter_stream.pig
	
	DEFINE is_good_quality `is_good_quality.py` SHIP ('is_good_quality.py');
	records = LOAD '/input/ncdc/micro-tab/sample.txt' AS (year:chararray, temperature:int, quality:int);
	filtered_records = STREAM records THROUGH is_good_quality AS (year:chararray, temperature:int);
	grouped_records = GROUP filtered_records BY year;
	max_temp = FOREACH grouped_records GENERATE group, MAX(filtered_records.temperature);
	DUMP max_temp;
	STORE max_temp INTO 'max_temp_stream';        

运行：

	$ hdfs dfs -put max_temp_filter_stream.pig
	$ pig -f max_temp_filter_stream.pig
	$ hdfs dfs -cat max_temp_stream/*
	1949	111
	1950	22

## 数据分组与连接

### 连接/JOIN

连接：

	grunt> C = JOIN A BY $0, B BY $1;
	
	注：等式连接，即：连接A.$0 == B.$1 的行，结果中的字段由所有输入关系的所有字段组成。

如果要连接的关系太大，不能全部放入内存，则应该使用通用的连接操作。如果有一个关系小到能够全部放入内存，则可以使用分段复制连接(fragment replicate join)，它把小的输入关系发生到所有mapper，并在map端使用内存查找表对(分段的)较大的关系进行连接。

分段复制连接：

	grunt> C = JOIN A BY $0, B BY $1 USING "replicated";
	
	注：第一个关系必须是大的关系，后面则是一个或多个相对较小的关系。(能够全部放入内存)

## 实战技巧

### 并行处理

Pig根据输入数据的大小设置reducer个数：每1GB 输入使用一个reducer，且 reducer 的个数不超过 999。可以设置 pig.exec.reducers.bytes.per.ducer 和 pig.exec.reducers.max 来修改默认设置。

为了告诉 Pig 每个作业要用多少个 reducer ，可以在 reducer 阶段的操作中使用 PARALLEL 子句。在 reduce 阶段使用的操作包括所有的 分组(grouping)、连接 (joining)操作(GROUP, COGROUP, JOIN, CROSS)以及DISTINCT 和 ORDER。

	grunt> grouped_records = GROUP records BY year PARALLEL 30;

也可以通过设置 default_paralle 选项达到相同效果：

	grunt> set default_parallel 30;

注：map 任务的歌声由输入的大小决定(每个HDFS块一个map），不受PARALLEL 子句影响。

### 参数替换

以下脚本中，$input, $output 用来指定输入和输出路径：

	$ cat max_temp_param.pig
	records = LOAD '$input' AS (year:chararray, temperature:int, quality:int);
	filtered_records = FILTER records BY temperature != 9999 AND (quality == 0 OR quality == 1 OR quality == 4 OR quality == 5 OR quality == 9);
	grouped_records = GROUP filtered_records BY year;
	max_temp = FOREACH grouped_records GENERATE group, MAX(filtered_records.temperature);
	STORE max_temp INTO '$output';

运行：

	$ pig -param input=/input/ncdc/micro-tab/sample.txt -param output=/tmp/out max_temp_param.pig

也可以将参数放在文件中：

	$ cat max_temp_param.param
	# Input file
	input=/input/ncdc/micro-tab/sample.txt
	# Output file
	output=/tmp/out

运行：

	$ pig -param_file max_temp_param.param max_temp_param.pig
