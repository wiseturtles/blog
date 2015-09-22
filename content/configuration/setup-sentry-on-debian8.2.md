Title:  Debian 8.2上安装Sentry
Date: 2015-09-22 15:55
Tags: sentry
Slug: setup-sentry-on-debian-8.2
Author: ox0spy
Summary: 在Debian 8.2上安装Sentry

Sentry是一个很好用的错误、异常收集平台，支持Python, Node.js, PHP, Ruby, Java, Go以及Android、iOS。

## 系统环境

查看系统版本。

    :::bash
    $ lsb_release -a
    No LSB modules are available.
    Distributor ID: Debian
    Description:    Debian GNU/Linux 8.2 (jessie)
    Release:    8.2
    Codename:   jessie

## 准备数据库环境

[官方安装文档]()

virtualenv的安装、配置就不再介绍了。

    :::bash
    $ sudo apt-get install postgresql libpq-dev
    $ mkvirtualenv sentry
    (sentry)$ pip install psycopg2

在PostgreSQL中为sentry创建数据库。

    :::bash
    $ sudo -u postgre createuser --superuser sentry
    $ sudo -u sentry psql
    postgres=# \password sentry
    Enter new password:
    Enter it again:
    postgres=# \q
    $ sudo -u sentry createdb -E utf8 sentry

## 安装sentry

数据库使用的是PostgreSQL，使用公司邮件服务器发送邮件。

    :::bash
    $ workon sentry
    (sentry)$ pip install sentry
    (sentry)$ sentry init /tmp/settings.py
    (sentry)$ sudo mv /tmp/settings.py /etc/sentry/sentry.conf.py

/etc/sentry/sentry.conf.py中的数据库配置如下：

    :::bash
    DATABASES = {
        'default': {
            # You can swap out the engine for MySQL easily by changing this value
            # to ``django.db.backends.mysql`` or to PostgreSQL with
            # ``sentry.db.postgres``

            # If you change this, you'll also need to install the appropriate python
            # package: psycopg2 (Postgres) or mysql-python
            'ENGINE': 'django.db.backends.postgresql_psycopg2',

            'NAME': 'sentry',
            'USER': 'sentry',
            'PASSWORD': 'xxxx',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

/etc/sentry/sentry.conf.py中的Web服务配置如下：

    :::bash
    # You MUST configure the absolute URI root for Sentry:
    SENTRY_URL_PREFIX = 'http://your-ip'  # No trailing slash!

    SENTRY_WEB_HOST = 'localhost'
    SENTRY_WEB_PORT = 9000
    SENTRY_WEB_OPTIONS = {
        'workers': 4,  # the number of gunicorn workers
        # 'secure_scheme_headers': {'X-FORWARDED-PROTO': 'https'},
    }

/etc/sentry/sentry.conf.py中的邮件配置根据个人情况修改。

修改完配置运行如下命令:

    :::bash
    (sentry)$ sentry --config=/etc/sentry/sentry.conf.py upgrade
    (sentry)$ sentry --config=/etc/sentry/sentry.conf.py repair

创建sentry超级用户:

    :::bash
    (sentry)$ sentry --config=/etc/sentry/sentry.conf.py createsuperuser

启动Web服务命令如下:

    :::bash
    (sentry)$ sentry --config=/etc/sentry/sentry.conf.py start

启动后就可以访问 http://your-ip:9000 了，用刚才创建的超级用户登录。

启动sentry worker:

    :::bash
    (sentry)$ sentry --config=/etc/sentry/sentry.conf.py celery worker -B -l WARNING

## 正式环境运行sentry

### supervisor管理sentry, sentry_worker

通过supervisor管理sentry, sentry_worker；并用nginx做反向代理。

supervisor的安装也不再介绍。

supervisor管理sentry:

    :::bash
    $ cat /etc/supervisor/conf.d/sentry.conf
    [program:sentry]
    #directory=/var/www/.virtualenvs/sentry/bin/
    environment=VIRTUAL_ENV_PATH="/var/www/.virtualenvs/sentry/bin/"
    command=/var/www/.virtualenvs/sentry/bin/sentry --config=/etc/sentry/sentry.conf.py start
    user=develop
    stdout_logfile=/data/log/supervisor/sentry.stdout
    stderr_logfile=/data/log/supervisor/sentry.stderr
    autostart=true
    autorestart=true
    killasgroup=true

supervisor管理sentry_worker:

    :::bash
    $ cat /etc/supervisor/conf.d/sentry_worker.conf
    [program:sentry_worker]
    #directory=/var/www/.virtualenvs/sentry/bin/
    environment=VIRTUAL_ENV_PATH="/var/www/.virtualenvs/sentry/bin/"
    command=/var/www/.virtualenvs/sentry/bin/sentry --config=/etc/sentry/sentry.conf.py celery worker -B -l WARNING
    user=develop
    stdout_logfile=/data/log/supervisor/sentry_worker.stdout
    stderr_logfile=/data/log/supervisor/sentry_worker.stderr
    autostart=true
    autorestart=true
    killasgroup=true

启动sentry, sentry_worker:

    :::bash
    $ sudo service supervisor restart
    $ sudo supervisorctl  # 查看sentry, sentry_worker运行情况

### 配置Nginx

/etc/nginx/sites-available/default的server配置中增加如下内容:

    ```
    proxy_set_header   Host                 $http_host;
    proxy_set_header   X-Real-IP            $remote_addr;
    proxy_set_header   X-Forwarded-For      $proxy_add_x_forwarded_for;
    proxy_set_header   X-Forwarded-Proto    $scheme;
    proxy_redirect     off;

    location / {
        proxy_pass         http://localhost:9000;
    }

    location ~* /api/(?P<projectid>\d+/)?store/ {
            proxy_pass        http://127.0.0.1:9000;
    }
    ```

重启nginx，并通过http://your-ip 访问。
