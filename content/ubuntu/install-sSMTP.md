Title: sSMTP发送邮件
Date: 2015-07-06 15:00
Tags: Debian, sSMTP
Slug: install-sSMTP
Author: ox0spy
Summary: 在Debian上安装sSMTP做邮件发送


工作中很多场景需要发送邮件，如：报警邮件、日报等。本文介绍如何安装、配置sSMTP做邮件发送。

## 安装

    :::bash
    $ sudo apt-get install ssmtp

## 配置

/etc/ssmtp/revaliases

    :::bash
    $ cat /etc/ssmtp/revaliases
    # sSMTP aliases
    #
    # Format:   local_account:outgoing_address:mailhub
    #
    # Example: root:your_login@your.domain:mailhub.your.domain[:port]
    # where [:port] is an optional port number that defaults to 25.
    nagios:no-reply@example.com:mail.example.com:587
    root:no-reply@example.com:mail.example.com:587 

/etc/ssmtp/ssmtp.conf

    :::bash
    $ #
    # Config file for sSMTP sendmail
    #
    # The person who gets all mail for userids < 1000
    # Make this empty to disable rewriting.
    root=<your-email@example.com>
    # The place where the mail goes. The actual machine name is required no
    # MX records are consulted. Commonly mailhosts are named mail.domain.com
    mailhub=<mail.example.com>
    # Where will the mail seem to come from?
    #rewriteDomain=
    # The full hostname
    hostname=<mail.example.com>
    # Are users allowed to set their own From: address?
    # YES - Allow the user to specify their own From: address
    # NO - Use the system generated From: address
    FromLineOverride=YES
    UseSTARTTLS=yes
    UseTLS=yes
    AuthUser=<your-domain/username>
    AuthPass=<your-passwd>

## 测试

    :::bash
    $ /usr/sbin/sendmail -t -F your-domain-name <<EOF
    SUBJECT: $YOUR-SUBJECT
    TO: A@example.com,B@example.com
    MIME-VERSION: 1.0
    Content-type: text/plain
    $YOUR-MAIL-BODY
     
    EOF

