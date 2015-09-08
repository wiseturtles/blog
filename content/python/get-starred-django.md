Title: Django入门
Date: 2015-08-18 14:22
Tags: python, django
Slug: get-started-django
Author: crazygit
Summary: Django入门
status: draft

## 常用命令

```bash
# 安装
$ pip install Django

# 创建项目
$ django-admin startproject mysite

# 创建app
$ python manage.py startapp myapp

# 生成migration文件
$ python manage.py makemigrations polls

# 打印Sql语句
$ python manage.py sqlmigrate polls 0001

```

## Models

1. 创建Model时，默认会创建主键`id`列, 除非代码显示定义了主键
2. 主键是只读的，不能修改主键列，如果修改的话，会新增一条记录，而不是修改原有的
```python
from django.db import models

class Fruit(models.Model):
    name = models.CharField(max_length=100, primary_key=True)


>>> fruit = Fruit.objects.create(name='Apple')
>>> fruit.name = 'Pear'
>>> fruit.save()
>>> Fruit.objects.values_list('name', flat=True)
['Apple', 'Pear']
```

3. Model 字段的名字不能是python的关键字或包含多个连在一起的下划线，会和Django的查询语法冲突
