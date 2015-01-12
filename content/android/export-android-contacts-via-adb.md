Title: export Android cantacts with vCard format via adb
Date: 2015-01-11 15:20
Tags: Android, vCard, adb
Slug: android-vcard-from-command-line
Author: Zhang Wanming
Summary: export Android contacts with vCard format via adb


参考:
<http://www.commandlinefu.com/commands/view/11688/dump-android-contacts-sms>


昨天手机(TCL S960)掉地下把屏幕摔坏了，Google被xx后，就没在用过其它通讯录同步，只好想办法从坏手机里导出，屏幕完全坏了，只能通过adb完成。

获取通讯录
===========

通过adb从手机中导出通讯录，可以用如下方法：

1. am

        :::bash
        $ adb shell am start -t "text/x-vcard" -d "file:///sdcard/contacts.vcf" -a android.intent.action.VIEW com.android.contacts

2. get contacts.db

        :::bash
        $ adb pull /data/data/com.android.providers.contacts/databases/contacts2.db .
        sqlite3 -batch <<EOF contacts2.db <CR> .header on <CR> .mode tabs <CR> select * from data; <CR> EOF


方法一无法运行报错，方法二需要root权限。

Android拿root权限貌似就两种方法: xx root工具(通过系统漏洞获取root权限); 刷recory分区。
我没找到该机型的recory，而是用360一键root，拿到root权限。

有了root权限，通过方法二就可以拿到通讯录数据了，剩下的就是生成vCard格式。
github上已经有人写了通过contacts2.db生成vCard文件的小工具。

    :::bash
    $ git clone git@github.com:stachre/dump-contacts2db.git
    $ cd dump-contacts2db
    $ bash dump-contacts2db.sh path/to/contacts2.db > path/to/contacts.vcf


如果还希望获取手机里的短信，可以用下面的命令:

    :::bash
    $ adb pull /data/data/com.android.providers.telephony/databases/mmssms.db
    $ sqlite3 -batch <<EOF mmssms.db <CR> .header on <CR> .mode tabs <CR> select * from sms; <CR> EOF


Android解锁
============
Android解锁我没试过，命令如下：

    :::bash
    adb shell
    cd /data/data/com.android.providers.settings/databases
    sqlite3 settings.db
    update system set value=0 where name=’lock_pattern_autolock';
    update secure set value=0 where name=’lock_pattern_autolock';
    update system set value=0 where name=’lockscreen.lockedoutpermanently';
    update secure set value=0 where name=’lockscreen.lockedoutpermanently';
    .quit

如果是忘了Android锁屏图案，想找回，可以试试 https://github.com/sch3m4/androidpatternlock
