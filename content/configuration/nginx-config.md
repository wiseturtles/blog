Title: Nginx获取客户端真实IP，X-Real-IP和X-Forwarded-For注意
Date: 2015-02-28 16:58
Tags: nginx, x_real_ip, x_forwarded_for
Slug: nginx-config
Author: crazygit
Summary: Nginx获取客户端真实IP, X-Real-IP和X-Forwarded-For注意
status: draft


本文参考于:

* http://serverfault.com/questions/314574/nginx-real-ip-header-and-x-forwarded-for-seems-wrong/414166
* http://luyadong.blog.51cto.com/2876653/851964
* http://nginx.org/en/docs/http/ngx_http_realip_module.html
* http://distinctplace.com/infrastructure/2014/04/23/story-behind-x-forwarded-for-and-x-real-ip-headers/


# X-Real-IP和X-Forwarded-For的注意
在配置nginx反向代理时，我们往往做如下配置
<pre>
    location /uri {
            proxy_set_header   Host             $host;
            proxy_set_header   X-Real-IP        $remote_addr;
            proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
            proxy_connect_timeout   60s;  # nginx跟后端服务器连接超时时间(代理连接超时)
            proxy_send_timeout      90s;  # 后端服务器数据回传时间(代理发送超时)
            proxy_read_timeout      90s;  # 连接成功后，后端服务器响应时间(代理接收超时)
            proxy_buffer_size        4k;  # 设置代理服务器（nginx）保存用户头信息的缓冲区大小
            proxy_buffers         4 32k;  # proxy_buffers缓冲区，网页平均在32k以下的设置
            proxy_busy_buffers_size 64k;  # 高负荷下缓冲大小（proxy_buffers*2）
            proxy_temp_file_write_size 64k; # 设定缓存文件夹大小，大于这个值，将从upstream服务器传
            proxy_buffering         off;
            proxy_ignore_client_abort on;
            proxy_pass   http://xx.xx.xx.xx;
</pre>

注意当中的这两行

    proxy_set_header   X-Real-IP        $remote_addr;
    proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;

根据维基百科描述,

X-Forwarded-for的格式应该如下:

    X-Forwarded-For: client1, proxy1, proxy2, ...

而nginx中，每次都是取X-Forwarded-For 中最右边的IP作为X-Real-IP的值，明显最右边的IP是一个反向代理的IP，而不是真实的客户端IP，这么做貌似是不正确的, 我们应该使用最左边的值作为X-Real-IP的值，但是nginx为什么要做么做时。





## 获取真实的客户端IP

为了获取真实的客户端IP,　需要使用ngx_http_realip_module模块，默认这个模块没有启动，需要在安装时使用`--with-http_realip_module`作为configuration的参数。
