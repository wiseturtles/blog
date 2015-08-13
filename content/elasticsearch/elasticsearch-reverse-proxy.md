Title: Elastichsearch反向代理设置
Date: 2015-08-12 17:29
Category: Elasticsearch
Tags: elasticsearch, reverse, proxy
Slug: elasticsearch-reverse-proxy
Authors: craygit
Summary: Elastichsearch反向代理设置


内网的ES集群，平时操作都是通过命令行，有点不方便，而且安装的site插件也没法使用
，比较蛋疼，所以配置nginx作为elasticsearch的反向代理，并且添加认证信息.

如果是直接用域名的根节点作为反向代理的话，比较简单，直接配置一下就可以，但是问
题是根节点被暂用，需要设置一个前缀来来访问, 就稍微麻烦一点.

nginx配置如下:

<pre>
    location ~ ^/es/ {
            rewrite ^/es/(.*)$ /$1 break;
            include proxy_params;
            proxy_pass http://es_node_ip:9200;
            proxy_redirect http://$host/ http://$host/es/;
            auth_basic "please login";
            auth_basic_user_file /data/passwd/es.htpasswd;
    }
</pre>

几点需要注意：

1. `include proxy_params;` proxy_params为一些反向代理设置参数，没有的话可以去掉
2. `proxy_pass http://es_node_ip:9200;` 需要替换es_node_ip 为ES集群的IP,
3. `auth_basic_user_file /data/passwd/es.htpasswd`中`/data/passwd/es.htpasswd`为认证文件，可以用apache工具或一些[在线工具](http://tool.oschina.net/htpasswd)生成

假设域名为www.example.com, 那么就可以直接访问

* <http://www.example.com/es/>
* <http://www.example.com/es/\_plugin/head/>

配置好之后，用起来爽多了。
