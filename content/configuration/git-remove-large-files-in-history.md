Title: git从历史中删除大文件
Date: 2016-08-24 18:20
Tags: Git
Slug: git-remove-large-files-in-history
Author: ox0spy
Summary: git从历史中删除大文件


如果有人在git库中提交了超大文件导致所有人下载代码都比较耗时怎么办？

## 删除git库中的大文件

我们知道git会保留历史记录，即使删除这些大文件并提交也无法减少git库的体积。

可以用 `git filter-branch` 解决，比如：删除误提交的 `src/node_modules` 目录。

    $ git filter-branch --tree-filter 'rm -rf src/node_modules' --prune-empty

## 找出git库中体积最大的文件

    $ git rev-list master | while read rev; do git ls-tree -lr $rev | cut -c54- | grep -v '^ '; done | sort -u | perl -e '
        while (<>) {
            chomp;
            @stuff=split("\t");
            $sums{$stuff[1]} += $stuff[0];
        }
        print "$sums{$_} $_\n" for (keys %sums);
        ' | sort -rn

注：
1. 这段代码来自 - http://blog.jessitron.com/2013/08/finding-and-removing-large-files-in-git.html
2. 还有个类似的工具有兴趣可以尝试 - [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)
