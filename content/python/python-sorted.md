Title: Python Sort
Date: 2015-09-08 17:31
Tags: python, sort
Slug: python-sort
Author: crazygit
Summary: python-sort
status: draft


```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random


def get_random_list(num):
    t = []
    for i in range(0, num):
        t.append(random.randint(0, 200))
    return t


def bubble_sort(t):
    '''从小到大'''
    passnum = len(t) - 1
    exchanges = True
    while passnum > 0 and exchanges:
        for i in range(passnum):
            if t[i] > t[i + 1]:
                exchanges = True
                t[i], t[i + 1] = t[i + 1], t[i]
        passnum -= 1


def bubble_sort2(alist):
    passnum = len(alist) - 1
    '''从小到大'''
    for i in range(passnum, 1, -1):
        change = False
        for j in range(0, i):
            if alist[j] > alist[j + 1]:
                change = True
                alist[j], alist[j + 1] = alist[j + 1], alist[j]
        print alist
        if not change:
            return


def qsort(alist):
    if len(alist) <= 1:
        return alist
    return qsort([lt for lt in alist[1:] if lt < alist[0]]) + [alist[0]] + qsort([gt for gt in alist[1:] if gt >= alist[0]])


if __name__ == '__main__':
    alist = get_random_list(10)
    bubble_sort(alist)
    print alist
    bubble_sort2(alist)
    print alist
    alist = qsort(alist)
    print alist

```
