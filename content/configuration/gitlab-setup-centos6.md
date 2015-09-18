Title:  Gitlab安装
Date: 2015-09-18 13:13
Tags: gitlab
Slug: gitlab-setup-on-centos6
Author: ox0spy
Summary: 在Centos6上安装Gitlab

公司没有统一的代码管理平台，虽然曾经用过stash、jira、confluence，但调研后还是觉得用gitlab。
下面介绍下gitlab安装、配置。

## 系统环境

查看系统版本。

    :::bash
    $ cat /etc/issue
    CentOS release 6.6 (Final)
    Kernel \r on an \m

## 安装gitlab

[官方安装文档](https://about.gitlab.com/downloads/#centos6)介绍的比较详细，
我用公司邮箱发送邮件，所以，没有安装postfix。

    :::bash
    $ sudo yum install curl openssh-server cronie
    $ sudo lokkit -s http -s ssh
    $ curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.rpm.sh | sudo bash
    $ sudo yum install gitlab-ce


## 配置gitlab

数据库使用的是PostgreSQL，使用公司邮件服务器。

    :::bash
    --- /etc/gitlab/gitlab.rb.back  2015-09-07 16:31:05.247042700 +0800
    +++ /etc/gitlab/gitlab.rb   2015-09-09 14:47:33.710061343 +0800
    @@ -3,7 +3,7 @@
    ## Url on which GitLab will be reachable.
    ## For more details on configuring external_url see:
    ## https://gitlab.com/gitlab-org/omnibus-gitlab/blob/629def0a7a26e7c2326566f0758d4a27857b52a3/README.md#configuring-the-external-url-for-gitlab
    -external_url 'http://iZ23rkm97f5Z'
    +external_url 'http://your-git-domain'


    ## Note: configuration settings below are optional.
    @@ -14,23 +14,23 @@

    # gitlab_rails['gitlab_ssh_host'] = 'ssh.host_example.com'
    gitlab_rails['time_zone'] = 'UTC'
    -# gitlab_rails['gitlab_email_enabled'] = true
    -# gitlab_rails['gitlab_email_from'] = 'example@example.com'
    -# gitlab_rails['gitlab_email_display_name'] = 'Example'
    -# gitlab_rails['gitlab_email_reply_to'] = 'noreply@example.com'
    -# gitlab_rails['gitlab_default_can_create_group'] = true
    -# gitlab_rails['gitlab_username_changing_enabled'] = true
    -# gitlab_rails['gitlab_default_theme'] = 2
    -# gitlab_rails['gitlab_restricted_visibility_levels'] = nil # to restrict public and internal: ['public', 'internal']
    -# gitlab_rails['gitlab_default_projects_features_issues'] = true
    -# gitlab_rails['gitlab_default_projects_features_merge_requests'] = true
    -# gitlab_rails['gitlab_default_projects_features_wiki'] = true
    -# gitlab_rails['gitlab_default_projects_features_snippets'] = false
    -# gitlab_rails['gitlab_default_projects_features_visibility_level'] = 'private'
    -# gitlab_rails['gitlab_repository_downloads_path'] = 'tmp/repositories'
    +gitlab_rails['gitlab_email_enabled'] = true
    +gitlab_rails['gitlab_email_from'] = 'noreply@yourdomain'
    +gitlab_rails['gitlab_email_display_name'] = 'Gitlab'
    +gitlab_rails['gitlab_email_reply_to'] = 'noreply@yourdomain'
    +gitlab_rails['gitlab_default_can_create_group'] = true
    +gitlab_rails['gitlab_username_changing_enabled'] = true
    +gitlab_rails['gitlab_default_theme'] = 2
    +gitlab_rails['gitlab_restricted_visibility_levels'] = ['public', 'internal'] # to restrict public and internal: ['public', 'internal']
    +gitlab_rails['gitlab_default_projects_features_issues'] = true
    +gitlab_rails['gitlab_default_projects_features_merge_requests'] = true
    +gitlab_rails['gitlab_default_projects_features_wiki'] = true
    +gitlab_rails['gitlab_default_projects_features_snippets'] = false
    +gitlab_rails['gitlab_default_projects_features_visibility_level'] = 'private'
    +gitlab_rails['gitlab_repository_downloads_path'] = 'tmp/repositories'
    # gitlab_rails['gravatar_plain_url'] = 'http://www.gravatar.com/avatar/%{hash}?s=%{size}&d=identicon'
    # gitlab_rails['gravatar_ssl_url'] = 'https://secure.gravatar.com/avatar/%{hash}?s=%{size}&d=identicon'
    -# gitlab_rails['webhook_timeout'] = 10
    +gitlab_rails['webhook_timeout'] = 10

    ## For setting up LDAP
    ## see https://gitlab.com/gitlab-org/omnibus-gitlab/blob/629def0a7a26e7c2326566f0758d4a27857b52a3/README.md#setting-up-ldap-sign-in
    @@ -107,9 +107,9 @@
    ## For setting up backups
    ## see https://gitlab.com/gitlab-org/omnibus-gitlab/blob/629def0a7a26e7c2326566f0758d4a27857b52a3/README.md#backups

    -# gitlab_rails['backup_path'] = "/var/opt/gitlab/backups"
    -# gitlab_rails['backup_archive_permissions'] = 0644 # See: http://doc.gitlab.com/ce/raketasks/backup_restore.html#backup-archive-permissions
    -# gitlab_rails['backup_keep_time'] = 604800
    +gitlab_rails['backup_path'] = "/var/opt/gitlab/backups"
    +gitlab_rails['backup_archive_permissions'] = 0644 # See: http://doc.gitlab.com/ce/raketasks/backup_restore.html#backup-archive-permissions
    +gitlab_rails['backup_keep_time'] = 604800
    # gitlab_rails['backup_upload_connection'] = {
    #   'provider' => 'AWS',
    #   'region' => 'eu-west-1',
    @@ -128,9 +128,9 @@
    # gitlab_rails['satellites_timeout'] = 30

    ## GitLab Shell settings for GitLab
    -# gitlab_rails['gitlab_shell_ssh_port'] = 22
    -# gitlab_rails['git_max_size'] = 20971520
    -# gitlab_rails['git_timeout'] = 10
    +gitlab_rails['gitlab_shell_ssh_port'] = 22
    +gitlab_rails['git_max_size'] = 20971520
    +gitlab_rails['git_timeout'] = 10

    ## Extra customization
    # gitlab_rails['extra_google_analytics_id'] = '_your_tracking_id'
    @@ -161,9 +161,9 @@
    # GitLab application settings #
    ###############################

    -# gitlab_rails['uploads_directory'] = "/var/opt/gitlab/gitlab-rails/uploads"
    -# gitlab_rails['rate_limit_requests_per_period'] = 10
    -# gitlab_rails['rate_limit_period'] = 60
    +gitlab_rails['uploads_directory'] = "/var/opt/gitlab/gitlab-rails/uploads"
    +gitlab_rails['rate_limit_requests_per_period'] = 10
    +gitlab_rails['rate_limit_period'] = 60

    # Change the initial default admin password.
    # Only applicable on inital setup, changing this setting after database is created and seeded
    @@ -176,13 +176,13 @@
    ## see https://gitlab.com/gitlab-org/omnibus-gitlab/blob/629def0a7a26e7c2326566f0758d4a27857b52a3/doc/settings/database.md#database-settings
    ## Only needed if you use an external database.

    -# gitlab_rails['db_adapter'] = "postgresql"
    -# gitlab_rails['db_encoding'] = "unicode"
    -# gitlab_rails['db_database'] = "gitlabhq_production"
    -# gitlab_rails['db_pool'] = 10
    -# gitlab_rails['db_username'] = "gitlab"
    -# gitlab_rails['db_password'] = nil
    -# gitlab_rails['db_host'] = nil
    +gitlab_rails['db_adapter'] = "postgresql"
    +gitlab_rails['db_encoding'] = "unicode"
    +gitlab_rails['db_database'] = "gitlab"
    +gitlab_rails['db_pool'] = 10
    +gitlab_rails['db_username'] = "gitlab"
    +gitlab_rails['db_password'] = nil
    +gitlab_rails['db_host'] = nil
    # gitlab_rails['db_port'] = 5432
    # gitlab_rails['db_socket'] = nil
    # gitlab_rails['db_sslmode'] = nil
    @@ -206,15 +206,15 @@
    # see https://gitlab.com/gitlab-org/omnibus-gitlab/blob/629def0a7a26e7c2326566f0758d4a27857b52a3/doc/settings/smtp.md#smtp-settings
    # Use smtp instead of sendmail/postfix.

    -# gitlab_rails['smtp_enable'] = true
    -# gitlab_rails['smtp_address'] = "smtp.server"
    -# gitlab_rails['smtp_port'] = 456
    -# gitlab_rails['smtp_user_name'] = "smtp user"
    -# gitlab_rails['smtp_password'] = "smtp password"
    -# gitlab_rails['smtp_domain'] = "example.com"
    -# gitlab_rails['smtp_authentication'] = "login"
    -# gitlab_rails['smtp_enable_starttls_auto'] = true
    -# gitlab_rails['smtp_tls'] = false
    +gitlab_rails['smtp_enable'] = true
    +gitlab_rails['smtp_address'] = "smtp.xxx.com"
    +gitlab_rails['smtp_port'] = 25
    +gitlab_rails['smtp_user_name'] = "noreply@yourdomain"
    +gitlab_rails['smtp_password'] = "yourpassword"
    +gitlab_rails['smtp_domain'] = "yourdomain"
    +gitlab_rails['smtp_authentication'] = "login"
    +gitlab_rails['smtp_enable_starttls_auto'] = false
    +gitlab_rails['smtp_tls'] = false
    # gitlab_rails['smtp_openssl_verify_mode'] = 'none' # Can be: 'none', 'peer', 'client_once', 'fail_if_no_peer_cert', see http://api.rubyonrails.org/classes/ActionMailer/Base.html
    # gitlab_rails['smtp_ca_path'] = "/etc/ssl/certs"
    # gitlab_rails['smtp_ca_file'] = "/etc/ssl/certs/ca-certificates.crt"
    @@ -242,18 +242,18 @@
    ##################
    ## Tweak unicorn settings.

    -# unicorn['worker_timeout'] = 60
    -# unicorn['worker_processes'] = 2
    +unicorn['worker_timeout'] = 60
    +unicorn['worker_processes'] = 2

    ## Advanced settings
    -# unicorn['listen'] = '127.0.0.1'
    -# unicorn['port'] = 8080
    -# unicorn['socket'] = '/var/opt/gitlab/gitlab-rails/sockets/gitlab.socket'
    -# unicorn['pidfile'] = '/opt/gitlab/var/unicorn/unicorn.pid'
    +unicorn['listen'] = '127.0.0.1'
    +unicorn['port'] = 8088
    +unicorn['socket'] = '/var/opt/gitlab/gitlab-rails/sockets/gitlab.socket'
    +unicorn['pidfile'] = '/opt/gitlab/var/unicorn/unicorn.pid'
    # unicorn['tcp_nopush'] = true
    -# unicorn['backlog_socket'] = 1024
    +unicorn['backlog_socket'] = 1024
    # Make sure somaxconn is equal or higher then backlog_socket
    -# unicorn['somaxconn'] = 1024
    +unicorn['somaxconn'] = 1024
    # We do not recommend changing this setting
    # unicorn['log_directory'] = "/var/log/gitlab/unicorn"

    @@ -290,11 +290,11 @@
    # GitLab PostgreSQL #
    #####################

    -# postgresql['enable'] = true
    -# postgresql['listen_address'] = nil
    -# postgresql['port'] = 5432
    -# postgresql['data_dir'] = "/var/opt/gitlab/postgresql/data"
    -# postgresql['shared_buffers'] = "256MB" # recommend value is 1/4 of total RAM, up to 14GB.
    +postgresql['enable'] = true
    +postgresql['listen_address'] = nil
    +postgresql['port'] = 5432
    +postgresql['data_dir'] = "/var/opt/gitlab/postgresql/data"
    +postgresql['shared_buffers'] = "256MB" # recommend value is 1/4 of total RAM, up to 14GB.

    ## Advanced settings
    # postgresql['ha'] = false
    @@ -326,7 +326,7 @@
    ################
    ## Can be disabled if you are using your own redis instance.

    -# redis['enable'] = true
    +redis['enable'] = true
    # redis['username'] = "gitlab-redis"
    # redis['uid'] = nil
    # redis['gid'] = nil
    @@ -470,14 +470,14 @@
    ## see https://gitlab.com/gitlab-org/omnibus-gitlab/tree/629def0a7a26e7c2326566f0758d4a27857b52a3/doc/settings/database.md#database-settings
    ## Only needed if you use an external database.

    -# gitlab_ci['db_adapter'] = "postgresql"
    -# gitlab_ci['db_encoding'] = "unicode"
    -# gitlab_ci['db_database'] = "gitlab_ci_production"
    +gitlab_ci['db_adapter'] = "postgresql"
    +gitlab_ci['db_encoding'] = "unicode"
    +gitlab_ci['db_database'] = "gitlab_ci_production"
    # gitlab_ci['db_pool'] = 10
    -# gitlab_ci['db_username'] = "gitlab_ci"
    -# gitlab_ci['db_password'] = nil
    -# gitlab_ci['db_host'] = nil
    -# gitlab_ci['db_port'] = 5432
    +gitlab_ci['db_username'] = "gitlab_ci"
    +gitlab_ci['db_password'] = nil
    +gitlab_ci['db_host'] = nil
    +gitlab_ci['db_port'] = 5432
    # gitlab_ci['db_socket'] = nil
    # gitlab_ci['db_sslmode'] = nil
    # gitlab_ci['db_sslrootcert'] = nil
    @@ -497,6 +497,15 @@
    ###################################
    ## see https://gitlab.com/gitlab-org/omnibus-gitlab/tree/629def0a7a26e7c2326566f0758d4a27857b52a3/doc/settings/smtp.md#smtp-settings

    +gitlab_ci['smtp_enable'] = true
    +gitlab_ci['smtp_address'] = "smtp.xxx.com"
    +gitlab_ci['smtp_port'] = 25
    +gitlab_ci['smtp_user_name'] = "noreply@yourdomain"
    +gitlab_ci['smtp_password'] = "yourpassword"
    +gitlab_ci['smtp_domain'] = "yourdomain"
    +gitlab_ci['smtp_authentication'] = "login"
    +gitlab_ci['smtp_enable_starttls_auto'] = false
    +gitlab_ci['smtp_tls'] = false
    # gitlab_ci['smtp_enable'] = true
    # gitlab_ci['smtp_address'] = "smtp.server"
    # gitlab_ci['smtp_port'] = 456


根据/etc/gitlab/gitlab.rb重新配置gitlab。

    :::bash
    $ sudo gitlab-ctl reconfigure

使用默认用户名:`root` 密码:`5iveL!fe`登陆，登陆后修改默认密码。


## 备份

    :::bash
    $ sudo crontab -l
    0 2 * * * /opt/gitlab/bin/gitlab-rake gitlab:backup:create
